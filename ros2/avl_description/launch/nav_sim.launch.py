"""Run Paarseus/IGVC_ROS2's navigation stack against the running sim.

Start the sim first (sim.launch.py, which also runs his EKFs + navsat).
This file mirrors his avros_bringup/launch/navigation.launch.py on Humble, minus
real-robot nodes (sensors, actuator_node, foxglove, autonomy_monitor):

  - Nav2 servers + lifecycle manager with his competition pair
    (config/igvc/nav2_params_igvc_autonav.yaml + navigate_igvc_autonav_2026.xml)
  - 3x avros_perception perception_node (camera lines -> semantic layer)
  - avros_perception lidar_preprocessor (LiDAR obstacles -> STVL)
  - avros_navigation mission_manager after 20 s, on config/igvc/waypoints_lap.yaml (full lap;
    waypoints_sim.yaml is the older half-lap set)

avros_perception, avros_navigation, and semantic_segmentation_layer
(Paarseus fork, branch avros-fixes) are not in this repo. Build them in a
separate workspace and source it before launching. STVL comes from apt
(ros-humble-spatio-temporal-voxel-layer). DDS: everything runs on the shell
default. Parsa forces CycloneDDS because mixing DDS layers corrupted goals, so
keep the sim and this launch on the same RMW.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    igvc = os.path.join(get_package_share_directory('avl_description'), 'config', 'igvc')
    perception_pkg = get_package_share_directory('avros_perception')
    perception_yaml = os.path.join(perception_pkg, 'config', 'perception.yaml')
    lidar_yaml = os.path.join(perception_pkg, 'config', 'lidar.yaml')
    bt_xml = os.path.join(igvc, 'navigate_igvc_autonav_2026.xml')

    nav2_params = RewrittenYaml(
        source_file=os.path.join(igvc, 'nav2_params_igvc_autonav.yaml'),
        param_rewrites={
            'use_sim_time': 'True',
            'default_nav_to_pose_bt_xml': bt_xml,
            'default_nav_through_poses_bt_xml': bt_xml,
            'graph_filepath': os.path.join(igvc, 'sim_route_graph.geojson'),
            # SIM-ONLY OVERRIDE (Ryan, 2026-11-09): feed all three ZEDs into the local costmap.
            # Parsa's file defines left/right sources ("single SemanticSegmentationLayer
            # instance with three ZED X sources") but lists only 'front', because his robot
            # runs only the front camera today. Global costmap is left as he has it.
            'local_costmap.local_costmap.ros__parameters.semantic_layer.observation_sources':
                'front left right',
        },
        convert_types=True,
    )

    # Same servers and order as Parsa's navigation.launch.py.
    nav2_servers = [
        ('nav2_controller', 'controller_server'),
        ('nav2_smoother', 'smoother_server'),
        ('nav2_planner', 'planner_server'),
        ('nav2_route', 'route_server'),
        ('nav2_behaviors', 'behavior_server'),
        ('nav2_velocity_smoother', 'velocity_smoother'),
        ('nav2_bt_navigator', 'bt_navigator'),
    ]
    sim_time = {'use_sim_time': True}

    # use_sim_time passed per node: RewrittenYaml only replaces keys that already exist,
    # and Parsa's params file has no use_sim_time keys, so the rewrite alone left the
    # servers on wall clock (goal stamps vs sim-time TF -> bogus "Reached the goal").
    nodes = [
        Node(package=pkg, executable=name, name=name, parameters=[nav2_params, sim_time],
             output='screen', respawn=True, respawn_delay=2.0)
        for pkg, name in nav2_servers
    ]
    nodes.append(Node(
        package='nav2_lifecycle_manager', executable='lifecycle_manager',
        name='lifecycle_manager_navigation', output='screen',
        parameters=[{'use_sim_time': True, 'autostart': True,
                     'node_names': [name for _, name in nav2_servers]}],
    ))
    # SIM-ONLY OVERRIDE (Ryan, 2026-11-09, option B): the side ZEDs are level stand-in mounts,
    # so Parsa's sooner25_band [0.40, 1.0] includes sky and drives the adaptive V ceiling to sky
    # brightness. [0.60, 1.0] matches his own sky_roi_poly (top 60% masked). Front camera keeps
    # his value. Remove once the real side-camera mounts are measured.
    side_override = {'sooner25_band': [0.60, 1.0]}
    nodes += [
        Node(package='avros_perception', executable='perception_node',
             name=f'perception_{cam}', output='screen',
             parameters=[perception_yaml, {'use_sim_time': True, 'camera_name': cam},
                         *([side_override] if cam != 'front' else [])])
        for cam in ('front', 'left', 'right')
    ]
    nodes.append(Node(
        package='avros_perception', executable='lidar_preprocessor',
        name='lidar_preprocessor', output='screen',
        parameters=[lidar_yaml, sim_time],
    ))
    nodes.append(TimerAction(
        period=20.0,
        actions=[Node(
            package='avros_navigation', executable='mission_manager',
            name='mission_manager', output='screen',
            parameters=[{'waypoints_file': os.path.join(igvc, 'waypoints_lap.yaml'),
                         'use_sim_time': True}],
        )],
        condition=IfCondition(LaunchConfiguration('mission')),
    ))

    return LaunchDescription([
        DeclareLaunchArgument('mission', default_value='true',
                              description='Start mission_manager (rover drives the waypoints).'),
        *nodes,
    ])
