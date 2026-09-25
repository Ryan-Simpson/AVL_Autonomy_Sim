# AVL Autonomy Sim: IGVC rover in Fortress

**Date:** 2026-09-24  
**Status:** Local note only. Not pushed.  
**Repo:** https://github.com/Ryan-Simpson/AVL_Autonomy_Sim

This is what we actually ran, what we do not have, and what the next steps are. It does not close any step on the team task list.

## We do not have MARVIN's official model

There is no official MARVIN URDF, mesh set, recorded TF tree, or filled measurement sheet in this repo. `assets/measurements.md` is still blank. Do not invent mounts. If a number is missing, leave it blank or write `TODO measure` and use `0 0 0`.

What we can start from is the IGVC stack at https://github.com/Paarseus/IGVC_ROS2 (Parsa Ghasemi). The robot description is `src/avros_bringup/urdf/avros.urdf.xacro`. It is a primitive-box model of the AVL IGVC chassis, not a mesh. The comments attribute the box sizes and several mounts to a 2026-05-06 resurvey and an April 2026 sketch. Several joints in that file are still marked "measure on the vehicle." Mass there is a placeholder **150 kg**, not the ~49 kg in our brief. The ZED links in that file come from Stereolabs `zed_wrapper`, which we do not have installed, so our copy uses boxes at the same mount poses.

`src/avros_sim/resource/avros_webots.urdf` is not a second robot. It only maps Webots devices onto topics.

The keyboard controller we used is the same node IGVC already launches: `teleop_twist_keyboard` from `src/avros_bringup/launch/teleop.launch.py`. We did not write a new controller. We did not launch `actuator_node`. That node talks to the Teensy over serial on the real robot.

## What is running

The sim is the lab image `avl/autonomy-sim:humble`: Ubuntu 22.04, ROS 2 Humble, Gazebo Fortress 6.18 (`ign gazebo`).

`docker compose up` / `./dev.sh up` did not start. The compose file reserves an NVIDIA GPU, and the driver is not loaded (`nvml error: driver not loaded`). The same image was started with `docker run` and no GPU. Container name: `avl-sim`. Lidar and camera rendering that need the GPU are not part of this run.

Inside that container:

- World `gazebo/worlds/empty_course.sdf`: flat ground, 1 ms physics step. No course boxes yet.
- Model `tracked_rover`, spawned from `ros2/avl_description/urdf/tracked_rover.urdf.xacro`.
- Chassis, IMU, VLP-16 cylinder, and three ZED boxes are the IGVC geometry.
- Four wheel cylinders stand in for the tracks so the body does not nose over. The team list still asks for two wheels. This is a stand-in, not the finished step.
- Drive plugin is Fortress `ignition-gazebo-diff-drive-system`. A straight-line velocity plugin was tried first. It slid the body along one direction and did not yaw, so it was removed.
- `teleop_twist_keyboard` publishes ROS `/model/tracked_rover/cmd_vel` (speed 0.3 m/s, turn 0.3 rad/s).
- `ros_gz_bridge` copies that into Fortress as `ignition.msgs.Twist`.
- A test command moved the rover off the origin and changed its heading. `i` forward, `j` / `l` turn, `k` stop.

The first driving session was on the host's ROS 2 Jazzy / `gz sim`, because the Docker daemon was down and then the GPU hook failed. That host session is not the team environment. The run that counts is the Fortress container above.

## What this does not finish

From `docs/plans/project-assignments.md`:

| Step | Where this leaves it |
|------|----------------------|
| 0 Shared container | The image already existed. This run did not use `./dev.sh up`, because the GPU reservation failed. |
| 1 Measurements and frame names | Not done. No `assets/urdf/frames.md`. Measurements sheet still blank. |
| 2 Freeze the topic list | Not done. `ros2/topic_map/topics.yaml` is still `status: draft`. No Jetson inventory. |
| 3 Robot model | Started. The xacro exists. It is not the step's model: four wheels, 150 kg copied from IGVC, mounts not tagged `TODO measure` against our sheet. |
| 4 Spawn in Gazebo | Started. It spawns and sits on the ground in Fortress. The world has no three course boxes. |
| 5 Make it drive | Started. Keyboard `/cmd_vel` reaches the wheels and the rover yaws. Still missing: `/clock`, `/odom`, `use_sim_time`, and a single `odom` → `base_link` publisher. The wheels listen on `/model/tracked_rover/cmd_vel`, not the bare `/cmd_vel` in the topic map. |
| 6–15 | Not started. No RPM mux, IMU, GPS, encoders, VLP-16 cloud, sim-to-real CSV, autonomy smoke test, poster, paper, ZED, or Isaac. |

## Where to go next

Stay on the team order. Do not skip ahead to lidar numbers or Isaac.

1. **Frame names (step 1).** Write `assets/urdf/frames.md` from the IGVC tree: `odom` → `base_link` → `velodyne`, `imu_link`, `gps_link`, `zed_front` / `zed_left` / `zed_right`, plus camera optical frames. Names only. Poses stay `TODO measure` until `assets/measurements.md` has a real number.
2. **Topic inventory (step 2).** Dump the Jetson topics from the IGVC repo (`avros_bringup` configs and launch files) into `ros2/topic_map/INVENTORY.md`. Mark unknowns. Do not freeze `topics.yaml` until that inventory is reviewed. Jetson names win.
3. **Bring the model in line with steps 3–5.** One xacro, two driven wheels, Fortress diff-drive, spawn as `tracked_rover`, bridge `/clock`, `/cmd_vel`, and `/odom`, `use_sim_time:=true`, and only one publisher of `odom` → `base_link`. The final launch has no remaps.
4. **GPU.** When the NVIDIA driver is loaded, use `./dev.sh up` so everyone shares the compose container. Until then, say plainly that a no-GPU `docker run` of the same image is a workaround.
5. **After the closed loop:** IMU, GPS, encoders only if the frozen map has them, then the 16-beam VLP-16 and the parked-scan comparison. Poster and paper use only that CSV. ZED and Isaac stay after steps 1–13.

Anyone can attempt a step that is not marked Ryan, on their own branch. One model, one bridge, one topic list get merged.
