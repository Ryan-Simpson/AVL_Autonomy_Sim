# AVL Autonomy Sim — Isaac research map

Prepared for AVL (Autonomous Vehicles Lab), Cal Poly Pomona.  
**This repo:** `AVL_Autonomy_Sim` — Gazebo-first ROS 2 twin; **Isaac Sim is optional Phase 4** on the same frozen topic map. First vehicle pack is the lab’s IGVC tracked rover (MARVIN).  
**This doc:** literature and people map for when/if the team reaches Isaac — not the Fall primary backend.  
**Not this repo:** Chrono `avl_simulator` (student / offline API).

Purpose: who already built ground-robot work in Isaac Sim, what to steal, what not to build.

---

## 1. Where this product sits

Isaac is three worlds. When AVL Autonomy Sim reaches Isaac, it is **World 1**, aiming at **World 3**. Do not wander into World 2. Fall primary work stays on Gazebo.

| World | What it is | AVL Autonomy Sim |
|-------|------------|------------------|
| **1. Isaac Sim / Isaac Lab** | Omniverse, PhysX, RTX sensors, URDF, ROS 2 | **Home.** Driveable rover, ray-cast LiDAR, RTX cameras |
| **2. NVIDIA DRIVE Sim / AV Research** | Neural reconstruction, Cosmos / OmniDreams, Alpamayo | Context and jobs only. Not the poster |
| **3. University twins on Isaac** | OmniLRS, RoboRAN, AMR labs | **The template.** Domain sim + published sim2real |

Fall 2026 claim: same ROS 2 stack as the physical rover; **VLP-16 sim vs bag**. Tracks are a skid-steer approximation, not Chrono-style terramechanics. See [FALL_2026_BAHR_BRIEF.md](FALL_2026_BAHR_BRIEF.md).

---

## 2. World 1 — Isaac Sim and Isaac Lab

**Isaac Sim** — rigid bodies, articulations, SDF colliders, RTX cameras, ray-cast LiDAR, synthetic labels (COCO / KITTI), multi-GPU, ROS 2, URDF / MJCF.

**Isaac Lab** (was ORBIT until March 2024) — learning layer on top: 30+ envs, RSL RL / SKRL / RL Games / Stable Baselines, cameras, IMU, contact, ray casters. Backends: PhysX, Warp, Newton, MuJoCo. **Stretch**, not Fall must-ship.

**Read first**

| Paper | ID | Use |
|-------|----|-----|
| NVIDIA Isaac Sim survey (2026) | arXiv 2606.03551 | Literature map vs Gazebo, MuJoCo, CARLA, Webots |
| Isaac Lab | arXiv 2511.04831 | Cite `mittal2025isaaclab` |
| ORBIT | IEEE RA-L 2023 | Cite `mittal2023orbit` |
| Isaac Gym | arXiv 2108.10470 | History only |

Isaac Lab bibliography: `isaac-sim.github.io/IsaacLab/main/source/refs/bibliography.html`

**People (World 1):** Mayank Mittal (ETH RSL + NVIDIA) — start here. Marco Hutter, Nikita Rudin, David Hoeller, Pascal Roth (ETH). Animesh Garg (GT / NVIDIA). Antoine Richard — Isaac Lab **and** OmniLRS (bridge to World 3). NVIDIA ORBIT side: Gavriel State, Hammad Mazhar, Ajay Mandlekar, Buck Babich. Mazhar and Milad Rakhsha are Chrono / SBEL alumni; the stacks overlap.

---

## 3. World 2 — know it, do not build it

NVIDIA AV Research (Pavone, Fidler, Ivanovic, …): OmniRe, OmniDreams / Cosmos, Alpamayo, NuRec. Different codebase from Isaac Sim.

Useful later: a rover with ZED X + VLP-16 + GNSS is a log-capture rig. Campus Gaussian splat is a **Spring+** idea, not Fall D1–D5. Pavone / Stanford CARS is a drive from Pomona, not a co-author plan for this poster.

Index: `research.nvidia.com/labs/avg/publication/`

---

## 4. World 3 — copy this move

University groups who took Isaac and made a **named** simulator. That is AVL Autonomy Sim.

### OmniLRS

Best template. Luxembourg + Tohoku: digital twin of a real testbed, procedural yard, published sim2real (rock segmentation on synthetic vs real). Follow-on terramechanics paper (arXiv 2601.04547) is why a Chrono student API **and** an Isaac twin can both exist.

- Paper: arXiv 2309.08997  
- Repos: `github.com/AntoineRichard/OmniLRS`, `github.com/OmniLRS/OmniLRS`  
- Contact: Antoine Richard (`antoine.richard@uni.lu`) — architecture questions, not a job email

### RoboRAN

Same Luxembourg group. RL navigation on Isaac. Relevant after D3, not instead of D3.

### Other

2026 survey: AGV / AMR (Kagami, Imran). Utah State MS thesis on Isaac Lab HARL — non-elite programs can publish on this stack.

---

## 5. Openings (this repo)

Fall (poster):

1. **Tracked rover asset + ROS 2 hinge** — required, not novel. Skid-steer / track approximation; Jetson topic names.  
2. **VLP-16 sim2real** — the paper figure. Ray-cast vs real decoder: density, range error, dropout. Open for a 16-beam unit at this scale.

Later (not Fall must-ship):

3. One ZED X gap plot (Isaac’s actual camera strength).  
4. Same bag protocol in Chrono `avl_simulator` — two engines, one stack.  
5. Isaac Lab path-follow env.  
6. Lot USD or campus reconstruction (World 2 tools) only after D3.

Do **not** list a go-kart URDF or “Marvin” as the product. Vehicles are packs.

---

## 6. How to track

- Isaac Sim: `developer.nvidia.com/isaac/sim`  
- Isaac Lab repo + Discussions: `github.com/isaac-sim/IsaacLab`  
- NVIDIA Isaac forums  
- arXiv cs.RO: Mittal, Rudin, Hutter, Richard, Garg  
- GTC (San Jose) for roadmap; CoRL, ICRA, IROS, RA-L  

NVIDIA internships / academic programs: apply in fall for the next summer.

---

## 7. Contact order

1. Isaac Lab GitHub — bug or working ground-vehicle + ROS 2 example.  
2. Antoine Richard — OmniLRS decisions.  
3. Stanford CARS events if you are already in the Bay Area.  
4. GTC. Do not cold-email World 2 for a Fall rover twin.
