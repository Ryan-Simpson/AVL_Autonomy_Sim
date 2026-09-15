# Gazebo-First Closed Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up AVL Autonomy Sim as a Gazebo-primary, C++-heavy ROS 2 twin with frozen Jetson topic names, a VLP-16 sim-to-real poster path, and Isaac deferred until the closed loop works.

**Architecture:** ROS 2 topic contract is the product; Gazebo is the required backend; Isaac is optional on the same contract. Vehicle pack is the IGVC tracked rover (skid-steer approximation). Primary code in `rclcpp` / Gazebo C++ plugins.

**Tech Stack:** ROS 2 Humble, Gazebo (Harmonic preferred with Humble via `ros_gz`), C++17, `rclcpp`, `sensor_msgs` / `nav_msgs` / `geometry_msgs`, URDF/xacro, optional Isaac Sim later.

**Spec:** [docs/superpowers/specs/2026-09-15-gazebo-first-design.md](../specs/2026-09-15-gazebo-first-design.md)

## Global Constraints

- Build order: Gazebo closed loop → freeze topic map → VLP-16 eval → Isaac optional.
- Jetson topic names win; no long-lived sim-only aliases.
- Do not replace Chrono `avl_simulator`; do not commit bags, `.env`, or huge meshes without LFS decision.
- C++ for plugins, bridge/hinge nodes, and LiDAR eval tools; YAML for topic map and params.
- Tracks are skid-steer approximated, not full track–soil.

---

### Task 1: Repo reframe (docs + layout)

**Files:**
- Modify: `README.md`
- Modify: `docs/FALL_2026_BAHR_BRIEF.md`
- Modify: `.gitignore`
- Create: `gazebo/.gitkeep` (if missing)
- Create: `ros2/topic_map/TOPICS.md`
- Create: `ros2/topic_map/topics.yaml`
- Keep: `isaac/` as Phase 4 stub

**Interfaces:**
- Consumes: design spec goals and discipline
- Produces: public repo story = Gazebo primary / Isaac optional; empty topic map schema for Task 2

- [ ] **Step 1: Rewrite README abstract and scope** for Gazebo-first + frozen topic contract + C++ hinge; keep vehicle/sensor list and “not Chrono” line.

- [ ] **Step 2: Update Fall brief** deliverables to D1 Gazebo closed loop, D2 topic map freeze, D3 VLP-16 figure, D4 poster, D5 paper; Isaac as stretch.

- [ ] **Step 3: Extend `.gitignore`** for `build/`, `install/`, `log/`, `*.pcd`, Gazebo cache, `compile_commands.json`.

- [ ] **Step 4: Add topic map stubs**

Create `ros2/topic_map/topics.yaml`:

```yaml
# STATUS: draft — freeze only after Jetson inventory (Task 2)
version: 0
status: draft
frame_ids:
  map: map
  odom: odom
  base_link: base_link
topics:
  cmd_vel:
    name: /cmd_vel
    type: geometry_msgs/msg/Twist
    direction: subscribe  # sim subscribes; autonomy publishes
  odom:
    name: /odom
    type: nav_msgs/msg/Odometry
    direction: publish
  imu:
    name: /imu/data
    type: sensor_msgs/msg/Imu
    direction: publish
  gps:
    name: /gps/fix
    type: sensor_msgs/msg/NavSatFix
    direction: publish
  lidar:
    name: /velodyne_points
    type: sensor_msgs/msg/PointCloud2
    direction: publish
```

Create `ros2/topic_map/TOPICS.md` explaining draft vs frozen and Jetson-wins rule.

- [ ] **Step 5: Commit**

```bash
git add README.md docs/FALL_2026_BAHR_BRIEF.md .gitignore gazebo ros2/topic_map docs/superpowers
git commit -m "$(cat <<'EOF'
 reframes AVL Autonomy Sim as Gazebo-first with Isaac optional.

Aligns README and Fall brief with closed-loop topic parity, C++ hinge,
and VLP-16 eval; adds topic map stubs for team inventory.
EOF
)"
```

---

### Task 2: Inventory and freeze the topic map

**Files:**
- Modify: `ros2/topic_map/topics.yaml`
- Modify: `ros2/topic_map/TOPICS.md`
- Create: `ros2/topic_map/INVENTORY.md` (sources: Jetson packages, bags notes, whiteboard)

**Interfaces:**
- Consumes: draft topics.yaml seed list
- Produces: `status: frozen` topics.yaml that all later packages must match exactly

- [ ] **Step 1: Team dumps every known Jetson pub/sub** into `INVENTORY.md` (node name, topic, type, who owns it). Mark unknowns as `unknown`.

- [ ] **Step 2: Diff inventory vs seed YAML.** Jetson name wins on conflict. Add missing required topics for closed loop (`cmd` + `odom` minimum; `imu`/`gps`/`velodyne_points` for poster path).

- [ ] **Step 3: Set `status: frozen` and `version: 1`** in `topics.yaml`. Update `TOPICS.md` with freeze date and rule: PRs that rename frozen topics require brief owner approval.

