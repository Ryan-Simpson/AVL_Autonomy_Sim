# MARVIN simulation interface status

Names and types below come from the adopted `ros2/topic_map/topics.yaml`.
Live publishers, subscribers, rates and QoS still need a Jetson capture.

| Hardware / system | Simulator status | Adopted ROS interface |
|---|---|---|
| Track drive / encoders | Stock Fortress DiffDrive, raw odometry bridge | `/cmd_vel` in; `/wheel_odom` out |
| Local EKF | External; not launched here | `/odometry/filtered`; owns `odom -> base_link` when enabled |
| Simulation time | World clock bridge | `/clock` |
| Xsens IMU | Mount frame exists; no sensor output implemented | `/imu/data`, frame `imu_link` |
| Xsens GNSS | Mount frame exists; no GNSS output implemented | `/gnss`, frame `gps_link` |
| GPS localization / corrections | External; not launched here | `/odometry/gps`, `/nmea`, `/rtcm` |
| Velodyne VLP-16 | Mount frame exists; no scan/cloud output implemented | `/velodyne_points`, frame `velodyne` |
| Front ZED | Frames exist; no image/cloud/VIO output implemented | `/zed_front/zed_node/...`; URDF `zed_center_link` |
| Left / right ZED | Frames exist; no image/cloud/VIO output implemented | `/zed_left/zed_node/...`, `/zed_right/zed_node/...` |
| Teensy actuator status / control | Custom message emulation not implemented | `/avros/actuator_state`, `/avros/actuator_command`, `/avros/wheel_debug`, `/autonomous_mode` |

The full camera names and types remain in the topic contract. The front RGB
path is still a live-check item: `rgb/image_rect_color` versus
`rgb/color/rect/image`. Keep the front namespace and mount frame distinct.
There are no separate ROS left/right RPM topics in the adopted stack.

Next lab-dependent steps:

1. Run `tools/capture_jetson_inventory.py` with MARVIN's usual stack active.
2. Review endpoints, QoS, image paths and TF ownership with Ryan; update only
   confirmed differences. Preserve absent and unobserved values as unknown.
3. Run the Fortress check in `SMOKE_TEST.md` on the shared environment.
4. Add sensor outputs using Ryan's approved mount values, then integrate the
   normal localization/autonomy launch with simulation time and a single TF owner.

Mounts and chassis dimensions remain the existing labeled stand-ins in
`assets/measurements.md`. No new measurements or real sensor observations are claimed.
