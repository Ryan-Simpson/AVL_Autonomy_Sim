# AVL Autonomy Sim: sensors working, next is waypoint navigation

**Date:** 2026-11-09
**Status:** Local note. Sensor work below is done and tested but not committed.
**Decided by:** Ryan (project lead)
**Reference stack:** https://github.com/Paarseus/IGVC_ROS2 (Parsa Ghasemi), commit `654ad97` (2026-10-14)

## Rule for this work

Everything follows Parsa's current code: topic names, frames, rates, perception settings, Nav2 config. We do not write a new planner or detector. When the sim doesn't match his settings, we fix the sim (world, lighting, sensors), not his thresholds.

## What works now (2026-11-09)

All of this was tested in `avl-sim` (Gazebo Fortress 6.18, ROS 2 Humble) on `igvc_course.sdf`.

| Sensor | ROS topic | Frame | Rate | Notes |
|---|---|---|---|---|
| VLP-16 | `/velodyne_points` | `velodyne` | 10 Hz | `gpu_lidar`, 16 beams over ±15°, 1800 samples around 360°, 0.5–100 m. Fields x, y, z, intensity, ring. |
| ZED front / left / right image | `/zed_<cam>/zed_node/rgb/color/rect/image` (+ `camera_info`) | `zed_center_optical_frame`, `zed_left_optical_frame`, `zed_right_optical_frame` | 8 Hz | 480×300, matching Parsa's `zed_front.yaml` (SVGA downscaled, 8 Hz). |
| ZED cloud | `/zed_<cam>/zed_node/point_cloud/cloud_registered` | `zed_<cam>_camera_link` | 8 Hz | Organized 480×300, same stamp as the image. Separate sensor because Gazebo's cloud is x-forward, not optical. |

**Line detection:** Parsa's `avros_perception` (`perception_node`, `sooner25` pipeline, his `perception.yaml` unchanged) was run against the sim with `cameras:=front,left,right use_sim_time:=true`. It marks the painted white lines on all three cameras (left 645, right 553, front 2133 lane pixels) and marks no asphalt. It ran from a scratch workspace in the container (`/tmp/parsa_ws`), not from this repo.

### Files changed

- `gazebo/worlds/igvc_course.sdf`: added `ignition-gazebo-sensors-system` (ogre2).
- `ros2/avl_description/urdf/tracked_rover.urdf.xacro`: VLP-16 `gpu_lidar`; `zed_sim` macro with a `camera` plus an `rgbd_camera` per ZED.
- `ros2/avl_description/config/bridge.yaml`: `/velodyne_points` plus image, camera_info and cloud for each ZED.
- `ros2/topic_map/topics.yaml`, `TOPICS.md`: ZED image topics renamed to the zed_wrapper v5.x path `rgb/color/rect/image`, which `avros_perception` subscribes to. The old `rgb/image_rect_color` is pre-v5. `INVENTORY.md` still asks the Jetson to confirm.
- `gazebo/models/orange_igvc/model.sdf`: ground material set to `metalness 0` / `roughness 1`. Before this, ogre2 rendered the white paint at V≈158, below Parsa's V 185 floor. After it, the paint renders at V≈240 on asphalt at V≈123.

### Known stand-ins and gaps

- ZED horizontal FOV 110° is the ZED X 2.2 mm datasheet value, not a measurement.
- All sensor mounts are still the IGVC stand-ins in `assets/measurements.md`.
- The side ZEDs are mounted level, so Parsa's adaptive V ceiling (93rd percentile of rows 40–100%) includes sky. The line (V≈240) only just beats the sky (V≈231). Real side mounts are not measured, and Parsa's stack does not run the side cameras on the robot yet.
- LiDAR rate: the spec says 10 Hz; Parsa's logs measured 19.7 Hz on the robot. Confirm on the Jetson.
- The bridge publishes RELIABLE; the real `velodyne_driver` is usually best-effort.

## Decisions made today (Ryan)

1. **Navigation is in scope.** Run Parsa's existing Nav2 stack on the sim. This is not a new planner.
2. **TF ownership:** once Parsa's odom EKF runs, it is the only publisher of `odom → base_link`, and the diff-drive `/tf` is no longer bridged. Before that, diff-drive owns it. Never two publishers.
3. **Installs:** STVL and the kiwicampus semantic layer may be installed in the running container for testing, then added to the Dockerfile.
4. **Waypoints:** we pick 4–5 points down the middle of the sim course's lane, converted to lat/lon from a world origin. They go in Parsa's `waypoints.yaml` format so his `mission_manager` reads them unchanged. His real Oakland waypoints do not match the sim course layout.
5. **`/gnss` frame:** `imu_link` (Ryan's 21 October note, same as Parsa's Webots sim), not `gps_link` from `topics.yaml`.

