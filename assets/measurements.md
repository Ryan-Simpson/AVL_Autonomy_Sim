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
| Mass (kg) | 49 | brief | Whole robot. Chassis link 45 kg, four wheels 1 kg each. |
| Track width `b` (m) | 0.7306 | IGVC | `2 * 0.3653` m, tread centerlines in the IGVC URDF. Not tape. |
| Wheel / sprocket radius `r` (m) | 0.06985 | IGVC | Half the IGVC tread-enclosure height. Diff-drive stand-in. |

## Frames

All mounts are **`xyz` + `rpy` relative to `base_link`** (REP-103: x forward, y left, z up).

| Link | x (m) | y (m) | z (m) | roll | pitch | yaw | Source | Notes |
|------|-------|-------|-------|------|-------|-----|--------|-------|
| `velodyne` | 0.089 | 0 | 0.7146 | 0 | 0 | 0 | IGVC | 3.5 in forward, 6.25 in above the IMU. Stand-in. |
| `imu_link` | 0 | 0 | 0.5556 | 0 | 0 | 0 | IGVC | 21.875 in above ground. Stand-in. |
| `gps_link` | 0.6795 | 0 | 0.534 | 0 | 0 | 0 | placement | On the roof of the main chassis, same x as the front camera. Not tape. |
| `zed_left_link` | 0.098 | 0.286 | 0.6126 | 0 | 0 | 1.5708 | IGVC | Faces left. Stand-in. |
| `zed_center_link` | 0.6795 | 0 | 0.4476 | 0 | 0.2618 | 0 | IGVC | Called `zed_front` in IGVC. 15 deg down. Stand-in. |
| `zed_right_link` | 0.098 | -0.286 | 0.6126 | 0 | 0 | -1.5708 | IGVC | Faces right. Stand-in. |

Camera optical frames (`*_optical_frame`) are Z-forward children of the camera links — defined in the URDF, not re-measured here.

## Session log

| Date | What was measured | Who |
|------|-------------------|-----|
| | | Ryan |

## Status

- [ ] Chassis L/W/H
- [x] Mass — 49 kg lab figure, not a weigh-in
- [x] Track width and wheel radius — IGVC stand-in, not tape
- [x] VLP-16 mount — IGVC stand-in
- [x] Xsens mount — IGVC stand-in
- [x] GNSS mount — on the main-chassis roof, placement, not tape
- [x] ZED X left / center / right mounts — IGVC stand-in
