"""Spawn the tracked rover on the IGVC course, the default sim world."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory('avl_description')
    xacro_path = os.path.join(pkg, 'urdf', 'tracked_rover.urdf.xacro')
    world = os.path.join(pkg, 'worlds', 'igvc_course.sdf')
    models = os.path.join(pkg, 'models')
    resource_path = os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    if resource_path:
        resource_path = models + ':' + resource_path
    else:
        resource_path = models

    robot_description = ParameterValue(
        Command(['xacro ', xacro_path]), value_type=str)
    server_flag = PythonExpression([
        "'' if '", LaunchConfiguration('gui'), "' == 'true' else '-s '"])

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': ['-r ', server_flag, world],
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('gui', default_value='true', choices=['true', 'false']),
        DeclareLaunchArgument(
            'publish_odom_tf', default_value='true', choices=['true', 'false'],
            description='Disable when the local EKF owns odom -> base_link.'),
        SetEnvironmentVariable('IGN_GAZEBO_RESOURCE_PATH', resource_path),
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', resource_path),
        gz_sim,
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': ParameterValue(
                    LaunchConfiguration('use_sim_time'), value_type=bool),
            }],
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-world', 'igvc_course',
                '-name', 'tracked_rover',
                '-topic', 'robot_description',
                '-x', '0',
                '-y', '1',
                '-z', '0.05',
                '-Y', '1.5708',
            ],
            output='screen',
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='gazebo_bridge',
            parameters=[{'config_file': os.path.join(pkg, 'config', 'bridge.yaml')}],
            output='screen',
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='gazebo_odom_tf_bridge',
            condition=IfCondition(LaunchConfiguration('publish_odom_tf')),
            arguments=[
                '/model/tracked_rover/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            ],
            remappings=[('/model/tracked_rover/tf', '/tf')],
            output='screen',
        ),
    ])
