# Fortress command and raw odometry check

This implements the Gazebo transport loop on the current IGVC stand-in model:

```text
/cmd_vel -> ros_gz_bridge -> DiffDrive -> /wheel_odom
                                       /clock
                                       odom -> base_link (optional TF bridge)
```

It does not launch Nav2, an EKF, or simulated IMU/GNSS/LiDAR/ZED sensors.
`/wheel_odom` is raw simulated drive odometry. `/odometry/filtered` remains
the local EKF's responsibility. The topic contract stays `adopted` until a live
Jetson inventory is reviewed. Existing geometry and `zed_center_link` are retained.

## Run in the shared Humble / Fortress container

Use an isolated ROS domain for this simulation. Set the same value in both
container terminals:

```bash
export ROS_DOMAIN_ID=42
cd /ws
colcon build --symlink-install --packages-select avl_description
source /ws/install/setup.bash
ros2 launch avl_description sim.launch.py gui:=false
```

Omit `gui:=false` to open the Gazebo window. The headless mode still runs physics.
In a second terminal, source the workspace and run:

```bash
export ROS_DOMAIN_ID=42
source /ws/install/setup.bash
ros2 run avl_description check_closed_loop.py --drive-sim
```

The check waits up to 45 wall seconds for the bridge and messages, sends zero
commands while the model settles, commands 0.15 m/s for about two wall seconds,
then sends zero commands. It passes only when the clock and odometry timestamps
advance, odometry has `odom` / `base_link` frames, and displacement exceeds 2 cm.
It checks that only `gazebo_bridge` consumes commands and publishes raw odometry
before sending commands. A failure exits nonzero and reports the failed criteria.

Also inspect TF in the default standalone mode:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

When the normal local EKF is added, give it ownership of `odom -> base_link`:

```bash
ros2 launch avl_description sim.launch.py publish_odom_tf:=false
```

All localization/autonomy nodes must also use simulation time. Do not alias raw
odometry onto `/odometry/filtered`, and do not enable both TF owners.

## Automated checks

```bash
colcon test --packages-select avl_description
colcon test-result --verbose
```

Contract tests expand the xacro and compare bridge topics, directions, frames,
wheel joints and world clock against the adopted contract. They also check
failure cases in the motion assessment and read-only inventory capture.
The GitHub workflow builds on Humble, runs these tests, then runs the actual
headless command-to-motion check and saves its logs. A successful source test
alone does not establish that Gazebo has run.

References: [Fortress DiffDrive parameters](https://gazebosim.org/api/gazebo/6/classignition_1_1gazebo_1_1systems_1_1DiffDrive.html)
and [Humble ros_gz bridge configuration](https://github.com/gazebosim/ros_gz/blob/humble/ros_gz_bridge/README.md).