## Roles

| Job | Parsa's pipeline |
|---|---|
| LiDAR: **obstacles only** | `/velodyne_points` → `lidar_preprocessor` → `/perception/lidar/obstacles` → STVL layer (local costmap) |
| Cameras: **stay inside the white lines** | 3× `perception_node` → `/perception/<cam>/semantic_*` → kiwicampus `semantic_segmentation_layer` (lines become cost) |
| Waypoints: **go forward** | `waypoints.yaml` → `mission_manager` → `/fromLL` (navsat_transform) → NavigateToPose goals in `map`; reached within 2 m. MPPI with `vx_min: 0` (no cruise reverse). |
| Localization | `ekf_filter_node_odom` + `ekf_filter_node_map` (`ekf.yaml`) + `navsat_transform` (`navsat.yaml`), fusing `/imu/data`, `/wheel_odom`, `/odometry/gps` |

Already in the container: `nav2_bringup`, `nav2_mppi_controller`, `nav2_route`, `nav2_waypoint_follower`, `robot_localization`.
Missing: `spatio_temporal_voxel_layer`, kiwicampus `semantic_segmentation_layer` (built from source with Parsa's `scripts/apply_kiwicampus_patches.sh`).

## Plan (each step verified before the next)

1. **IMU, GPS and world origin.** Gazebo IMU on `imu_link` → `/imu/data`. NavSat → `/gnss` with frame `imu_link`. `spherical_coordinates` in `igvc_course.sdf`. Bridge types `ignition.msgs.IMU`, `ignition.msgs.NavSat`.
   - Check: `ros2 topic hz /imu/data` ≈ 100 Hz, `frame_id: imu_link`. `ros2 topic echo /gnss --once` shows a fix near the world origin.
2. **Localization.** Parsa's `ekf.yaml` and `navsat.yaml`. Remove the diff-drive `/tf` bridge entry.
   - Check: `ros2 run tf2_ros tf2_echo map base_link` works. `/odometry/filtered` and `/odometry/gps` publish. `odom → base_link` has exactly one publisher.
3. **LiDAR obstacles.** Install STVL. Run Parsa's `lidar_preprocessor` with his `lidar.yaml`.
   - Check: barrels show up in `/local_costmap/costmap` in RViz.
4. **Camera lines.** Build the kiwicampus layer with Parsa's patch.
   - Check: the painted lines show up as cost in `/local_costmap/costmap`.
5. **Waypoints.** Sim waypoints in Parsa's format. His `nav2_params_igvc_autonav.yaml`, BT XML and `mission_manager` with `use_sim_time`.
   - Check: the rover drives forward through the waypoints in order without crossing a line or hitting a barrel.

## Progress (end of 2026-11-09)

| Step | Status | Evidence |
|---|---|---|
| 1. IMU, GPS, world origin | ✅ | `/imu/data` 100 Hz in `imu_link`, absolute ENU yaw (+90° when facing north). `/gnss` 10 Hz, fix; moves 2.87 m north when the rover drives 2.86 m. |
| 2. Localization | ✅ | Parsa's `ekf.yaml` and `navsat.yaml` (unchanged, `config/igvc/`). `/odometry/filtered` and `/odometry/global` at 30 Hz, `/odometry/gps` at 10 Hz. `map → base_link` matches the spawn. `/tf` publishers: the two EKFs and robot_state_publisher; diff-drive `/tf` removed from the bridge. |
| 3. LiDAR obstacles | ✅ | STVL installed (apt, and in the Dockerfile). Parsa's `lidar_preprocessor` gives `/perception/lidar/obstacles` at 10 Hz: ground removed, barrels kept. |
| 4. Camera lines | ⚠️ built, detection patchy | Paarseus `semantic_segmentation_layer` fork (`avros-fixes`, `ffb3c7d`) built. Lines reach the costmap only now and then (see below). |
| 5. Waypoints | ⚠️ drives, crosses lines | `nav_sim.launch.py` with Parsa's competition Nav2 pair and `mission_manager` on `waypoints_sim.yaml` (6 points). Trial: 35.9 m forward through all waypoints in order (4 reached at 2 m, 2 aborted by Nav2 and skipped). No barrel contact (closest 1.16 m from an edge). **A line was under the footprint for ~12 s**: it cut the inside of the south-east bend and ran in the infield near y≈11. |

### Why the lines don't hold the rover in the lane

- **Front ZED** (15° down, 0.45 m, both IGVC stand-ins): Parsa's `sky_roi_poly` masks the top 60%, so it only sees ground 0.3–0.96 m ahead and about ±1.37 m sideways. Centered in the ~3.2 m lane, the lines (±1.6 m) are just out of view.
- **Side ZEDs** (level, stand-in): `sooner25_band: [0.40, 1.0]` includes sky, so the adaptive V ceiling rises to sky brightness and the line is missed most of the time.
- Both come from mount poses that aren't measured. Parsa's thresholds weren't changed.

### Fixes made along the way

- The Nav2 servers were on wall clock: `RewrittenYaml` only replaces keys that already exist, and Parsa's params have no `use_sim_time`. Now `use_sim_time` is passed to each node. Before this, every goal "succeeded" instantly.
- Waypoints moved away from barrels (the course has barrels in the lane). WP5 inside the east barrel slalom was dropped.
- Spawn moved to the south-lane centerline facing east (`0, 0.1, yaw 0`). The old spawn faced the inner line 0.6 m away.
- `cpp_campus_graph.geojson` (11.6 MB) not copied; a 2-node `sim_route_graph.geojson` lets `route_server` activate.
- Parsa's launch files force CycloneDDS. The sim and Nav2 all run on the default Fast DDS (consistent), so his nodes are started without his DDS setting.

### Line-holding work (later on 2026-11-09, Ryan approved options 1 and 2)

- **Option B** (sim-only, `nav_sim.launch.py`): side cameras use `sooner25_band: [0.60, 1.0]`; the front keeps Parsa's `[0.40, 1.0]`.
- **Outer ground** (`igvc_course.sdf`): a 200 × 200 m plain plane, gray 0.35, 5 mm under the course. Before it, the side cameras looked past the outer lines into empty background. Right camera line pixels went from 0 to 810.
- **Main cause found:** Parsa's local `semantic_layer` lists `observation_sources: front` only. His `left` and `right` blocks are fully written but unused, because his robot runs only the front camera. Sim-only override: `front left right` for the local costmap (path-specific `RewrittenYaml` key); the global costmap is unchanged. At spawn, both lane lines are now lethal in the local costmap before the rover moves.
- **Trial after these changes:** 33.7 m, waypoints in order (4 reached, 2 aborted by Nav2 and skipped), closest barrel 1.13 m from an edge. Line under the footprint at the south-east bend dropped from ~12 s to ~2 s. **Still crosses at the east barrel slalom** (y 9.5–13): it squeezed between barrel 7 (16.06, 11.89) and the inner line, a gap of about 0.76 m against a 0.83 m footprint, instead of the 1.26 m gap between barrels 5 and 7.
- MPPI `CostCritic` has `consider_footprint: true` and `collision_cost: 1e6`, so the line cells must have been missing where it crossed. Unverified guess: with `clearing: true`, each source raytraces free space through what it sees, so the front camera's masked top 60% may clear lines the side cameras marked, and a line right beside the rover is below the side cameras' view (closest visible ground is 0.69 m). Next step: capture the local costmap while the rover is in the slalom.
- NoMachine (`nxserver`) was hooked into `:0` with nobody connected and broke OpenGL for container GUIs. Stopped with `sudo /usr/NX/bin/nxserver --shutdown`; GUIs work again. Restore with `sudo /usr/NX/bin/nxserver --startup`.

### Host display problem (2026-11-09 evening)

The Gazebo GUI and RViz started segfaulting on `DISPLAY=:0` (OpenGL init, `XCB error 148`), even with NVIDIA GLX offload or software GL. It worked earlier in the day, so the host display changed. Workaround: `sim.launch.py headless:=true` (`--headless-rendering`, EGL on the NVIDIA GPU, no X). RViz still needs a working display.

## Operating notes

- Closing the Gazebo window leaves the launch, the bridge and sometimes `ign gazebo server` running in the container. Clear them before relaunching, or you get two Gazebos on one partition (stale topics, halved sensor rates).
- Launch: `docker exec -d avl-sim bash -lc 'source /ws/install/setup.bash; export DISPLAY=:0; ros2 launch avl_description sim.launch.py > /tmp/sim.log 2>&1'`
- Headless sim: `ros2 launch avl_description sim.launch.py headless:=true`
- Navigation (after the sim is up, with the external workspace sourced): `source /tmp/parsa_ws/install/setup.bash && ros2 launch avl_description nav_sim.launch.py` (`mission:=false` to bring up Nav2 without driving). The external workspace (`avros_perception`, `avros_navigation`, `semantic_segmentation_layer`) lives in the container's `/tmp/parsa_ws` and is lost when the container is recreated.
