# Topic map

**Status:** draft until Jetson inventory is done, then freeze.

## Rules

1. Where the Jetson stack already uses a name, that name wins.
2. Gaps are added once here, then frozen with everything else.
3. No long-lived sim-only aliases unless the same name exists on the robot.
4. After freeze (`topics.yaml` → `status: frozen`), renames need brief-owner approval.

## Files

- `topics.yaml` — machine-readable contract for bridges and launch
- `INVENTORY.md` — team dump of known Jetson pubs/subs (create during inventory)

## Seed list (from project abstract; override from inventory)

| Topic | Type (expected) | Direction (from sim) |
|-------|-----------------|----------------------|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | subscribe |
| `/odom` | `nav_msgs/msg/Odometry` | publish |
| `/imu/data` | `sensor_msgs/msg/Imu` | publish |
| `/gps/fix` | `sensor_msgs/msg/NavSatFix` | publish |
| `/velodyne_points` | `sensor_msgs/msg/PointCloud2` | publish |
| ZED streams | image / camera_info | publish (later) |
| L/R RPM (Teensy-style) | TBD from inventory | subscribe if used on robot |
