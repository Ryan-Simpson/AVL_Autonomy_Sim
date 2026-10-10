# MARVIN topic inventory

**status: names adopted from Paarseus/IGVC_ROS2**

The names in `topics.yaml` are the IGVC stack. This sheet is what still needs a live Jetson check: publisher, subscriber, rate, and QoS. Rates below are the numbers in that repo’s configs, not a `ros2 topic hz` on the robot.

## Topics to check

| Interface | Topic | Type | Rate in IGVC config | Frame | Live check |
|---|---|---|---|---|---|
| drive | `/cmd_vel` | `geometry_msgs/msg/Twist` | — | — | publisher, QoS |
| raw odom | `/wheel_odom` | `nav_msgs/msg/Odometry` | 50 Hz | `odom` → `base_link` | confirm child frame |
| filtered odom | `/odometry/filtered` | `nav_msgs/msg/Odometry` | EKF | `odom` → `base_link` | confirm this is the TF broadcaster |
| GPS meters | `/odometry/gps` | `nav_msgs/msg/Odometry` | navsat | — | confirm it is published |
| IMU | `/imu/data` | `sensor_msgs/msg/Imu` | 100 Hz | `imu_link` | QoS |
| GNSS | `/gnss` | `sensor_msgs/msg/NavSatFix` | — | `gps_link` | confirm, not `/gps/fix` |
| NMEA | `/nmea` | `nmea_msgs/msg/Sentence` | — | — | confirm remap |
| RTCM | `/rtcm` | `rtcm_msgs/msg/Message` | — | — | confirm remap |
| VLP-16 | `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | ~10 Hz | `velodyne` | QoS |
| front image | `/zed_front/zed_node/rgb/image_rect_color` | `sensor_msgs/msg/Image` | — | `zed_center_optical_frame` | confirm this path vs `rgb/color/rect/image` |
| front cloud | `/zed_front/zed_node/point_cloud/cloud_registered` | `sensor_msgs/msg/PointCloud2` | — | — | confirm |
| front VIO | `/zed_front/zed_node/odom` | `nav_msgs/msg/Odometry` | — | — | confirm |
| left image | `/zed_left/zed_node/rgb/image_rect_color` | `sensor_msgs/msg/Image` | — | `zed_left_optical_frame` | confirm |
| left cloud | `/zed_left/zed_node/point_cloud/cloud_registered` | `sensor_msgs/msg/PointCloud2` | — | — | confirm |
| left VIO | `/zed_left/zed_node/odom` | `nav_msgs/msg/Odometry` | — | — | confirm |
| right image | `/zed_right/zed_node/rgb/image_rect_color` | `sensor_msgs/msg/Image` | — | `zed_right_optical_frame` | confirm |
| right cloud | `/zed_right/zed_node/point_cloud/cloud_registered` | `sensor_msgs/msg/PointCloud2` | — | — | confirm |
| right VIO | `/zed_right/zed_node/odom` | `nav_msgs/msg/Odometry` | — | — | confirm |
| actuator state | `/avros/actuator_state` | `avros_msgs/msg/ActuatorState` | 20 Hz | — | confirm message package is built |
| actuator command | `/avros/actuator_command` | `avros_msgs/msg/ActuatorCommand` | — | — | confirm |
| wheel debug | `/avros/wheel_debug` | `avros_msgs/msg/WheelDebug` | — | — | confirm |
| mode | `/autonomous_mode` | `std_msgs/msg/Bool` | — | — | confirm |
| left/right RPM | none in that repo | — | Teensy internal | — | confirm they stay off ROS |

## What the IGVC repo actually uses

- Drive command is `/cmd_vel`.
- Two odometry topics: `/wheel_odom` from the tracks, `/odometry/filtered` from the local EKF.
- GPS fix is `/gnss`. Meters are `/odometry/gps`.
- IMU is `/imu/data`. Lidar is `/velodyne_points`.
- Cameras are `zed_front`, `zed_left`, and `zed_right` under `zed_node`.
- No separate ROS RPM topics.

## Checking it on the Jetson

With the normal MARVIN stack running, collect all 22 adopted interfaces in one
read-only pass from the repository root:

```bash
python3 tools/capture_jetson_inventory.py --output artifacts/jetson-inventory.json
```

This records endpoint/QoS information, bounded rate samples, available frame
headers, and odometry child frames. An absent topic is marked `seen=false`;
a timeout is preserved as a timeout, never filled in with an assumed value.
The default is eight seconds per command, so a complete pass may take several
minutes. Capture files stay outside version control. Review the observations
with Ryan before correcting the adopted contract or marking it frozen.

Start with the normal MARVIN stack running:

```bash
ros2 node list
ros2 topic list -t
```

For each topic we care about:

```bash
ros2 topic info -v <topic>
ros2 topic hz <topic>
```

For the frame ID:

```bash
ros2 topic echo <topic> --once --field header
```

And for odom:

```bash
ros2 topic echo <odom_topic> --once --field child_frame_id
```

That should give us everything Ryan asked for: the exact name, type, publisher, subscriber, rate, QoS, and frame.

## What a live echo still has to confirm

Names are already in `topics.yaml`. On the Jetson, confirm each one is actually up, and fill publisher, subscriber, rate, and QoS. The one name most likely to differ is the front RGB path (`image_rect_color` vs `rgb/color/rect/image`).
