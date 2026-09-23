# MARVIN measurements

**Owner:** Ryan only. Team copies from this file or writes `TODO measure`. Do not invent numbers.

Units: **meters** and **radians**. Leave a cell blank if not measured yet. Blank beats guessing.

**Source codes:** `tape` | `CAD` | `datasheet` | `estimate` (avoid) | blank = not done

## Chassis

| Quantity | Value | Source | Notes |
|----------|-------|--------|-------|
| Length (m) | | | along drive direction |
| Width (m) | | | left–right outer |
| Height (m) | | | ground to top of chassis (no mast) |
| Mass (kg) | | | ~49 kg if still unknown — label `TODO measure` in URDF |
| Track width `b` (m) | | | left contact center to right contact center |
| Wheel / sprocket radius `r` (m) | | | used by diff-drive stand-in |

## Frames

All mounts are **`xyz` + `rpy` relative to `base_link`** (REP-103: x forward, y left, z up).

| Link | x (m) | y (m) | z (m) | roll | pitch | yaw | Source | Notes |
|------|-------|-------|-------|------|-------|-----|--------|-------|
| `velodyne` | | | | | | | | VLP-16 optical / sensor origin |
| `imu_link` | | | | | | | | Xsens MTi-680G |
| `gps_link` | | | | | | | | GNSS antenna |
| `zed_left_link` | | | | | | | | Stereolabs ZED X |
| `zed_center_link` | | | | | | | | |
| `zed_right_link` | | | | | | | | |

Camera optical frames (`*_optical_frame`) are Z-forward children of the camera links — defined in the URDF, not re-measured here.

## Session log

| Date | What was measured | Who |
|------|-------------------|-----|
| | | Ryan |

## Status

- [ ] Chassis L/W/H
- [ ] Mass
- [ ] Track width and wheel radius
- [ ] VLP-16 mount
- [ ] Xsens mount
- [ ] GNSS mount
- [ ] ZED X left / center / right mounts
