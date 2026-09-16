# AVL Autonomy Sim: Team Update

**Date:** 2026-09-15  
**Doc name:** `AVLAS_09-15-2026 Meeting Notes`  
**Drive:** Shared with me → `AVL_Autonomy_Sim` → `Context Messages/Files`  
**Repo:** https://github.com/Ryan-Simpson/AVL_Autonomy_Sim

I'm setting up this repo to get started with the project and how it's laid out. I'm starting this with basic structure and how things get setup.

## Scope change: Gazebo first

We are moving to a **Gazebo first** simulation phase (Isaac Sim later if time remains). Goal is closed-loop topic parity with the Jetson stack, then VLP-16 sim-to-real for the poster, with C++ as the primary hinge language.

Build order:

1. One closed loop on Gazebo with real topic names  
2. Freeze the topic map  
3. Measure VLP-16 sim-to-real  
4. Isaac only if time remains  

## What's coming next

1. **Initial assets in the repo**  
   Keep structure and notes in GitHub (`docs/`, `gazebo/`, `ros2/`, etc.) so the team works from one trunk — not only Drive.

2. **Start with Gazebo simulation on the lab PC**  
   Set up a VirtualBox VM on the lab PC with **Ubuntu 22.04**, **ROS 2 Humble**, and **Gazebo**.  
   Use the lab wifi if you don't want to install everything yourself. Follow the lab setup guide for Ubuntu 22.04 when available.

3. **Learning resources**  
   Learn what ROS and Gazebo actually do before diving deep into the vehicle pack.

   - ROS 2 overview: nodes, topics, messages, services, parameters, launch files, packages, and workspaces  
   - Video: [ROS 2 Overview (in 11 minutes)](https://www.youtube.com/watch?v=0A85EcgBHT0) *(swap URL if the team uses a different link)*

## Repo pointers (after Gazebo-first reframe)

| Doc | Purpose |
|-----|---------|
| [README.md](../../README.md) | Product abstract + layout |
| [FALL_2026_BAHR_BRIEF.md](../FALL_2026_BAHR_BRIEF.md) | Fall deliverables |
| [gazebo-first design](../design/2026-09-15-gazebo-first-design.md) | Architecture |
| [gazebo-first plan](../plans/2026-09-15-gazebo-first-closed-loop.md) | Task breakdown |
| [topic map](../../ros2/topic_map/TOPICS.md) | Draft Jetson topic contract |

## Sync note

Google Doc in the autonomy team Drive folder is fine for drafting. After each meeting, mirror the notes here under `docs/context_meetings/` so GitHub stays the durable record.
