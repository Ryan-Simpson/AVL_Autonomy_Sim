"""Spawn the tracked rover on the IGVC course, the default sim world.

Also runs Paarseus/IGVC_ROS2's localization (dual EKF + navsat_transform) with his
config files (config/igvc/, copied unchanged) and his remaps from
avros_bringup/launch/localization.launch.py. The odom EKF is the only
odom -> base_link publisher; bridge.yaml does not bridge the diff-drive /tf.

headless:=true runs the Gazebo server only, rendering sensors through EGL
(--headless-rendering) so no X display is needed.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory('avl_description')
    xacro_path = os.path.join(pkg, 'urdf', 'tracked_rover.urdf.xacro')
    world = os.path.join(pkg, 'worlds', 'igvc_course.sdf')
    models = os.path.join(pkg, 'models')
    bridge_yaml = os.path.join(pkg, 'config', 'bridge.yaml')
    sim_params = os.path.join(pkg, 'config', 'sim_params.yaml')
    ekf_yaml = os.path.join(pkg, 'config', 'igvc', 'ekf.yaml')
    navsat_yaml = os.path.join(pkg, 'config', 'igvc', 'navsat.yaml')
    resource_path = os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')
    if resource_path:
        resource_path = models + ':' + resource_path
    else:
        resource_path = models

    robot_description = ParameterValue(
        Command(['xacro ', xacro_path, ' model:=', LaunchConfiguration('model')]), value_type=str)

    gz_launch = os.path.join(
        get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch),
        launch_arguments={'gz_args': ['-r ', world]}.items(),
        condition=UnlessCondition(LaunchConfiguration('headless')),
    )
    gz_sim_headless = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch),
        launch_arguments={'gz_args': ['-s -r --headless-rendering ', world]}.items(),
        condition=IfCondition(LaunchConfiguration('headless')),
    )

    sim_time = {'use_sim_time': True}

    return LaunchDescription([
        DeclareLaunchArgument('model', default_value='v1'),
        DeclareLaunchArgument('headless', default_value='false'),
        SetEnvironmentVariable('IGN_GAZEBO_RESOURCE_PATH', resource_path),
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', resource_path),
        gz_sim,
        gz_sim_headless,
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                sim_params,
                {'robot_description': robot_description},
            ],
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-world', 'igvc_course',
                '-name', 'tracked_rover',
                '-topic', 'robot_description',
                # South-lane centerline, facing east (down-course) so the waypoints
                # in config/igvc/waypoints_sim.yaml are ahead (Parsa: vx_min 0, keep goals ahead).
                '-x', '0',
                '-y', '0.1',
                '-z', '0.05',
                '-Y', '0',
            ],
            output='screen',
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{'config_file': bridge_yaml}],
            output='screen',
        ),
        # Paarseus/IGVC_ROS2 localization.launch.py nodes, same names and remaps.
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_odom',
            parameters=[ekf_yaml, sim_time],
            remappings=[('odometry/filtered', '/odometry/filtered')],
            output='screen',
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_map',
            parameters=[ekf_yaml, sim_time],
            remappings=[('odometry/filtered', '/odometry/global')],
            output='screen',
        ),
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform',
            parameters=[navsat_yaml, sim_time],
            remappings=[
                ('imu/data', '/imu/data'),
                ('gps/fix', '/gnss'),
                ('gps/filtered', '/gps/filtered'),
                ('odometry/gps', '/odometry/gps'),
                ('odometry/filtered', '/odometry/global'),
            ],
            output='screen',
        ),
    ])
