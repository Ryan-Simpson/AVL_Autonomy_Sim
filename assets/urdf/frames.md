# MARVIN frames

Frame names and who publishes them. The URDF is `ros2/avl_description/urdf/tracked_rover.urdf.xacro`. Numbers below are what that file uses today. Sensor mounts are IGVC stand-ins, not a tape measurement. `gps_link` sits on the roof of the main chassis, in line with the front camera.

`base_link` is on the ground. REP-103: x forward, y left, z up. `odom` → `base_link` is published by the diff-drive plugin only when Gazebo is running, so it is not a fixed joint in the URDF.

```text
odom                          (dynamic, Gazebo diff-drive)
└── base_link                 mass 49 kg
    ├── imu_link              xyz 0 0 0.5556
    ├── velodyne              xyz 0.089 0 0.7146
    ├── gps_link              xyz 0.6795 0 0.534    on the main-chassis roof, in line with the front camera
    ├── zed_left_link         xyz 0.098 0.286 0.6126    rpy 0 0 1.5708
    │   └── zed_left_optical_frame      rpy -1.5708 0 -1.5708
    ├── zed_center_link       xyz 0.6795 0 0.4476      rpy 0 0.2618 0
    │   └── zed_center_optical_frame    rpy -1.5708 0 -1.5708
    ├── zed_right_link        xyz 0.098 -0.286 0.6126   rpy 0 0 -1.5708
    │   └── zed_right_optical_frame     rpy -1.5708 0 -1.5708
    ├── left_rear_wheel       xyz -0.05 0.3653 0.0699   axis 0 1 0
    ├── left_front_wheel      xyz 0.55 0.3653 0.0699
    ├── right_rear_wheel      xyz -0.05 -0.3653 0.0699
    └── right_front_wheel     xyz 0.55 -0.3653 0.0699
```

`zed_center_link` is the forward camera. The IGVC file and [avros_cam_sim](https://github.com/cbmusonda/avros_cam_sim) call that camera `zed_front`. Optical frames are Z-forward children of the camera links. Wheel joints are continuous. Their transforms appear in TF only when joint states are published.

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