- [ ] **Step 4: Commit**

```bash
git add ros2/topic_map
git commit -m "$(cat <<'EOF'
freeze ROS 2 topic map after Jetson inventory.

Locks Jetson-aligned names so Gazebo and later Isaac backends share one contract.
EOF
)"
```

---

### Task 3: Minimal URDF vehicle pack (skid-steer)

**Files:**
- Create: `assets/urdf/tracked_rover.urdf.xacro`
- Create: `assets/urdf/sensors.xacro` (VLP-16 mount link + optical frames stubs)
- Create: `assets/urdf/README.md` (units, source of mount measurements)
- Create: `ros2/src/avl_description/` (package wrapping URDF for `robot_state_publisher`)

**Interfaces:**
- Consumes: frozen `base_link` / sensor frame names from topics.yaml
- Produces: spawnable URDF with left/right wheel (or track proxy) joints for Gazebo differential drive

- [ ] **Step 1: Create `avl_description` package** with `package.xml` / `CMakeLists.txt` installing `urdf/` and `launch/`.

- [ ] **Step 2: Author xacro** with `base_link`, chassis inertia placeholder, two driven wheels (track proxy), caster or skid contacts as needed for Gazebo, and a `velodyne` link at measured height/offset (placeholders OK if labeled `TODO measure`).

- [ ] **Step 3: Launch check**

```bash
ros2 launch avl_description display.launch.py
# or: ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro ...)"
```

Expected: TF tree publishes `base_link` → `velodyne` without errors.

- [ ] **Step 4: Commit**

```bash
git add assets/urdf ros2/src/avl_description
git commit -m "$(cat <<'EOF'
add tracked rover URDF pack with VLP-16 mount frame.

Skid-steer wheel proxy for Gazebo; mounts documented for later measurement fill-in.
EOF
)"
```

---

### Task 4: Gazebo world + differential drive closed loop

**Files:**
- Create: `gazebo/worlds/empty_course.sdf`
- Create: `gazebo/models/tracked_rover/` (or spawn from URDF via ros_gz)
- Create: `ros2/src/avl_gazebo_bringup/` (launch: Gazebo + spawn + bridges)
- Create: `ros2/src/avl_gazebo_plugins/` only if stock diff-drive is insufficient

**Interfaces:**
- Consumes: URDF from Task 3; topic names from frozen `topics.yaml`
- Produces: `/cmd_vel` → motion; `/odom` out under frozen names

- [ ] **Step 1: Empty world SDF** with flat ground and a simple course marker (cones or painted line boxes) for later LiDAR eval.

- [ ] **Step 2: Bringup launch** that starts Gazebo, spawns rover, starts `ros_gz_bridge` parameter_bridge mappings from `topics.yaml` (`cmd_vel`, `odom`; clock if needed).

Example bridge param sketch (adjust to exact Humble/Harmonic syntax):

```yaml
- ros_topic_name: "/cmd_vel"
  gz_topic_name: "/model/tracked_rover/cmd_vel"
  ros_type_name: "geometry_msgs/msg/Twist"
  gz_type_name: "gz.msgs.Twist"
  direction: ROS_TO_GZ
- ros_topic_name: "/odom"
  gz_topic_name: "/model/tracked_rover/odometry"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS
```

- [ ] **Step 3: Manual drive test**

```bash
ros2 launch avl_gazebo_bringup sim.launch.py
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}, angular: {z: 0.2}}" -r 10
ros2 topic echo /odom --once
```

Expected: pose changes; no topic rename hacks.

- [ ] **Step 4: Commit**

```bash
git add gazebo ros2/src/avl_gazebo_bringup
git commit -m "$(cat <<'EOF'
add Gazebo bringup with cmd_vel to odom closed loop.

Uses frozen topic names so autonomy can drive the skid-steer rover unchanged.
EOF
)"
```

---

### Task 5: C++ hinge node (Teensy L/R RPM path optional)

**Files:**
- Create: `ros2/src/avl_sim_bridge/` (`rclcpp` package)
- Create: `ros2/src/avl_sim_bridge/src/cmd_mux.cpp`
- Create: `ros2/src/avl_sim_bridge/src/topic_map_loader.cpp` (optional; or codegen from YAML at build time)
- Test: `ros2/src/avl_sim_bridge/test/test_cmd_mux.cpp`

**Interfaces:**
- Consumes: frozen `/cmd_vel` and optional L/R RPM topics from `topics.yaml`
- Produces: single command stream to Gazebo drive plugin; documents which path Jetson uses

- [ ] **Step 1: Write failing test** for mux priority (e.g. RPM overrides Twist when both present, or the inverse — pick one rule and lock it in TOPICS.md).

```cpp
TEST(CmdMux, TwistOnlyPassesThrough) {
  CmdMux mux;
  auto out = mux.updateTwist(/*vx=*/0.5, /*wz=*/0.1);
  EXPECT_NEAR(out.left_wheel_rad_s, /*expected from track width*/, 1e-3);
}
```

