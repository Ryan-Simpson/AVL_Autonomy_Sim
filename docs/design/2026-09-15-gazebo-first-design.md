# AVL Autonomy Sim — Gazebo-First Design

**Date:** 2026-09-15  
**Status:** Approved direction for team start  
**Product:** AVL Autonomy Sim (Cal Poly Pomona AVL)

## Problem

The GitHub repo was framed as an Isaac-only twin. The team needs a runnable closed-loop sim sooner, stronger C++/ROS practice, and a Fall poster result — without abandoning Isaac if time remains.

## Goals (all three)

1. **Closed-loop topic parity** — autonomy code talks to sim on the same ROS 2 topics as the Jetson robot (no sim-only fork).
2. **VLP-16 sim-to-real poster number** — range error / density / dropout on a repeatable course vs a real bag.
3. **Solid C++ / Gazebo reps** — `rclcpp` nodes and Gazebo C++ plugins as the primary implementation language for the sim hinge.

## Non-goals

- Replacing Chrono `avl_simulator`
- Campus-scale photoreal / NuRec / DRIVE Sim
- Perfect track–soil physics
- Full Isaac + Gazebo feature parity in Fall 2026
- Inventing a permanent “sim-only” topic namespace

## Discipline (build order)

1. One closed loop on **Gazebo** with real topic names  
2. **Freeze** the topic map  
3. Measure **VLP-16** sim-to-real  
4. **Isaac optional** on the same frozen contract  

## Architecture

```
                    ┌─────────────────────────┐
                    │  Autonomy stack (Jetson │
                    │  or laptop)             │
                    │  same topic names       │
                    └───────────┬─────────────┘
                                │ ROS 2
                    ┌───────────▼─────────────┐
                    │  Frozen topic map       │
                    │  (ros2/topic_map/)      │
                    └───────────┬─────────────┘
              ┌─────────────────┼─────────────────┐
              │                                   │
    ┌─────────▼─────────┐             ┌───────────▼─────────┐
    │ Gazebo primary    │             │ Isaac optional      │
    │ gazebo/ + C++     │             │ isaac/ (later)      │
    │ plugins / ros_gz  │             │ same topics         │
    └─────────┬─────────┘             └───────────┬─────────┘
              │                                   │
              └────────────┬──────────────────────┘
                           ▼
                 assets/ (URDF first; USD later)
```

**Stable product:** the ROS 2 topic contract + tracked-rover vehicle pack.  
**Backends:** Gazebo (required for Fall), Isaac (time-permitting).

### Language split

| Layer | Language | Why |
|-------|----------|-----|
| Gazebo plugins, drive/odom hinge, LiDAR eval tools | C++ (`rclcpp`, gz plugins) | Mastery + Jetson-transferable |
| Launch, params, topic map YAML | YAML / Python launch as needed | ROS convention |
| Isaac authoring (if reached) | Python / USD | Isaac ecosystem reality |

### Topic map rule

- Jetson names win where they already exist (semi-written stack).
- Gaps are added once, documented in `ros2/topic_map/`, then frozen.
- No long-lived sim-only aliases unless also present on the robot.

### Seed topic list (from current abstract; inventory may override)

| Direction | Topics |
|-----------|--------|
| Cmd in | `/cmd_vel` and/or Teensy-style L/R RPM |
| State out | `/odom`, `/imu/data`, `/gps/fix` |
| Sensors out | `/velodyne_points`, ZED image streams |

Freeze only after team inventory of the semi-written Jetson stack.

## Vehicle pack (first)

IGVC tracked rover (~49 kg), skid-steer approximation of tank belts, measured sensor mounts:

- Velodyne VLP-16  
- Stereolabs ZED X ×3 (pipeline later; LiDAR first for poster)  
- Xsens MTi-680G + GNSS  
- Dual track encoders  

## Evaluation

Repeatable course. Compare Gazebo VLP-16 clouds to real recordings: range error, point density, dropout. Honestly labeled — geometric fidelity, not photoreal RTX.

## Repo layout (target)

```
AVL_Autonomy_Sim/
├── assets/           # URDF / meshes first; USD when Isaac starts
├── gazebo/           # Worlds, models, C++ plugins (primary backend)
├── isaac/            # Optional Phase 4
├── ros2/             # Bridge packages, topic_map, launch
├── docs/
│   ├── FALL_2026_BAHR_BRIEF.md
│   ├── ISAAC_RESEARCH_MAP.md
│   ├── context_meetings/
│   ├── design/
│   └── plans/
└── README.md
```

## Success criteria (Fall)

| ID | Criterion |
|----|-----------|
| S1 | `/cmd_vel` (or L/R RPM) drives rover in Gazebo; `/odom` (and agreed sensors) publish under frozen names |
| S2 | Topic map file committed and marked frozen |
| S3 | Poster figure: Gazebo vs bag VLP-16 metrics |
| S4 | Primary hinge code in C++ |
| S5 | Isaac only if S1–S3 done |

## Relationship to prior work

- This repo is the team trunk.  
- `avl_simulator` / Chrono and older `AVLsim` / `marvin_isaac` trees are reference only, not the product.
