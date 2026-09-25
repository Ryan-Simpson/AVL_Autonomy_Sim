"""Spawn the tracked rover into Gazebo Sim on a flat ground plane."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory('avl_description')
    xacro_path = os.path.join(pkg, 'urdf', 'tracked_rover.urdf.xacro')
    world = os.path.join(pkg, 'worlds', 'empty_course.sdf')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_path]), value_type=str)

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': ['-r ', world],
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        gz_sim,
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': LaunchConfiguration('use_sim_time'),
            }],
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-world', 'empty_course',
                '-name', 'tracked_rover',
                '-topic', 'robot_description',
                '-z', '0.05',
            ],
            output='screen',
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/model/tracked_rover/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            ],
            output='screen',
        ),
        # IGVC teleop publishes /cmd_vel. Diff-drive listens on the model topic.
        ExecuteProcess(
            cmd=['/usr/bin/python3.12', '-c',
                 'import rclpy\n'
                 'from geometry_msgs.msg import Twist\n'
                 'rclpy.init()\n'
                 'n = rclpy.create_node("cmd_vel_relay")\n'
                 'p = n.create_publisher(Twist, "/model/tracked_rover/cmd_vel", 10)\n'
                 'n.create_subscription(Twist, "/cmd_vel", lambda m: p.publish(m), 10)\n'
                 'rclpy.spin(n)\n'],
            output='screen',
        ),
    ])
