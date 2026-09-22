#!/usr/bin/env bash
set -e
source "/opt/ros/${ROS_DISTRO}/setup.bash"
[ -f /ws/install/setup.bash ] && source /ws/install/setup.bash
exec "$@"
