#!/usr/bin/env python3
"""Read-only, bounded capture of the adopted MARVIN topic contract on a Jetson."""

import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess

import yaml


def run_ros(arguments, seconds):
    command = ['ros2', *arguments]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=seconds,
                                env={**os.environ, 'PYTHONUNBUFFERED': '1'})
        return {'command': command, 'status': 'ok' if result.returncode == 0 else 'error',
                'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else (value or '')
        return {'command': command, 'status': 'timeout',
                'stdout': decode(error.stdout), 'stderr': decode(error.stderr)}
    except FileNotFoundError:
        return {'command': command, 'status': 'error', 'stderr': 'ros2 executable not found',
                'stdout': ''}


def collect(contract, seconds, runner=run_ros):
    node_list = runner(['node', 'list'], seconds)
    topic_list = runner(['topic', 'list', '-t'], seconds)
    if topic_list['status'] != 'ok':
        raise RuntimeError('Could not list ROS topics: ' + topic_list['stderr'])
    seen = {line.split()[0] for line in topic_list['stdout'].splitlines() if line.startswith('/')}
    records = []
    for key, topic in contract['topics'].items():
        record = {'interface': key, 'contract': topic, 'seen': topic['name'] in seen}
        records.append(record)
        if not record['seen']:
            continue
        name = topic['name']
        record['endpoint_info'] = runner(['topic', 'info', '-v', name], seconds)
        record['rate_sample'] = runner(['topic', 'hz', name], seconds)
        # hz runs until interrupted: preserve its bounded output as a sample.
        record['rate_sample']['bounded_sample'] = True
        fields = []
        if topic.get('frame_id') or topic['type'] == 'nav_msgs/msg/Odometry':
            fields.append('header')
        if topic['type'] == 'nav_msgs/msg/Odometry':
            fields.append('child_frame_id')
        for field in fields:
            record[field] = runner([
                'topic', 'echo', name, topic['type'], '--once', '--field', field,
                '--qos-reliability', 'best_effort', '--qos-durability', 'volatile'], seconds)
    return {'captured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'contract_status': contract['status'], 'source': contract.get('source'),
            'ros_domain_id': os.environ.get('ROS_DOMAIN_ID', '0'),
            'ros_distro': os.environ.get('ROS_DISTRO', 'unknown'),
            'node_list': node_list, 'topic_list': topic_list, 'topics': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract', type=Path, default=Path(__file__).resolve().parents[1]
                        / 'ros2/topic_map/topics.yaml')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seconds', type=float, default=8.0,
                        help='Maximum wall time per ROS command (default: 8).')
    args = parser.parse_args()
    if not 0 < args.seconds <= 60:
        parser.error('--seconds must be between 0 and 60')
    try:
        contract = yaml.safe_load(args.contract.read_text())
        result = collect(contract, args.seconds)
    except (OSError, RuntimeError, yaml.YAMLError) as error:
        parser.exit(1, str(error) + '\n')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('Saved %d topic observations to %s. Missing topics are marked seen=false.'
          % (len(result['topics']), args.output))


if __name__ == '__main__':
    main()
