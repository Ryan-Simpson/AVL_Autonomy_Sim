# MARVIN frames

This is the frame layout for MARVIN in the sim. The actual sensor positions still come from `assets/measurements.md` — I’m only defining the frame names and who should publish each transform here.

```text
odom
└── base_link
    ├── velodyne
    ├── imu_link
    ├── gps_link
    ├── zed_left_link
    │   └── zed_left_optical_frame
    ├── zed_center_link
    │   └── zed_center_optical_frame
    └── zed_right_link
        └── zed_right_optical_frame
```

## Who publishes what

| Transform | Type | Publisher |
|---|---|---|
| `odom -> base_link` | dynamic | Gazebo diff-drive |
| `base_link -> velodyne` | fixed | `robot_state_publisher` |
| `base_link -> imu_link` | fixed | `robot_state_publisher` |
| `base_link -> gps_link` | fixed | `robot_state_publisher` |
| `base_link -> zed_left_link` | fixed | `robot_state_publisher` |
| `base_link -> zed_center_link` | fixed | `robot_state_publisher` |
| `base_link -> zed_right_link` | fixed | `robot_state_publisher` |
| each ZED link -> its optical frame | fixed | `robot_state_publisher` |

A few things I want to keep consistent:

- there should only be one `base_link`
- Gazebo should be the only thing publishing `odom -> base_link`
- sensor `xyz` / `rpy` values should come from `assets/measurements.md`
- if Ryan has not measured a mount yet, leave it at `0 0 0` and mark it `TODO measure`
- the ZED optical frames stay separate from the camera links and point Z forward

## Quick checks

Once the description package is ready:

```bash
ros2 launch avl_description display.launch.py
ros2 run tf2_ros tf2_echo base_link velodyne
```

Once Gazebo is running:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

For that last check, there should only be one broadcaster for `odom -> base_link`.
