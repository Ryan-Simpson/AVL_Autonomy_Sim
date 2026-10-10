"""Validate the built rover and bridge against the adopted ROS contract."""

import importlib.util
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest
import xacro
import yaml

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]


def load_script(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bridge_matches_contract_and_fortress_model():
    contract = yaml.safe_load((ROOT / 'ros2/topic_map/topics.yaml').read_text())
    bridges = yaml.safe_load((PACKAGE / 'config/bridge.yaml').read_text())
    robot = ET.fromstring(xacro.process_file(str(PACKAGE / 'urdf/tracked_rover.urdf.xacro')).toxml())
    drive = robot.find("gazebo/plugin[@name='ignition::gazebo::systems::DiffDrive']")
    assert drive is not None
    by_name = {bridge['ros_topic_name']: bridge for bridge in bridges}
    assert len(by_name) == len(bridges) == 3
    for interface, field, direction in (
            ('cmd_vel', 'topic', 'ROS_TO_GZ'), ('wheel_odom', 'odom_topic', 'GZ_TO_ROS')):
        topic = contract['topics'][interface]
        bridge = by_name[topic['name']]
        assert bridge['ros_type_name'] == topic['type']
        assert bridge['gz_topic_name'] == drive.findtext(field)
        assert bridge['direction'] == direction
    assert drive.findtext('frame_id') == contract['frame_ids']['odom']
    assert drive.findtext('child_frame_id') == contract['frame_ids']['base_link']
    assert drive.findtext('odom_publish_frequency') == '50'
    world = ET.parse(ROOT / 'gazebo/worlds/igvc_course.sdf').find('world').attrib['name']
    assert by_name['/clock']['gz_topic_name'] == '/world/%s/clock' % world
    assert by_name['/clock']['direction'] == 'GZ_TO_ROS'
    assert all(bridge['gz_type_name'].startswith('ignition.msgs.') for bridge in bridges)
    assert '/odometry/filtered' not in by_name  # The local EKF must own filtered odometry.
    joints = {joint.attrib['name'] for joint in robot.findall('joint')}
    assert all(joint.text in joints for side in ('left_joint', 'right_joint')
               for joint in drive.findall(side))


@pytest.mark.parametrize('before,after,c0,c1,valid', [
    ((0, 0), (0, 0.2), 0, 100, True),
    ((0, 0), (0, 0), 0, 100, False),
    ((0, 0), (0.2, 0), 100, 100, False),
    ((0, 0), (float('nan'), 0), 0, 100, False),
])
def test_motion_requires_finite_displacement_and_advancing_clock(before, after, c0, c1, valid):
    checker = load_script('checker', PACKAGE / 'scripts/check_closed_loop.py')
    _, errors = checker.assess_motion(before, after, c0, c1)
    assert (not errors) == valid


def test_inventory_keeps_unknowns_and_never_publishes():
    capture = load_script('capture', ROOT / 'tools/capture_jetson_inventory.py')
    contract = yaml.safe_load((ROOT / 'ros2/topic_map/topics.yaml').read_text())
    calls = []

    def runner(arguments, seconds):
        calls.append(arguments)
        output = '/wheel_odom [nav_msgs/msg/Odometry]\n' if arguments == ['topic', 'list', '-t'] else ''
        return {'status': 'ok', 'stdout': output, 'stderr': ''}

    result = capture.collect(contract, 1, runner)
    assert len(result['topics']) == len(contract['topics']) == 22
    observed = [record for record in result['topics'] if record['seen']]
    assert len(observed) == 1
    assert observed[0]['interface'] == 'wheel_odom'
    assert 'child_frame_id' in observed[0]
    assert not any('pub' in call or 'set' in call for call in calls)
    assert contract['status'] == 'adopted'


def test_inventory_rejects_failed_graph_capture():
    capture = load_script('capture', ROOT / 'tools/capture_jetson_inventory.py')
    with pytest.raises(RuntimeError, match='Could not list ROS topics'):
        capture.collect({'topics': {}}, 1, lambda *args: {
            'status': 'error', 'stdout': '', 'stderr': 'ROS unavailable'})


def test_inventory_preserves_partial_rate_samples():
    capture = load_script('capture', ROOT / 'tools/capture_jetson_inventory.py')
    contract = {'status': 'adopted', 'topics': {'lidar': {
        'name': '/velodyne_points', 'type': 'sensor_msgs/msg/PointCloud2',
        'frame_id': 'velodyne'}}}

    def runner(arguments, seconds):
        if arguments == ['topic', 'list', '-t']:
            return {'status': 'ok', 'stdout': '/velodyne_points [sensor_msgs/msg/PointCloud2]\n',
                    'stderr': ''}
        return {'status': 'timeout', 'stdout': 'average rate: 9.9\n', 'stderr': ''}

    record = capture.collect(contract, 1, runner)['topics'][0]
    assert record['rate_sample']['status'] == 'timeout'
    assert record['rate_sample']['stdout'] == 'average rate: 9.9\n'
    assert record['header']['status'] == 'timeout'
    assert record['contract']['frame_id'] == 'velodyne'
