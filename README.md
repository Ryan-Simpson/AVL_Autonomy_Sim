# AVL Autonomy Sim

Cal Poly Pomona **Autonomous Vehicles Lab** autonomy simulator in [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac/sim).

GPU-rendered vehicles and sensors, ROS 2 on the same topics as the lab robots. First platform is the IGVC tracked rover; more vehicles are packs, not a rename.

This is **not** the Chrono student package (`avl_simulator`).

---

## Abstract

This work presents AVL Autonomy Sim, a digital twin platform in NVIDIA Isaac Sim for Cal Poly Pomona’s Autonomous Vehicles Lab. The twin is built so the same ROS 2 autonomy stack that runs on the lab’s Jetson computers can be developed in a GPU-rendered environment before a field test. The first vehicle pack is a roughly 49 kg differential tank-tread rover with a Velodyne VLP-16, three Stereolabs ZED X cameras, an Xsens MTi-680G with GNSS, and dual track encoders. In Isaac Sim that rover is modeled as a skid-steer vehicle with measured sensor mounts; tank belts are approximated rather than simulated as a full track-soil system. A thin ROS 2 bridge uses the physical robot’s topic names—commanding left and right tracks from `/cmd_vel` or Teensy-style L/R RPM and publishing `/odom`, `/imu/data`, `/gps/fix`, `/velodyne_points`, and ZED image streams—so onboard software does not require a simulation-only fork. The evaluation compares simulated VLP-16 point clouds to recordings from the real sensor on a repeatable course and reports range error, point density, and dropout. The goal is a closed-loop, honestly labeled twin of the lab’s tracked rover, not a photoreal campus reconstruction or a learned driving policy.

---

## Scope

| In | Out |
|----|-----|
| Isaac Sim vehicle packs (tracked rover first) | NVIDIA DRIVE Sim / world models |
| Jetson topic names (`/cmd_vel`, `/odom`, `/velodyne_points`, …) | Campus-scale Gaussian / NuRec reconstruction |
| VLP-16 sim-to-real (poster result) | Replacing Chrono `avl_simulator` |

Fall 2026 deliverables: [docs/FALL_2026_BAHR_BRIEF.md](docs/FALL_2026_BAHR_BRIEF.md).  
Create the GitHub repo with [docs/GIT_PUSH.md](docs/GIT_PUSH.md).

## Layout

```
AVL_Autonomy_Sim/
├── assets/           # URDF / USD / meshes (no huge bags)
├── isaac/            # Isaac Sim scripts and extensions
├── ros2/             # Bridge and topic map
├── docs/
└── README.md
```

## Requirements (planned)

- Isaac Sim on an RTX workstation
- ROS 2 Humble
- Python 3.10+

## License

BSD-3-Clause. Cal Poly Pomona Autonomous Vehicles Lab.
