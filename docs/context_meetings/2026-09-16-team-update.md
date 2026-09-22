# AVL Autonomy Sim: Team Update

**Date:** 2026-09-16  
**Drive:** Shared → `AVL_Autonomy_Sim` → `Context Messages/Files`  
**Repo:** https://github.com/Ryan-Simpson/AVL_Autonomy_Sim

Check out the GitHub repo to get familiar with the project and how it's laid out:  
`https://github.com/Ryan-Simpson/AVL_Autonomy_Sim`

I'll divide up the work soon, once we see how things get rolling.

## Scope change: Gazebo first

We're moving to a **Gazebo-first** simulation. Isaac Sim is now an optional second backend that we'll only pick up if time allows once Gazebo is working. Because of this, how we split up the work will change a bit too. The repo README and the design doc in `docs/` have the updated scope.

## What's coming next

### 1. MARVIN assets in the repo
I'll add the MARVIN assets (URDF, meshes) to the GitHub as soon as I can, so you can all start working with the rover model. They'll be in `assets/`.

### 2. Shared Gazebo environment on the lab PC
You don't have to set this up on your own laptop. I'm building a **VirtualBox VM on the lab PC** with **Ubuntu 22.04, ROS 2 Humble, and Gazebo**, and it will have the MARVIN simulation ready to run.

- **Use the lab VM** if you don't want to install everything yourself.
- **Set it up locally** if you'd like (Ubuntu 22.04 + ROS 2 Humble + Gazebo) so your setup matches the VM.

I'll post in the group once the VM is ready.

### 3. Learning resources
Watch these two videos before we start building. They explain what ROS and Gazebo actually do, so they aren't just buzzwords:

1. **ROS Overview** (Articulated Robotics): https://www.youtube.com/watch?v=KAASuA3_4eg  
   Covers nodes, topics, messages, services, parameters, launch files, packages, and workspaces.
2. **Simulating Robots with Gazebo and ROS** (Articulated Robotics): https://www.youtube.com/watch?v=laWn7_cj434  
   Covers what a simulator does, how a robot model gets into Gazebo, and how Gazebo talks to ROS.

> **Note:** These videos use ROS 2 Foxy and Gazebo Classic. The ideas are the same for us, but some commands are different. We use ROS 2 Humble with **Gazebo Fortress** (`gz sim`, `ros-humble-ros-gz`), so follow our repo for the actual setup commands.

## Action items

| Who | What |
|-----|------|
| Ryan | Push MARVIN assets to the repo |
| Ryan | Set up the Ubuntu 22.04 / Gazebo VM on the lab PC |
| Ryan | Share the ROS 2 + Gazebo intro videos |
| Everyone | Watch both videos, then choose the lab VM or a local install |

## Repo pointers

| Doc | Purpose |
|-----|---------|
| [README.md](../../README.md) | Product abstract + layout |
| [FALL_2026_BAHR_BRIEF.md](../FALL_2026_BAHR_BRIEF.md) | Fall deliverables |
| [gazebo-first design](../design/2026-09-15-gazebo-first-design.md) | Architecture |
| [gazebo-first plan](../plans/2026-09-15-gazebo-first-closed-loop.md) | Task breakdown |
| [topic map](../../ros2/topic_map/TOPICS.md) | Draft Jetson topic contract |
| [Isaac research map](../ISAAC_RESEARCH_MAP.md) | Phase 4 literature (optional Isaac) |
