# syntax=docker/dockerfile:1
# AVL Autonomy Sim — ROS 2 Humble + Gazebo Fortress (Ubuntu 22.04 / JetPack 6 userland)

ARG ROS_DISTRO=humble
FROM osrf/ros:${ROS_DISTRO}-desktop

ARG ROS_DISTRO
ENV DEBIAN_FRONTEND=noninteractive

# LAYER 1: sim + tooling. Gazebo Fortress is Humble's official pairing;
# ros_gz pulls in the Fortress libraries from packages.ros.org.
RUN apt-get update && apt-get install -y --no-install-recommends \
      ros-${ROS_DISTRO}-ros-gz \
      ros-${ROS_DISTRO}-gz-ros2-control \
      ros-${ROS_DISTRO}-xacro \
      ros-${ROS_DISTRO}-robot-state-publisher \
      ros-${ROS_DISTRO}-joint-state-publisher-gui \
      ros-${ROS_DISTRO}-ros2-control \
      ros-${ROS_DISTRO}-ros2-controllers \
      ros-${ROS_DISTRO}-diff-drive-controller \
      ros-${ROS_DISTRO}-rviz2 \
      ros-${ROS_DISTRO}-tf2-tools \
      ros-${ROS_DISTRO}-pointcloud-to-laserscan \
      ros-${ROS_DISTRO}-robot-localization \
      ros-${ROS_DISTRO}-nav2-bringup \
      ros-${ROS_DISTRO}-slam-toolbox \
      python3-colcon-common-extensions \
      python3-vcstool \
      python3-rosdep \
      python3-pip \
      git vim nano tmux less curl wget file iputils-ping net-tools sudo \
      libglvnd0 libgl1 libglx0 libegl1 libgles2 libxext6 libx11-6 mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# LAYER 2: non-root user matching the HOST uid/gid.
ARG USERNAME=avl
ARG UID=1000
ARG GID=1000

RUN if getent group ${GID} >/dev/null; then \
        groupmod -n ${USERNAME} "$(getent group ${GID} | cut -d: -f1)"; \
    else \
        groupadd -g ${GID} ${USERNAME}; \
    fi \
 && if getent passwd ${UID} >/dev/null; then \
        usermod -l ${USERNAME} -d /home/${USERNAME} -m \
                "$(getent passwd ${UID} | cut -d: -f1)"; \
    else \
        useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USERNAME}; \
    fi \
 && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
 && chmod 0440 /etc/sudoers.d/${USERNAME}

# LAYER 3: runtime env. Fortress reads IGN_GAZEBO_RESOURCE_PATH;
# GZ_SIM_RESOURCE_PATH is the Harmonic name, set too for future-proofing.
ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=all \
    QT_X11_NO_MITSHM=1 \
    IGN_GAZEBO_RESOURCE_PATH=/ws/src/AVL_Autonomy_Sim/gazebo/models:/ws/src/AVL_Autonomy_Sim/gazebo/worlds:/ws/src/AVL_Autonomy_Sim/gazebo \
    GZ_SIM_RESOURCE_PATH=/ws/src/AVL_Autonomy_Sim/gazebo/models:/ws/src/AVL_Autonomy_Sim/gazebo/worlds:/ws/src/AVL_Autonomy_Sim/gazebo \
    ROS_DISTRO=${ROS_DISTRO}

RUN mkdir -p /ws/src /ws/build /ws/install \
 && chown -R ${UID}:${GID} /ws

COPY --chmod=0755 entrypoint.sh /entrypoint.sh

USER ${USERNAME}
WORKDIR /ws

RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc \
 && echo "[ -f /ws/install/setup.bash ] && source /ws/install/setup.bash" >> ~/.bashrc

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
