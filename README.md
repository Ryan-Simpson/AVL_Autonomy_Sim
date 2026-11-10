# AVL Autonomy Sim

Cal Poly Pomona **Autonomous Vehicles Lab** autonomy simulator: **Gazebo first**, ROS 2 topic parity with the lab robots, **Isaac Sim optional** if time remains.

Same Jetson topic names so autonomy does not need a simulation-only fork. First platform is the IGVC tracked rover; more vehicles are packs, not a rename. Primary hinge code targets **C++** (`rclcpp` / Gazebo plugins).

This is **not** the Chrono student package (`avl_simulator`).

---

## Abstract

This work presents AVL Autonomy Sim, a digital twin platform for Cal Poly Pomona’s Autonomous Vehicles Lab. The twin is built so the same ROS 2 autonomy stack that runs on the lab’s Jetson computers can be developed in simulation before a field test. The primary backend is Gazebo with a C++ ROS 2 hinge; NVIDIA Isaac Sim is a time-permitting second backend on the **same frozen topic map**. The first vehicle pack is a roughly 49 kg differential tank-tread rover with a Velodyne VLP-16, three Stereolabs ZED X cameras, an Xsens MTi-680G with GNSS, and dual track encoders. The rover is modeled as a skid-steer vehicle with measured sensor mounts; tank belts are approximated rather than simulated as a full track-soil system. A thin ROS 2 bridge uses the physical robot’s topic names—commanding the tracks from `/cmd_vel` and publishing `/wheel_odom`, `/imu/data`, `/gnss`, `/velodyne_points`, and ZED image streams. The evaluation compares simulated VLP-16 point clouds to recordings from the real sensor on a repeatable course and reports range error, point density, and dropout. The goal is a closed-loop, honestly labeled twin of the lab’s tracked rover, not a photoreal campus reconstruction or a learned driving policy.

---

## Status (2026-11-09)

- MARVIN (the IGVC tracked rover) runs on the IGVC course in Gazebo Fortress with LiDAR, three ZED X cameras, IMU and GNSS.
- Paarseus/IGVC_ROS2 runs unchanged on top: dual EKF + navsat, Nav2 MPPI, STVL (LiDAR obstacles), semantic line layer (cameras), `mission_manager` (GPS waypoints).
- First full autonomous lap: 136 m, 41/48 waypoints reached (7 skipped, not yet explained), 0 barrels hit.
- **Sim-only:** the ZEDs are raised 1.0 m and the side ZEDs tilted 30° down (`zed_sim_raise`, `zed_side_pitch` in `tracked_rover.urdf.xacro`). Set both to 0 for the measured mounts.

Latest notes: [docs/context_meetings/2026-11-09-sensors-and-waypoint-nav.md](docs/context_meetings/2026-11-09-sensors-and-waypoint-nav.md)

## Quick start

Docker setup and troubleshooting: [docker/README.md](docker/README.md).

```bash
# host
cd docker && ./dev.sh build   # first time only
./dev.sh up                   # container avl-sim, repo at /ws/src/AVL_Autonomy_Sim

# in the container: build and launch the sim (Gazebo + EKFs + navsat)
cd /ws && colcon build --symlink-install && source install/setup.bash
ros2 launch avl_description sim.launch.py            # headless:=true for no window
```

Autonomous lap (second terminal, `./dev.sh shell`). It needs three packages that are not in this repo; build them in a separate workspace first:

| Package | Source |
|---|---|
| `avros_perception`, `avros_navigation` | `src/` of [Paarseus/IGVC_ROS2](https://github.com/Paarseus/IGVC_ROS2) |
| `semantic_segmentation_layer` | [Paarseus/semantic_segmentation_layer](https://github.com/Paarseus/semantic_segmentation_layer), branch `avros-fixes` |

```bash
source /ws/install/setup.bash && source <external_ws>/install/setup.bash
ros2 launch avl_description nav_sim.launch.py        # mission:=false brings up Nav2 without driving
```

`mission_manager` starts 20 s after Nav2 and drives `config/igvc/waypoints_lap.yaml`. If Nav2 hangs while configuring, restart only `nav_sim.launch.py`.

## Repo map

| Path | What |
|---|---|
| `ros2/avl_description/` | The one ROS 2 package: URDF, launch files, bridge, configs |
| `ros2/avl_description/config/marvin_v1.yaml` | Every mechanical number in the URDF |
| `ros2/avl_description/config/igvc/` | Parsa's configs (copied unchanged) + our sim waypoints. See its README |
| `ros2/topic_map/` | Topic contract (`topics.yaml`, provisional until Jetson confirmation) |
| `gazebo/worlds/igvc_course.sdf` | Default world. `hand_drawn_test.sdf`, `empty_course.sdf` are extras |
| `gazebo/models/` | IGVC course (Hosei Orange, Apache-2.0) and hand-drawn track |
| `assets/measurements.md` | Measurement authority |
| `docker/` | Container image and `dev.sh` |
| `docs/` | Design, plans, meeting notes |

## Build discipline

1. One closed loop on **Gazebo** with real topic names  
2. **Freeze** the topic map (`ros2/topic_map/`)  
3. Measure **VLP-16** sim-to-real  
4. **Isaac** only if time remains, on the same contract  

Design: [docs/design/2026-09-15-gazebo-first-design.md](docs/design/2026-09-15-gazebo-first-design.md)  
Plan: [docs/plans/2026-09-15-gazebo-first-closed-loop.md](docs/plans/2026-09-15-gazebo-first-closed-loop.md)

## Scope

| In | Out |
|----|-----|
| Gazebo vehicle packs (tracked rover first) | NVIDIA DRIVE Sim / world models |
| Jetson topic names (`/cmd_vel`, `/wheel_odom`, `/velodyne_points`, …) | Campus-scale Gaussian / NuRec reconstruction |
| C++ ROS 2 / Gazebo hinge | Replacing Chrono `avl_simulator` |
| VLP-16 sim-to-real (poster result) | Full Isaac feature parity in Fall 2026 |
| Isaac Sim as optional second backend | Perfect track–soil physics |

Fall 2026 deliverables: [docs/FALL_2026_BAHR_BRIEF.md](docs/FALL_2026_BAHR_BRIEF.md).  
Team context / notes (Drive + GitHub): [docs/context_meetings/](docs/context_meetings/).  
Isaac literature (Phase 4): [docs/ISAAC_RESEARCH_MAP.md](docs/ISAAC_RESEARCH_MAP.md).

## Requirements

- ROS 2 Humble  
- Gazebo Fortress (`ign gazebo`) + `ros-humble-ros-gz`  
- C++17 toolchain (`colcon`, `rclcpp`)  
- NVIDIA GPU + Container Toolkit for sensors and the GUI (see `docker/README.md`)  
- Isaac Sim on an RTX workstation — **optional**, after closed loop  
- Python only where launch/tooling or Isaac requires it  

## License

BSD-3-Clause. Cal Poly Pomona Autonomous Vehicles Lab.
