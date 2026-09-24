# MARVIN topic inventory

**status: draft**

This is my Step 2.1 sheet for checking the real MARVIN Jetson. I left anything I could not prove as `TODO` instead of guessing from older code.

## Topics to check

| Interface | Topic | Type | Publisher | Subscriber(s) | Rate | QoS | Frame |
|---|---|---|---|---|---|---|---|
| drive | `/cmd_vel` | `geometry_msgs/msg/Twist` | TODO | TODO | TODO | TODO | — |
| left/right RPM | check if ROS topics exist | TODO | TODO | TODO | TODO | TODO | — |
| odom | `/odom` or whatever the Jetson actually uses | `nav_msgs/msg/Odometry` | TODO | TODO | TODO | TODO | `odom -> base_link` |
| IMU | `/imu/data` | `sensor_msgs/msg/Imu` | TODO | TODO | TODO | TODO | `imu_link` |
| GPS/GNSS | `/gps/fix` or `/gnss` | `sensor_msgs/msg/NavSatFix` | TODO | TODO | TODO | TODO | TODO |
| VLP-16 | `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | TODO | TODO | TODO | TODO | `velodyne` |
| ZED left image | exact live topic | `sensor_msgs/msg/Image` | TODO | TODO | TODO | TODO | optical frame |
| ZED left camera info | exact live topic | `sensor_msgs/msg/CameraInfo` | TODO | TODO | TODO | TODO | `zed_left_optical_frame` |
| ZED center image | exact live topic | `sensor_msgs/msg/Image` | TODO | TODO | TODO | TODO | optical frame |
| ZED center camera info | exact live topic | `sensor_msgs/msg/CameraInfo` | TODO | TODO | TODO | TODO | `zed_center_optical_frame` |
| ZED right image | exact live topic | `sensor_msgs/msg/Image` | TODO | TODO | TODO | TODO | optical frame |
| ZED right camera info | exact live topic | `sensor_msgs/msg/CameraInfo` | TODO | TODO | TODO | TODO | `zed_right_optical_frame` |
| wheel/joint state | check if the real robot publishes one | TODO | TODO | TODO | TODO | TODO | TODO |

## What I found so far

I checked a few of the existing public AVL / IGVC ROS repos so I would know what to look for on the Jetson.

- `/cmd_vel` is used by the existing control stack
- `/imu/data` is used for the Xsens
- `/velodyne_points` is used for the VLP-16
- GPS naming is mixed: the task sheet says `/gps/fix`, but other AVL code uses `/gnss`
- odom naming is mixed too: I found `/odom`, `/wheel_odom`, and filtered odometry topics in different stacks
- the Teensy firmware has left/right RPM internally, but I did not find separate ROS RPM topics yet
- the older camera setups do not all use the same ZED names, so I left those open instead of copying the wrong namespace

The main things I’d double-check first on the real Jetson are the GPS topic, the odom topic the autonomy stack actually uses, and whether left/right RPM ever exists as ROS topics.

## Checking it on the Jetson

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

## Before this gets frozen

I’d only call the inventory done once:

- the command and odom topics are confirmed
- IMU, GPS/GNSS, and VLP-16 are confirmed
- all three ZED image + camera_info topics are filled in
- RPM and wheel/joint-state topics are either filled in or confirmed not to exist
- publisher/subscriber names, rates, QoS, and frames are filled in

Then Ryan can copy the final values into `topics.yaml` and freeze version 1.
