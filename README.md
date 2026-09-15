# AVL Autonomy Sim

Cal Poly Pomona **Autonomous Vehicles Lab** autonomy simulator: **Gazebo first**, ROS 2 topic parity with the lab robots, **Isaac Sim optional** if time remains.

Same Jetson topic names so autonomy does not need a simulation-only fork. First platform is the IGVC tracked rover; more vehicles are packs, not a rename. Primary hinge code targets **C++** (`rclcpp` / Gazebo plugins).

This is **not** the Chrono student package (`avl_simulator`).

---

## Abstract

This work presents AVL Autonomy Sim, a digital twin platform for Cal Poly Pomona’s Autonomous Vehicles Lab. The twin is built so the same ROS 2 autonomy stack that runs on the lab’s Jetson computers can be developed in simulation before a field test. The primary backend is Gazebo with a C++ ROS 2 hinge; NVIDIA Isaac Sim is a time-permitting second backend on the **same frozen topic map**. The first vehicle pack is a roughly 49 kg differential tank-tread rover with a Velodyne VLP-16, three Stereolabs ZED X cameras, an Xsens MTi-680G with GNSS, and dual track encoders. The rover is modeled as a skid-steer vehicle with measured sensor mounts; tank belts are approximated rather than simulated as a full track-soil system. A thin ROS 2 bridge uses the physical robot’s topic names—commanding left and right tracks from `/cmd_vel` or Teensy-style L/R RPM and publishing `/odom`, `/imu/data`, `/gps/fix`, `/velodyne_points`, and ZED image streams. The evaluation compares simulated VLP-16 point clouds to recordings from the real sensor on a repeatable course and reports range error, point density, and dropout. The goal is a closed-loop, honestly labeled twin of the lab’s tracked rover, not a photoreal campus reconstruction or a learned driving policy.

---

## Build discipline

1. One closed loop on **Gazebo** with real topic names  
2. **Freeze** the topic map (`ros2/topic_map/`)  
3. Measure **VLP-16** sim-to-real  
4. **Isaac** only if time remains, on the same contract  

Design: [docs/superpowers/specs/2026-09-15-gazebo-first-design.md](docs/superpowers/specs/2026-09-15-gazebo-first-design.md)  
Plan: [docs/superpowers/plans/2026-09-15-gazebo-first-closed-loop.md](docs/superpowers/plans/2026-09-15-gazebo-first-closed-loop.md)

## Scope

| In | Out |
|----|-----|
| Gazebo vehicle packs (tracked rover first) | NVIDIA DRIVE Sim / world models |
| Jetson topic names (`/cmd_vel`, `/odom`, `/velodyne_points`, …) | Campus-scale Gaussian / NuRec reconstruction |
| C++ ROS 2 / Gazebo hinge | Replacing Chrono `avl_simulator` |
| VLP-16 sim-to-real (poster result) | Full Isaac feature parity in Fall 2026 |
| Isaac Sim as optional second backend | Perfect track–soil physics |

Fall 2026 deliverables: [docs/FALL_2026_BAHR_BRIEF.md](docs/FALL_2026_BAHR_BRIEF.md).  
Isaac literature (Phase 4): [docs/ISAAC_RESEARCH_MAP.md](docs/ISAAC_RESEARCH_MAP.md).  
GitHub push steps: [docs/GIT_PUSH.md](docs/GIT_PUSH.md).

## Layout

```
AVL_Autonomy_Sim/
├── assets/           # URDF / meshes (USD when Isaac starts)
├── gazebo/           # Worlds, models, plugins (primary backend)
├── isaac/            # Optional Phase 4
├── ros2/             # Bridge packages + topic_map
├── docs/
└── README.md
```

## Requirements (planned)

- ROS 2 Humble  
- Gazebo (Harmonic via `ros_gz` preferred)  
- C++17 toolchain (`colcon`, `rclcpp`)  
- Isaac Sim on an RTX workstation — **optional**, after closed loop  
- Python only where launch/tooling or Isaac requires it  

## License

BSD-3-Clause. Cal Poly Pomona Autonomous Vehicles Lab.
