# Docker — AVL Autonomy Sim

Shared env for the team: **Ubuntu 22.04**, **ROS 2 Humble**, **Gazebo Fortress**, **`ros-humble-ros-gz`**.

Fortress CLI is **`ign gazebo`** (not `gz sim` — that name is Harmonic-era). Do not install a different Gazebo. Do not use Gazebo Classic.

## Prerequisites (host)

- Docker Engine + Docker Compose v2
- NVIDIA Container Toolkit (lab PC / workstation with GPU) for sensors and GUI
- X11 display if you want the Gazebo window (`echo $DISPLAY` should print something like `:0` or `:1`)

Clone the repo, then work from this folder:

```bash
cd ~/Documents/AVL_Autonomy_Sim/docker
# or wherever you cloned AVL_Autonomy_Sim
```

## Build

First time, or after `Dockerfile` changes:

```bash
cd docker
./dev.sh build
```

Image name: `avl/autonomy-sim:humble`.

## Start (GUI on the lab GPU machine)

```bash
./dev.sh up
```

That builds the X auth cookie, starts container `avl-sim`, and drops you into a bash shell with ROS sourced.

More terminals into the same container:

```bash
./dev.sh shell
```

Stop:

```bash
./dev.sh stop
```

Wipe volumes (build/install caches) if things are badly broken:

```bash
./dev.sh clean
```

## Prove it works (do this once after build)

Inside the container (`./dev.sh up` or `./dev.sh shell`):

```bash
# ROS 2
ros2 --help
echo $ROS_DISTRO   # expect: humble

# Gazebo Fortress (CLI is ign gazebo, not gz sim)
ign gazebo -v 4 shapes.sdf
```

That should open the Fortress window. Close it when you are done looking.

Headless (no window — useful on SSH or when checking sensors later):

```bash
ign gazebo -s -v 4 shapes.sdf
# Ctrl+C to stop
```

If `ros2` or `ign` is missing in a fresh `docker compose exec` shell, run:

```bash
source /opt/ros/humble/setup.bash
```

Interactive `./dev.sh shell` already sources ROS via `~/.bashrc`.

## Repo mount and colcon

The repo is mounted at `/ws/src/AVL_Autonomy_Sim`.

```bash
cd /ws
# after packages exist under /ws/src/AVL_Autonomy_Sim/ros2/...
colcon build --symlink-install
source /ws/install/setup.bash
```

`build/` and `install/` live in Docker volumes so they persist across `./dev.sh stop`.

## If something fails

| Symptom | Fix |
|---------|-----|
| `could not select device driver "nvidia"` | Install/enable NVIDIA drivers + NVIDIA Container Toolkit on the host. Lab GPU machine is the intended target. |
| Gazebo window blank / no display | On the host: `xhost +local:docker` once per login, confirm `echo $DISPLAY`, then `./dev.sh up` again. |
| Permission errors writing under the repo | `./dev.sh` sets `HOST_UID` / `HOST_GID` to your user. Rebuild if you changed users: `./dev.sh build`. |
| Stale packages after pulling | `./dev.sh shell` then `cd /ws && colcon build --symlink-install`. |

## What this image is not

- Not Gazebo Classic (`gazebo` / `gazebo11`)
- Not Isaac Sim
- Not a substitute for measuring the real robot (`assets/measurements.md` is Ryan’s sheet)