- [ ] **Step 2: Run test — expect fail** (class missing).

```bash
cd ros2 && colcon build --packages-select avl_sim_bridge --cmake-args -DBUILD_TESTING=ON
colcon test --packages-select avl_sim_bridge
```

- [ ] **Step 3: Implement minimal `CmdMux` + `rclcpp` node** subscribing frozen command topics, publishing what Gazebo expects (or calling plugin interface).

- [ ] **Step 4: Run tests — expect pass.** Manual: drive via Twist again through the node.

- [ ] **Step 5: Commit**

```bash
git add ros2/src/avl_sim_bridge
git commit -m "$(cat <<'EOF'
add C++ cmd mux hinge for Gazebo drive inputs.

Keeps Jetson-style Twist/RPM command paths on frozen topic names.
EOF
)"
```

---

### Task 6: VLP-16 in Gazebo + bag comparison tooling

**Files:**
- Create: `gazebo/models/vlp16/` or use existing gz lidar sensor on `velodyne` link
- Create: `ros2/src/avl_lidar_eval/` (C++): load bag cloud + live/sim cloud, compute range error / density / dropout
- Create: `docs/eval/VLP16_PROTOCOL.md` (course, distances, bag naming)
- Bridge: `/velodyne_points` must match frozen name and `sensor_msgs/PointCloud2`

**Interfaces:**
- Consumes: frozen `/velodyne_points`; real bag path outside git (`*.mcap` / `*.db3` gitignored)
- Produces: CSV or markdown table + figure script inputs for poster

- [ ] **Step 1: Attach GPU/CPU lidar sensor** in Gazebo to `velodyne` frame; bridge to `/velodyne_points`.

- [ ] **Step 2: Verify**

```bash
ros2 topic hz /velodyne_points
ros2 topic echo /velodyne_points --once
```

Expected: non-empty cloud, frame_id matches topic map.

- [ ] **Step 3: Write `avl_lidar_eval` C++ tool** that for each paired scan computes: mean/median range error vs nearest real point (or plane targets), points-per-scan density, dropout fraction below intensity/range threshold. Document assumptions in `VLP16_PROTOCOL.md`.

- [ ] **Step 4: Run on one real bag + one sim recording** of the empty_course markers. Save numbers under `docs/eval/results/` (small text only).

- [ ] **Step 5: Commit** (no bags)

```bash
git add gazebo ros2/src/avl_lidar_eval docs/eval
git commit -m "$(cat <<'EOF'
add VLP-16 Gazebo sensor path and C++ sim-to-real eval tool.

Supports poster metrics: range error, density, and dropout on a fixed course.
EOF
)"
```

---

### Task 7: Autonomy unchanged smoke test

**Files:**
- Create: `ros2/src/avl_gazebo_bringup/launch/autonomy_smoke.launch.py`
- Create: `docs/SMOKE_TEST.md`

**Interfaces:**
- Consumes: whatever semi-written autonomy package the team points at (external or submodule later)
- Produces: checklist proving no topic remaps required

- [ ] **Step 1: Document** exact packages/nodes used for smoke test in `SMOKE_TEST.md`.

- [ ] **Step 2: Launch sim + autonomy** with **zero** `remap` rules for frozen topics.

- [ ] **Step 3: Pass criteria:** robot moves from autonomy commands; `/odom` and `/velodyne_points` received by autonomy without rename.

- [ ] **Step 4: Commit** docs + launch helper.

```bash
git add ros2/src/avl_gazebo_bringup docs/SMOKE_TEST.md
git commit -m "$(cat <<'EOF'
add autonomy smoke test proving frozen topic parity.

Documents zero-remap closed loop against the Jetson-aligned map.
EOF
)"
```

---

### Task 8: Isaac optional (only after S1–S3)

**Files:**
- Modify: `isaac/` scripts to subscribe/publish the **same** `topics.yaml` names
- Create: `docs/ISAAC_PHASE4.md` gate checklist

**Interfaces:**
- Consumes: frozen topic map + URDF (convert/export USD as needed)
- Produces: alternate backend, not a second topic contract

- [ ] **Step 1: Confirm** Tasks 4–7 done and topic map still `frozen`.

- [ ] **Step 2: Minimal Isaac scene** with skid-steer + lidar publishing `/velodyne_points` and taking `/cmd_vel`.

- [ ] **Step 3: Re-run autonomy smoke with Isaac backend; no topic renames.**

- [ ] **Step 4: Commit** only if gate passed.

---

## Self-review

1. **Spec coverage:** S1↔Tasks 4–5,7; S2↔Task 2; S3↔Task 6; S4↔Tasks 5–6; S5↔Task 8. Non-goals respected (no Chrono replace, no campus recon).
2. **Placeholders:** Topic types may change in Task 2 after inventory — that is intentional; later tasks must re-read frozen YAML.
3. **Consistency:** Package names `avl_description`, `avl_gazebo_bringup`, `avl_sim_bridge`, `avl_lidar_eval` used throughout.
