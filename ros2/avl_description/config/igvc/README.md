# Files from Paarseus/IGVC_ROS2

Copied from `src/avros_bringup/config/` at commit `654ad97` (2026-10-14). Do not edit them here; copy them again from upstream.

| File | Use in the sim |
|---|---|
| `ekf.yaml`, `navsat.yaml` | `sim.launch.py` localization. The world origin equals the navsat datum. |
| `nav2_params_igvc_autonav.yaml`, `navigate_igvc_autonav_2026.xml` | `nav_sim.launch.py`, Parsa's competition pair |
| (not copied) `cpp_campus_graph.geojson` | 11.6 MB of CPP-campus graph. Replaced by our 2-node `sim_route_graph.geojson`, used only so `route_server` can activate. The competition BT does not use routes. |

`waypoints_sim.yaml` is ours: sim-course waypoints in Parsa's format (see its header).
`ekf.yaml` and `navsat.yaml` have a two-line source header added; the other copied files are byte-for-byte.
