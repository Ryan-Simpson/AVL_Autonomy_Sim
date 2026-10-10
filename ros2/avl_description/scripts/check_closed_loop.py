#!/usr/bin/env python3
"""Bounded command-to-motion check for an isolated, running Gazebo instance."""

import argparse
import json
import math
import time


def assess_motion(before, after, clock_before, clock_after, minimum_distance=0.02):
    distance = math.hypot(after[0] - before[0], after[1] - before[1])
    errors = []
    if not all(math.isfinite(v) for v in (*before, *after)):
        errors.append('Odometry position contains non-finite values.')
    if clock_after <= clock_before:
        errors.append('Simulation clock did not advance.')
    if distance < minimum_distance:
        errors.append('Command produced less than %.3f m displacement.' % minimum_distance)
    return distance, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drive-sim', action='store_true', required=True,
                        help='Explicitly allow a short /cmd_vel command in simulation.')
    parser.add_argument('--timeout', type=float, default=45.0)
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('--timeout must be finite and positive')

    import rclpy
    from geometry_msgs.msg import Twist
    from nav_msgs.msg import Odometry
    from rclpy.qos import qos_profile_sensor_data
    from rosgraph_msgs.msg import Clock

    rclpy.init()
    node = rclpy.create_node('check_gazebo_closed_loop')
    state = {'clock': None, 'odom': None, 'errors': set()}
    publisher = node.create_publisher(Twist, '/cmd_vel', 10)
    started_driving = False
    deadline = time.monotonic() + args.timeout

    def clock_callback(msg):
        state['clock'] = msg.clock.sec * 1_000_000_000 + msg.clock.nanosec

    def odom_callback(msg):
        state['odom'] = msg
        if msg.header.frame_id != 'odom' or msg.child_frame_id != 'base_link':
            state['errors'].add('Expected odom -> base_link frame IDs.')

    node.create_subscription(Clock, '/clock', clock_callback, qos_profile_sensor_data)
    node.create_subscription(Odometry, '/wheel_odom', odom_callback, qos_profile_sensor_data)

    def spin_for(seconds):
        finish = min(time.monotonic() + seconds, deadline)
        while time.monotonic() < finish:
            rclpy.spin_once(node, timeout_sec=0.05)
        if time.monotonic() >= deadline:
            raise RuntimeError('Closed-loop check timed out.')

    def position(msg):
        return (msg.pose.pose.position.x, msg.pose.pose.position.y)

    def stamp(msg):
        return msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec

    try:
        while True:
            spin_for(0.1)
            subscribers = node.get_subscriptions_info_by_topic('/cmd_vel')
            odom_publishers = node.get_publishers_info_by_topic('/wheel_odom')
            if state['clock'] is not None and state['odom'] is not None and subscribers:
                if len(subscribers) != 1 or subscribers[0].node_name != 'gazebo_bridge':
                    raise RuntimeError('Expected only gazebo_bridge to consume /cmd_vel.')
                if len(odom_publishers) != 1 or odom_publishers[0].node_name != 'gazebo_bridge':
                    raise RuntimeError('Expected only gazebo_bridge to publish /wheel_odom.')
                break

        # Let the newly spawned rover settle before recording the baseline.
        for _ in range(20):
            publisher.publish(Twist())
            started_driving = True
            spin_for(0.1)
        before = position(state['odom'])
        stamp_before = stamp(state['odom'])
        clock_before = state['clock']
        command = Twist()
        command.linear.x = 0.15
        for _ in range(20):
            publisher.publish(command)
            spin_for(0.1)
        publisher.publish(Twist())
        spin_for(0.3)

        distance, errors = assess_motion(
            before, position(state['odom']), clock_before, state['clock'])
        errors.extend(sorted(state['errors']))
        if stamp(state['odom']) <= stamp_before:
            errors.append('Odometry timestamp did not advance.')
        result = {
            'status': 'FAIL' if errors else 'PASS',
            'displacement_m': distance if math.isfinite(distance) else None,
            'simulation_elapsed_s': (state['clock'] - clock_before) / 1e9,
            'odom_frame': state['odom'].header.frame_id,
            'child_frame': state['odom'].child_frame_id,
            'errors': errors,
        }
        print(json.dumps(result, indent=2, allow_nan=False))
        return 1 if errors else 0
    except (RuntimeError, KeyboardInterrupt) as error:
        print(json.dumps({'status': 'FAIL', 'errors': [str(error)]}, indent=2))
        return 1
    finally:
        if started_driving and rclpy.ok():
            # Allow DDS time to deliver the stop before destroying the publisher.
            for _ in range(5):
                publisher.publish(Twist())
                rclpy.spin_once(node, timeout_sec=0.1)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    raise SystemExit(main())
