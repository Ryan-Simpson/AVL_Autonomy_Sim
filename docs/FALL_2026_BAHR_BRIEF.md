# AVL Autonomy Sim — Fall 2026 Research Brief

**For:** Dr. Behnam Bahr, Autonomous Vehicles Lab  
**Platform:** NVIDIA Isaac Sim + ROS 2 Humble  
**Product:** AVL Autonomy Sim  
**First vehicle pack:** IGVC tracked rover (tank treads)

Chrono `avl_simulator` is a separate student API.

## Abstract

This work presents AVL Autonomy Sim, a digital twin platform in NVIDIA Isaac Sim for Cal Poly Pomona’s Autonomous Vehicles Lab. The twin is built so the same ROS 2 autonomy stack that runs on the lab’s Jetson computers can be developed in a GPU-rendered environment before a field test. The first vehicle pack is a roughly 49 kg differential tank-tread rover with a Velodyne VLP-16, three Stereolabs ZED X cameras, an Xsens MTi-680G with GNSS, and dual track encoders. In Isaac Sim that rover is modeled as a skid-steer vehicle with measured sensor mounts; tank belts are approximated rather than simulated as a full track-soil system. A thin ROS 2 bridge uses the physical robot’s topic names—commanding left and right tracks from `/cmd_vel` or Teensy-style L/R RPM and publishing `/odom`, `/imu/data`, `/gps/fix`, `/velodyne_points`, and ZED image streams—so onboard software does not require a simulation-only fork. The evaluation compares simulated VLP-16 point clouds to recordings from the real sensor on a repeatable course and reports range error, point density, and dropout. The goal is a closed-loop, honestly labeled twin of the lab’s tracked rover, not a photoreal campus reconstruction or a learned driving policy.

## Research question

If the Jetson stack talks to Isaac through the same ROS 2 topics as the physical rover, how large is the VLP-16 (and optional ZED X) sim-to-real gap?

## Deliverables

| ID | Deliverable |
|----|-------------|
| D1 | Tracked rover drives in Isaac (skid-steer / track approximation, measured mounts) |
| D2 | ROS 2 hinge with Jetson topic names |
| D3 | VLP-16 sim-vs-bag figure |
| D4 | Research poster |
| D5 | 4–6 page paper draft |
