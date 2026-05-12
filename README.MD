# ⚡ MYTHOS — The Epic of Olympus

> *A great storm broke over Olympus. The gods were summoned to the arena.*
> *Who shall rule? Who shall fall? The epic is being written now...*

```
  ╔══════════════════════════════════════════════════╗
  ║     ⚡  MYTHOS — THE EPIC OF OLYMPUS  ⚡           ║
  ║   A multiplayer terminal battle game in Python   ║
  ╚══════════════════════════════════════════════════╝
```

Mythos is a multiplayer terminal battle game where **2–6 players** connect over TCP sockets, choose a Greek god, and fight to the death in a turn-based arena. Each god has unique passive abilities, special powers, and narrative story templates. Every move is etched into the Epic of Olympus.

---

## 🗂️ Table of Contents

- [Features](#-features)
- [Gods](#%EF%B8%8F-gods)
- [Status Effects](#-status-effects)
- [Olympus Events](#%EF%B8%8F-olympus-events)
- [Installation](#-installation)
- [How to Play](#%EF%B8%8F-how-to-play)
- [Technical Architecture](#%EF%B8%8F-technical-architecture)
- [File Structure](#-file-structure)

---

## ✨ Features

- 🧵 **Multiplayer** — 2 to 6 players, connected in real time over TCP sockets
- ⚡ **12 unique gods** — each with distinct HP/ATK/DEF stats, a special power, and a passive ability
- 🔥 **6 status effects** — Burn, Frozen, Blessed, Cursed, Poisoned, Enraged
- 🌩️ **Olympus Events** — random divine interventions with a 15% chance each round
- 📜 **Epics & Epitaphs** — at game end, an auto-generated *Epic of Olympus* recounts every battle event; each player receives a personal epitaph with stats and a legendary title
- 🎨 **Colorful terminal UI** — full ANSI color, symbols, and emojis via `colorama`
- ⏱️ **30-second move timer** — if a player times out, the server auto-selects Defend

---

## ⚔️ Gods

| # | God | Symbol | HP | ATK | DEF | Special Power | Passive |
|---|-----|--------|-----|-----|-----|---------------|---------|
| 1 | Zeus | ⚡ | 100 | 30 | 15 | Lightning Storm | Storm Aura — 20% chance to reflect 10 damage back |
| 2 | Poseidon | 🌊 | 110 | 25 | 20 | Tsunami | Tide Pull — Heals 5 HP at the start of every turn |
| 3 | Athena | 🦉 | 90 | 20 | 35 | Shield of Wisdom | Tactical Mind — Defend restores 5 extra HP |
| 4 | Ares | ⚔️ | 120 | 38 | 8 | Blood Frenzy | Bloodlust — Gains permanent +3 ATK per kill |
| 5 | Hermes | 🪶 | 85 | 28 | 15 | Divine Speed | Quicksilver — 30% chance to dodge any attack |
| 6 | Hades | 💀 | 130 | 28 | 22 | Soul Drain | Undying — Once per game, survives a killing blow with 1 HP |
| 7 | Apollo | 🌞 | 95 | 26 | 18 | Solar Flare | Healer's Touch — Alliance heals 20 HP instead of 10 |
| 8 | Artemis | 🌙 | 88 | 32 | 14 | Moonshot | Hunter's Focus — First attack each round always hits for max damage |
| 9 | Aphrodite | 💖 | 80 | 18 | 20 | Enthrall | Charm Aura — 25% chance an attacker is charmed and skips their attack |
| 10 | Hephaestus | 🔨 | 115 | 24 | 28 | Forge Blast | Iron Skin — All incoming damage reduced by 5 |
| 11 | Dionysus | 🍇 | 92 | 22 | 16 | Divine Madness | Chaos Brew — Random ±15 HP or ATK bonus/penalty each turn |
| 12 | Persephone | 🌸 | 98 | 24 | 22 | Bloom & Wither | Seasonal Shift — Even rounds: +ATK; odd rounds: +DEF |

---

## 🔥 Status Effects

| Effect | Emoji | Description |
|--------|-------|-------------|
| `burn` | 🔥 | -8 HP per turn |
| `frozen` | ❄️ | Skips next turn |
| `blessed` | ✨ | +10 ATK this turn |
| `cursed` | 🌑 | -10 DEF |
| `poisoned` | ☠️ | -5 HP per turn |
| `enraged` | 😡 | +15 ATK, -15 DEF |

The same effect cannot stack — applying it again only refreshes the duration.

---

## ⛈️ Olympus Events

Each round has a **15% chance** of triggering a divine intervention:

| Event | Effect |
|-------|--------|
| ⚡ Zeus sends a thunderbolt | All gods take 10 damage |
| 💚 Hera blesses the arena | All gods heal 15 HP |
| 🔀 The Fates intervene | Turn order is shuffled |
| 🔥 Prometheus gifts fire | The active player gains `blessed` |
| ☠️ Pandora's box opens | A random player is poisoned |
| 🌬️ A divine wind blows | All status effects are cleared |
| 🌟 The Oracle speaks | The weakest god heals 20 HP |
| 😡 Ares ignites the arena | All gods are enraged for 1 turn |

---

## 🚀 Installation

### Requirements

- Python 3.8+
- `colorama` library

### Steps

```bash
# Clone the repository
git clone https://github.com/ozgemelteminan/olympus-arena.git
cd olympus-arena

# Install dependencies
pip install colorama

# Start the server
python server.py
```

Then, in a **separate terminal window for each player**:

```bash
python client.py
```

> By default the server runs on `127.0.0.1:5555`.  
> To play over a network, update the `HOST` value in both `server.py` and `client.py` to the server machine's IP address.

---

## 🕹️ How to Play

### Connecting & Choosing a God

1. Run `python client.py` to connect to the server
2. Enter your username
3. Browse the god roster and pick a number (1–12)
4. The game starts automatically once a second player connects

### Move System

On your turn, choose from five actions:

```
  [1] Attack       — Pick a target and deal damage
  [2] Defend       — Recover 10–20 HP
  [3] Alliance     — Choose an ally; both of you heal 10 HP
  [4] Special      — Unleash your god's power on all enemies (18–28 dmg)
  [5] Steal HP     — Drain 10–20 HP from a target and add it to your own
```

**Input format:** `<move> <target>` — e.g. `1 2` (attack player 2), `2` (defend)

### End of Game

The last god standing rules Olympus. After the final blow:

- 🏆 **Winner announcement**
- 📜 **The Epic of Olympus** — a full narrative of every battle event
- 🪦 **Personal Epitaphs** — each player's stats and their earned legendary title

Example titles: `"The Godslayer"`, `"Herald of Peace"`, `"The Untouchable"`, `"Ruler of Olympus"`

---

## 🏛️ Technical Architecture

```
┌─────────────┐        TCP/5555        ┌──────────────────────────┐
│  client.py  │ ◄────────────────────  │        server.py         │
│             │                        │                          │
│  - Send     │ ──────────────────────►│  handle_client()         │
│  - Receive  │                        │  game_loop()             │
└─────────────┘                        │  process_move()          │
                                       │  tick_status()           │
┌─────────────┐        TCP/5555        │  trigger_olympus_event() │
│  client.py  │ ◄────────────────────  │                          │
│  (player 2) │ ──────────────────────►│  GameState               │
└─────────────┘                        │  (shared, Lock-protected)│
     ...                               └──────────────────────────┘
```

- The **server** spawns a dedicated thread per client via `threading.Thread`
- **Game state** lives in a single `GameState` object, kept thread-safe with `threading.Lock`
- **Turn order** is tracked in a list; eliminated players are removed each round
- **Broadcasting** — every message is sent to all connected players simultaneously via `broadcast_all()`
- **Input timeout** — `socket.settimeout(30)` enforces the 30-second move limit server-side

### Modules Used

| Module | Purpose |
|--------|---------|
| `socket` | TCP connection management |
| `threading` | Per-client threads and `Lock`-based synchronization |
| `random` | Damage rolls, event selection, narrative template picks |
| `time` | Pacing delays between turns (`sleep`) |
| `colorama` | Cross-platform ANSI color codes |

---

## 📁 File Structure

```
olympus-arena/
├── server.py      # All game logic, server loop, and state management
└── client.py      # Lightweight terminal client — send and receive
```

---

This project was developed for **CMPE322 — Computer Networks**.  
It demonstrates core networking concepts — TCP sockets, client-server architecture, and multi-threaded connection handling — through an interactive game.

---

<div align="center">

*⚡ Olympus will remember you all forever. 🏛️*

</div>
