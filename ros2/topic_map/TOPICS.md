# Topic map

**Status:** adopted from [Paarseus/IGVC_ROS2](https://github.com/Paarseus/IGVC_ROS2). These are the names in that repo’s launch and config files. A live Jetson echo can still correct one name; do not invent a second set.

## Rules

1. The IGVC stack name is the name the sim publishes or subscribes.
2. `/gnss` is the GPS fix. `/gps/fix` is not the contract.
3. Raw track odometry is `/wheel_odom`. The pose the planner uses is `/odometry/filtered`.
4. There is no separate ROS topic for left and right RPM. Those stay inside the Teensy.
5. The front camera namespace is `zed_front`. The URDF link for that camera is `zed_center_link`.

## Files

- `topics.yaml` — machine-readable contract for bridges and launch
- `INVENTORY.md` — same names, plus what still needs a live rate, QoS, and publisher check

## Contract

| Topic | Type | Direction from the sim |
|-------|------|------------------------|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | subscribe |
| `/wheel_odom` | `nav_msgs/msg/Odometry` | publish |
| `/odometry/filtered` | `nav_msgs/msg/Odometry` | publish |
| `/odometry/gps` | `nav_msgs/msg/Odometry` | publish |
| `/imu/data` | `sensor_msgs/msg/Imu` | publish |
| `/gnss` | `sensor_msgs/msg/NavSatFix` | publish |
| `/nmea` | `nmea_msgs/msg/Sentence` | publish |
| `/rtcm` | `rtcm_msgs/msg/Message` | publish |
| `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | publish |
| `/zed_front/zed_node/rgb/image_rect_color` | `sensor_msgs/msg/Image` | publish |
| `/zed_front/zed_node/point_cloud/cloud_registered` | `sensor_msgs/msg/PointCloud2` | publish |
| `/zed_front/zed_node/odom` | `nav_msgs/msg/Odometry` | publish |
| `/zed_left/zed_node/rgb/image_rect_color` | `sensor_msgs/msg/Image` | publish |
| `/zed_left/zed_node/point_cloud/cloud_registered` | `sensor_msgs/msg/PointCloud2` | publish |
| `/zed_left/zed_node/odom` | `nav_msgs/msg/Odometry` | publish |
| `/zed_right/zed_node/rgb/image_rect_color` | `sensor_msgs/msg/Image` | publish |
| `/zed_right/zed_node/point_cloud/cloud_registered` | `sensor_msgs/msg/PointCloud2` | publish |
| `/zed_right/zed_node/odom` | `nav_msgs/msg/Odometry` | publish |
| `/avros/actuator_state` | `avros_msgs/msg/ActuatorState` | publish |
| `/avros/actuator_command` | `avros_msgs/msg/ActuatorCommand` | subscribe |
| `/avros/wheel_debug` | `avros_msgs/msg/WheelDebug` | publish |
| `/autonomous_mode` | `std_msgs/msg/Bool` | subscribe |

## Course world

The default world is `gazebo/worlds/igvc_course.sdf`. It loads the Hosei Orange IGVC model in `gazebo/models/orange_igvc` (Apache-2.0). The rover spawns at `0 1 0.05`, facing up the course. `empty_course.sdf` is only the old flat ground.
