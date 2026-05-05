import socket
import threading
import random
import time
from colorama import Fore, Back, Style, init

init(autoreset=True)

# ─────────────────────────────────────────
#  SERVER SETTINGS
# ─────────────────────────────────────────
HOST = '127.0.0.1'
PORT = 5555
MAX_PLAYERS = 6
MIN_PLAYERS = 2

# ─────────────────────────────────────────
#  COLOR HELPERS
# ─────────────────────────────────────────
def gold(text):    return Fore.YELLOW + Style.BRIGHT + str(text) + Style.RESET_ALL
def red(text):     return Fore.RED    + Style.BRIGHT + str(text) + Style.RESET_ALL
def cyan(text):    return Fore.CYAN   + Style.BRIGHT + str(text) + Style.RESET_ALL
def green(text):   return Fore.GREEN  + Style.BRIGHT + str(text) + Style.RESET_ALL
def magenta(text): return Fore.MAGENTA + Style.BRIGHT + str(text) + Style.RESET_ALL
def blue(text):    return Fore.BLUE   + Style.BRIGHT + str(text) + Style.RESET_ALL
def white(text):   return Fore.WHITE  + Style.BRIGHT + str(text) + Style.RESET_ALL
def dim(text):     return Style.DIM   + str(text) + Style.RESET_ALL

# ─────────────────────────────────────────
#  STATUS EFFECTS
# ─────────────────────────────────────────
# Each effect is a dict: {"turns": int, "type": str}
# Types: "burn", "frozen", "blessed", "cursed", "poisoned", "enraged"

STATUS_INFO = {
    "burn":     {"color": red,     "emoji": "🔥", "desc": "Burning (-8 HP/turn)"},
    "frozen":   {"color": cyan,    "emoji": "❄️", "desc": "Frozen (skips next turn)"},
    "blessed":  {"color": gold,    "emoji": "✨", "desc": "Blessed (+10 ATK this turn)"},
    "cursed":   {"color": magenta, "emoji": "🌑", "desc": "Cursed (-10 DEF)"},
    "poisoned": {"color": green,   "emoji": "☠️", "desc": "Poisoned (-5 HP/turn)"},
    "enraged":  {"color": red,     "emoji": "😡", "desc": "Enraged (+15 ATK, -15 DEF)"},
}

# ─────────────────────────────────────────
#  GODS  (12 total)
# ─────────────────────────────────────────
GODS = {
    "Zeus": {
        "symbol": "⚡", "color": gold,
        "hp": 100, "attack": 30, "defense": 15,
        "special": "Lightning Storm",
        "passive": "Storm Aura",
        "passive_desc": "20% chance to reflect 10 damage back on attacker",
        "special_effect": None,
        "description": "Ruler of Olympus, master of the sky",
    },
    "Poseidon": {
        "symbol": "🌊", "color": blue,
        "hp": 110, "attack": 25, "defense": 20,
        "special": "Tsunami",
        "passive": "Tide Pull",
        "passive_desc": "Heals 5 HP at the start of every turn",
        "special_effect": "frozen",
        "description": "God of the seas and earthquakes",
    },
    "Athena": {
        "symbol": "🦉", "color": cyan,
        "hp": 90, "attack": 20, "defense": 35,
        "special": "Shield of Wisdom",
        "passive": "Tactical Mind",
        "passive_desc": "Defend action restores 5 extra HP",
        "special_effect": "blessed",
        "description": "Goddess of war strategy and wisdom",
    },
    "Ares": {
        "symbol": "⚔️", "color": red,
        "hp": 120, "attack": 38, "defense": 8,
        "special": "Blood Frenzy",
        "passive": "Bloodlust",
        "passive_desc": "Gains +3 ATK permanently each time he defeats an enemy",
        "special_effect": "enraged",
        "description": "God of war and fury",
    },
    "Hermes": {
        "symbol": "🪶", "color": white,
        "hp": 85, "attack": 28, "defense": 15,
        "special": "Divine Speed",
        "passive": "Quicksilver",
        "passive_desc": "30% chance to dodge any incoming attack",
        "special_effect": None,
        "description": "God of speed and trickery",
    },
    "Hades": {
        "symbol": "💀", "color": magenta,
        "hp": 130, "attack": 28, "defense": 22,
        "special": "Soul Drain",
        "passive": "Undying",
        "passive_desc": "Once per game, survives a killing blow with 1 HP",
        "special_effect": "cursed",
        "description": "Lord of the underworld",
    },
    "Apollo": {
        "symbol": "🌞", "color": gold,
        "hp": 95, "attack": 26, "defense": 18,
        "special": "Solar Flare",
        "passive": "Healer's Touch",
        "passive_desc": "Alliance restores 20 HP instead of 10",
        "special_effect": "burn",
        "description": "God of the sun, music, and prophecy",
    },
    "Artemis": {
        "symbol": "🌙", "color": cyan,
        "hp": 88, "attack": 32, "defense": 14,
        "special": "Moonshot",
        "passive": "Hunter's Focus",
        "passive_desc": "First attack each round always hits for maximum damage",
        "special_effect": "poisoned",
        "description": "Goddess of the hunt and the moon",
    },
    "Aphrodite": {
        "symbol": "💖", "color": magenta,
        "hp": 80, "attack": 18, "defense": 20,
        "special": "Enthrall",
        "passive": "Charm Aura",
        "passive_desc": "25% chance that an attacker skips their attack due to charm",
        "special_effect": "frozen",
        "description": "Goddess of love and desire",
    },
    "Hephaestus": {
        "symbol": "🔨", "color": red,
        "hp": 115, "attack": 24, "defense": 28,
        "special": "Forge Blast",
        "passive": "Iron Skin",
        "passive_desc": "Reduces all incoming damage by 5",
        "special_effect": "burn",
        "description": "God of fire and the forge",
    },
    "Dionysus": {
        "symbol": "🍇", "color": magenta,
        "hp": 92, "attack": 22, "defense": 16,
        "special": "Divine Madness",
        "passive": "Chaos Brew",
        "passive_desc": "Random bonus or penalty each turn (±15 HP or ATK)",
        "special_effect": "enraged",
        "description": "God of wine, madness, and festivity",
    },
    "Persephone": {
        "symbol": "🌸", "color": green,
        "hp": 98, "attack": 24, "defense": 22,
        "special": "Bloom & Wither",
        "passive": "Seasonal Shift",
        "passive_desc": "Alternates each round: even rounds +ATK, odd rounds +DEF",
        "special_effect": "poisoned",
        "description": "Queen of the underworld, goddess of spring",
    },
}

# ─────────────────────────────────────────
#  RANDOM OLYMPUS EVENTS
# ─────────────────────────────────────────
OLYMPUS_EVENTS = [
    ("Zeus sends a thunderbolt — everyone takes 10 damage!",        "damage_all",  10),
    ("Hera blesses the arena — everyone heals 15 HP!",              "heal_all",    15),
    ("The Fates intervene — turn order is shuffled!",               "shuffle",      0),
    ("Prometheus gifts fire — the current player gains +10 ATK!",   "buff_atk",    10),
    ("Pandora's box opens — a random player is poisoned!",          "random_poison", 0),
    ("A divine wind blows — all status effects are cleared!",       "clear_status",  0),
    ("The Oracle speaks — the weakest god heals 20 HP!",            "heal_weakest", 20),
    ("Ares ignites the arena — everyone is enraged for 1 turn!",    "enrage_all",   0),
]

# ─────────────────────────────────────────
#  STORY TEMPLATES
# ─────────────────────────────────────────
ATTACK_TEMPLATES = [
    "{attacker} raised their mighty hands and struck {defender} with {special}!",
    "{attacker}'s fury shook the heavens — {special} rattled {defender} to the core!",
    "Olympus trembled. {attacker} unleashed {special} upon {defender}.",
    "{attacker} let out a war cry. {special} engulfed {defender}, and the mountains wept.",
    "Stars fell from the sky as {attacker} channeled {special} into {defender}.",
]

DEFEND_TEMPLATES = [
    "{defender} staggered but did not fall — they endured {damage} damage.",
    "The prayers of mortals echoed — {defender} stood firm, taking {damage} damage.",
    "{defender} gritted their teeth. Olympus shook, but they did not. ({damage} damage)",
    "Ancient shields cracked but held. {defender} absorbed {damage} damage.",
]

DODGE_TEMPLATES = [
    "{defender} vanished like smoke — the attack passed through thin air!",
    "Swift as Hermes himself, {defender} sidestepped the blow entirely!",
    "{attacker}'s attack found only shadow — {defender} was already gone.",
]

REFLECT_TEMPLATES = [
    "{defender}'s Storm Aura crackled — the blow bounced back for {damage} damage!",
    "Lightning surrounded {defender} — the strike reversed and burned the attacker!",
]

ALLIANCE_TEMPLATES = [
    "{attacker} reached out to {defender}. 'Together we are stronger,' they said.",
    "A rare sight on Olympus: {attacker} and {defender} stood side by side.",
    "Lightning flashed in {attacker}'s eyes — in friendship, they came to aid {defender}.",
    "Even rivals can find common ground — {attacker} and {defender} clasped hands.",
]

SPECIAL_TEMPLATES = [
    "The sky was torn apart! {attacker} unleashed their legendary {special}!",
    "Time froze on Olympus. {attacker}'s {special} consumed everything in sight!",
    "Mortals would wait a thousand years to witness this — {attacker}'s {special}!",
    "The ground split open. {attacker} called upon {special} with terrifying force!",
]

ELIMINATED_TEMPLATES = [
    "{god} fell to the ground. Their light faded. Olympus will remember them.",
    "{god}'s cry echoed through the mountains — and dissolved into silence.",
    "Even gods can fall tonight. {god} has left the battlefield.",
    "The stars dimmed as {god} collapsed — a god no more, but a legend forever.",
]

WINNER_TEMPLATES = [
    "And only {god} remained standing on Olympus. The sky submitted to them.",
    "Legends were written, bards sang: {god} is the new ruler of Olympus.",
    "Though a thousand years pass, this night will not be forgotten — {god} is the god of gods.",
    "The heavens opened for {god} alone. All other gods bowed in defeat.",
]

# ─────────────────────────────────────────
#  GAME STATE
# ─────────────────────────────────────────
class GameState:
    def __init__(self):
        self.players    = {}       # {socket: {"god":str, "hp":int, "stats":dict, "status":list, "undying_used":bool}}
        self.usernames  = {}       # {socket: str}
        self.turn_order = []       # [socket, ...]
        self.round      = 0
        self.story      = []
        self.lock       = threading.Lock()
        self.phase      = "WAITING"

game = GameState()

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def send_msg(client, message):
    try:
        client.send((message + "\n").encode("utf-8"))
    except:
        pass

def broadcast_all(message):
    with game.lock:
        for c in list(game.players.keys()):
            send_msg(c, message)

def add_story(line):
    game.story.append(line)
    broadcast_all(f"  {dim('📜')} {line}")

def alive_players():
    return {s: p for s, p in game.players.items() if p["hp"] > 0}

# ─────────────────────────────────────────
#  STATUS EFFECT HELPERS
# ─────────────────────────────────────────
def apply_status(target_data, effect_type, turns=2):
    """Apply a status effect to a player dict."""
    # Don't stack the same effect
    for s in target_data["status"]:
        if s["type"] == effect_type:
            s["turns"] = max(s["turns"], turns)
            return
    target_data["status"].append({"type": effect_type, "turns": turns})

def has_status(player_data, effect_type):
    return any(s["type"] == effect_type for s in player_data["status"])

def tick_status(attacker_socket):
    """Apply per-turn status effects and decrement counters."""
    player   = game.players[attacker_socket]
    god_name = player["god"]
    expired  = []
    messages = []

    for status in player["status"]:
        stype = status["type"]
        info  = STATUS_INFO[stype]

        if stype == "burn":
            player["hp"] -= 8
            messages.append(red(f"  {info['emoji']} {god_name} is burning! -8 HP"))
        elif stype == "poisoned":
            player["hp"] -= 5
            messages.append(green(f"  {info['emoji']} {god_name} is poisoned! -5 HP"))

        status["turns"] -= 1
        if status["turns"] <= 0:
            expired.append(status)
            messages.append(dim(f"  {god_name}'s {stype} wore off."))

    for s in expired:
        player["status"].remove(s)

    for msg in messages:
        broadcast_all(msg)

    # Poseidon passive: heal 5 HP at start of turn
    if GODS[god_name]["passive"] == "Tide Pull":
        player["hp"] = min(GODS[god_name]["hp"] + 50, player["hp"] + 5)
        broadcast_all(cyan(f"  🌊 {god_name}'s Tide Pull: +5 HP"))

    # Dionysus passive: random chaos
    if GODS[god_name]["passive"] == "Chaos Brew":
        roll = random.randint(1, 4)
        if roll == 1:
            player["hp"] += 15
            broadcast_all(magenta(f"  🍇 Chaos Brew blesses {god_name}! +15 HP"))
        elif roll == 2:
            player["hp"] -= 15
            broadcast_all(magenta(f"  🍇 Chaos Brew punishes {god_name}! -15 HP"))

    # Persephone passive
    if GODS[god_name]["passive"] == "Seasonal Shift":
        if game.round % 2 == 0:
            broadcast_all(green(f"  🌸 Seasonal Shift: {god_name} is in Summer — ATK boosted this turn!"))
        else:
            broadcast_all(green(f"  🌸 Seasonal Shift: {god_name} is in Winter — DEF boosted this turn!"))

# ─────────────────────────────────────────
#  OLYMPUS RANDOM EVENT
# ─────────────────────────────────────────
def trigger_olympus_event(current_attacker_socket):
    """15% chance each round to trigger a random Olympus event."""
    if random.random() > 0.15:
        return

    event_text, event_type, value = random.choice(OLYMPUS_EVENTS)
    broadcast_all("\n" + gold("  ═" * 26))
    broadcast_all(gold(f"  ⚡ OLYMPUS EVENT: {event_text}"))
    broadcast_all(gold("  ═" * 26) + "\n")
    add_story(f"[Divine Intervention] {event_text}")

    alive = alive_players()

    if event_type == "damage_all":
        for s, p in alive.items():
            p["hp"] -= value
        broadcast_all(red(f"  All gods take {value} damage!"))

    elif event_type == "heal_all":
        for s, p in alive.items():
            p["hp"] += value
        broadcast_all(green(f"  All gods heal {value} HP!"))

    elif event_type == "shuffle":
        random.shuffle(game.turn_order)
        broadcast_all(cyan("  Turn order has been reshuffled!"))

    elif event_type == "buff_atk":
        if current_attacker_socket in game.players:
            apply_status(game.players[current_attacker_socket], "blessed", turns=1)
            broadcast_all(gold("  The current player gains a blessed boost!"))

    elif event_type == "random_poison":
        target_socket = random.choice(list(alive.keys()))
        apply_status(game.players[target_socket], "poisoned", turns=2)
        god = game.players[target_socket]["god"]
        broadcast_all(green(f"  {god} is poisoned by Pandora's box!"))

    elif event_type == "clear_status":
        for s, p in alive.items():
            p["status"].clear()
        broadcast_all(cyan("  All status effects cleared!"))

    elif event_type == "heal_weakest":
        weakest = min(alive.items(), key=lambda x: x[1]["hp"])
        weakest[1]["hp"] += value
        broadcast_all(green(f"  {weakest[1]['god']} (the weakest) healed {value} HP!"))

    elif event_type == "enrage_all":
        for s, p in alive.items():
            apply_status(p, "enraged", turns=1)
        broadcast_all(red("  All gods are enraged for this turn!"))

# ─────────────────────────────────────────
#  END-GAME GENERATORS
# ─────────────────────────────────────────
def generate_epitaph(username, god_name, god_data, stats):
    symbol = god_data["symbol"]
    color  = god_data["color"]
    kills     = stats.get("kills", 0)
    damage    = stats.get("damage_dealt", 0)
    alliances = stats.get("alliances", 0)
    specials  = stats.get("specials_used", 0)
    survived  = stats.get("survived", False)
    dodges    = stats.get("dodges", 0)

    if survived:       title = "Ruler of Olympus"
    elif kills >= 3:   title = "The Godslayer"
    elif kills >= 2:   title = "Champion of War"
    elif alliances >= 2: title = "Herald of Peace"
    elif specials >= 3:  title = "Master of the Divine Arts"
    elif dodges >= 2:    title = "The Untouchable"
    else:              title = "Honorable Warrior"

    lines = [
        color("╔══════════════════════════════════════════╗"),
        color(f"  {symbol}  EPITAPH OF {god_name.upper()} — {username}"),
        color("  ══════════════════════════════════════"),
        f"  Total damage dealt   : {gold(damage)}",
        f"  Gods defeated        : {red(kills)}",
        f"  Alliances formed     : {green(alliances)}",
        f"  Special powers used  : {magenta(specials)}",
        f"  Attacks dodged       : {cyan(dodges)}",
        "",
        f"  Olympus remembered them as:",
        gold(f'  "{title}"'),
        color("╚══════════════════════════════════════════╝"),
    ]
    return "\n".join(lines)

def generate_epic():
    lines = "\n".join(f"    {line}" for line in game.story)
    return (
        "\n" + gold("═"*52) + "\n" +
        gold("           ⚡  THE EPIC OF OLYMPUS  ⚡") + "\n" +
        gold("═"*52) + "\n\n" +
        lines + "\n\n" +
        gold("═"*52) + "\n" +
        dim("   This epic was written so the last battle\n"
            "   of the gods shall never be forgotten.") + "\n" +
        gold("═"*52) + "\n"
    )

# ─────────────────────────────────────────
#  MOVE PROCESSING
# ─────────────────────────────────────────
def process_move(attacker_socket, move, target_socket=None):
    attacker      = game.players[attacker_socket]
    attacker_god  = attacker["god"]
    attacker_data = GODS[attacker_god]
    stats         = attacker["stats"]
    color         = attacker_data["color"]

    # ── Attack ──────────────────────────────
    if move == "1":
        if target_socket is None or target_socket not in game.players:
            send_msg(attacker_socket, red("⚠️  Invalid target."))
            return False

        target     = game.players[target_socket]
        target_god = target["god"]
        target_data = GODS[target_god]

        # Aphrodite charm passive: 25% chance attacker is charmed
        if target_data["passive"] == "Charm Aura" and random.random() < 0.25:
            broadcast_all(magenta(f"  💖 {attacker_god} is charmed by {target_god} and cannot attack!"))
            add_story(f"{attacker_god} was charmed by {target_god}'s aura and hesitated.")
            return False

        # Hermes dodge passive: 30% chance to dodge
        if target_data["passive"] == "Quicksilver" and random.random() < 0.30:
            broadcast_all(white(f"  🪶 {target_god} dodges the attack!"))
            add_story(random.choice(DODGE_TEMPLATES).format(
                attacker=attacker_god, defender=target_god))
            target["stats"]["dodges"] = target["stats"].get("dodges", 0) + 1
            return False

        # Calculate damage
        base_atk = attacker_data["attack"]
        if has_status(attacker, "blessed"):   base_atk += 10
        if has_status(attacker, "enraged"):   base_atk += 15
        if has_status(attacker, "cursed"):    base_atk -= 10
        if attacker_data["passive"] == "Seasonal Shift" and game.round % 2 == 0:
            base_atk += 8
        if attacker_data["passive"] == "Hunter's Focus":
            # First attack of the round: max damage
            base_atk_val = base_atk + 5
        else:
            base_atk_val = random.randint(max(1, base_atk - 5), base_atk + 5)

        base_def = target_data["defense"]
        if has_status(target, "cursed"):  base_def -= 10
        if has_status(target, "enraged"): base_def -= 15
        if attacker_data["passive"] == "Seasonal Shift" and game.round % 2 != 0:
            base_def += 8
        if target_data["passive"] == "Iron Skin":
            base_def += 5  # handled as flat reduction below

        damage = max(1, base_atk_val - max(0, base_def // 4))
        if target_data["passive"] == "Iron Skin":
            damage = max(1, damage - 5)

        target["hp"] -= damage
        stats["damage_dealt"] = stats.get("damage_dealt", 0) + damage

        # Zeus reflect passive
        if target_data["passive"] == "Storm Aura" and random.random() < 0.20:
            reflect = 10
            attacker["hp"] -= reflect
            broadcast_all(gold(f"  ⚡ Storm Aura reflects {reflect} damage back at {attacker_god}!"))
            add_story(random.choice(REFLECT_TEMPLATES).format(
                defender=target_god, damage=reflect))

        # Story line
        add_story(random.choice(ATTACK_TEMPLATES).format(
            attacker=attacker_god, defender=target_god,
            special=attacker_data["special"], damage=damage))
        add_story(random.choice(DEFEND_TEMPLATES).format(
            defender=target_god, damage=damage))
        broadcast_all(red(f"  💥 {target_god}'s HP: {max(0, target['hp'])}"))

        # Apply special effect on attack
        if attacker_data["special_effect"]:
            apply_status(target, attacker_data["special_effect"], turns=2)
            eff = attacker_data["special_effect"]
            info = STATUS_INFO[eff]
            broadcast_all(info["color"](f"  {info['emoji']} {target_god} is now {eff}! ({info['desc']})"))

        # Elimination check
        if target["hp"] <= 0:
            # Hades undying passive
            if target_data["passive"] == "Undying" and not target.get("undying_used"):
                target["hp"] = 1
                target["undying_used"] = True
                broadcast_all(magenta(f"  💀 {target_god}'s Undying passive triggers — survives with 1 HP!"))
                add_story(f"{target_god} cheated death through the power of Undying!")
                return False

            stats["kills"] = stats.get("kills", 0) + 1
            # Ares bloodlust: gain +3 ATK permanently
            if attacker_data["passive"] == "Bloodlust":
                attacker_data["attack"] += 3
                broadcast_all(red(f"  ⚔️ Bloodlust! {attacker_god}'s ATK permanently increased to {attacker_data['attack']}!"))

            add_story(random.choice(ELIMINATED_TEMPLATES).format(god=target_god))
            broadcast_all(red(f"\n  ☠️  {target_god} ({game.usernames[target_socket]}) has been eliminated!\n"))
            send_msg(target_socket, magenta("\n  💀 You have fallen... But Olympus will not forget you.\n"))
            return True

    # ── Defend ──────────────────────────────
    elif move == "2":
        heal = random.randint(10, 20)
        if attacker_data["passive"] == "Tactical Mind":
            heal += 5
        attacker["hp"] = min(attacker_data["hp"] + 50, attacker["hp"] + heal)
        add_story(f"{attacker_god} gathered their strength and restored {heal} HP.")
        broadcast_all(green(f"  💚 {attacker_god}'s HP: {attacker['hp']}"))

    # ── Alliance ────────────────────────────
    elif move == "3":
        if target_socket is None or target_socket not in game.players:
            send_msg(attacker_socket, red("⚠️  Invalid target."))
            return False
        target_god = game.players[target_socket]["god"]
        add_story(random.choice(ALLIANCE_TEMPLATES).format(
            attacker=attacker_god, defender=target_god))
        stats["alliances"] = stats.get("alliances", 0) + 1
        heal = 20 if attacker_data["passive"] == "Healer's Touch" else 10
        attacker["hp"] = min(attacker_data["hp"] + 50, attacker["hp"] + heal)
        game.players[target_socket]["hp"] = min(
            GODS[target_god]["hp"] + 50,
            game.players[target_socket]["hp"] + heal)
        broadcast_all(green(f"  🤝 Both gods gained {heal} HP from the alliance."))

    # ── Special power ───────────────────────
    elif move == "4":
        add_story(random.choice(SPECIAL_TEMPLATES).format(
            attacker=attacker_god, special=attacker_data["special"]))
        stats["specials_used"] = stats.get("specials_used", 0) + 1
        damage = random.randint(18, 28)
        for s, p in list(game.players.items()):
            if s != attacker_socket and p["hp"] > 0:
                p["hp"] -= damage
                stats["damage_dealt"] = stats.get("damage_dealt", 0) + damage
                if attacker_data["special_effect"]:
                    apply_status(p, attacker_data["special_effect"], turns=2)
                    eff  = attacker_data["special_effect"]
                    info = STATUS_INFO[eff]
                    broadcast_all(info["color"](
                        f"  {info['emoji']} {p['god']} is now {eff}!"))
                broadcast_all(red(f"  💥 {p['god']} took {damage} dmg! HP: {max(0, p['hp'])}"))

    # ── Steal (bonus move 5) ─────────────────
    elif move == "5":
        # Steal up to 20 HP from target
        if target_socket is None or target_socket not in game.players:
            send_msg(attacker_socket, red("⚠️  Invalid target."))
            return False
        steal = random.randint(10, 20)
        target = game.players[target_socket]
        actual = min(steal, target["hp"])
        target["hp"] -= actual
        attacker["hp"] += actual
        stats["damage_dealt"] = stats.get("damage_dealt", 0) + actual
        add_story(f"{attacker_god} drained {actual} HP from {target['god']} through dark sorcery!")
        broadcast_all(magenta(f"  🌑 {attacker_god} stole {actual} HP! "
                               f"({target['god']}: {max(0, target['hp'])} HP)"))

    return False

# ─────────────────────────────────────────
#  GAME LOOP
# ─────────────────────────────────────────
def game_loop():
    time.sleep(1)
    broadcast_all("\n" + gold("═"*52))
    broadcast_all(gold("  ⚡  MYTHOS — THE EPIC OF OLYMPUS BEGINS  ⚡"))
    broadcast_all(gold("═"*52))
    add_story("A great storm broke over Olympus. The gods were summoned to the arena.")
    add_story("Who shall rule? Who shall fall? The epic is being written now...")
    broadcast_all(gold("═"*52) + "\n")
    time.sleep(2)

    first_round = True

    while True:
        alive = alive_players()
        if len(alive) <= 1:
            break

        game.round += 1
        broadcast_all(f"\n{cyan('─'*40)}")
        broadcast_all(gold(f"  🏛️   ROUND {game.round}"))
        broadcast_all(cyan("─"*40))

        # Olympus event (not on first round)
        if not first_round:
            current = game.turn_order[0] if game.turn_order else None
            trigger_olympus_event(current)
        first_round = False

        # Update turn order
        game.turn_order = [s for s in game.turn_order if s in alive_players()]

        for attacker_socket in list(game.turn_order):
            alive = alive_players()
            if attacker_socket not in alive:
                continue
            if len(alive) <= 1:
                break

            attacker      = game.players[attacker_socket]
            attacker_god  = attacker["god"]
            god_data      = GODS[attacker_god]
            color         = god_data["color"]

            # Tick status effects
            tick_status(attacker_socket)

            # Skip turn if frozen
            if has_status(attacker, "frozen"):
                broadcast_all(cyan(f"  ❄️  {attacker_god} is frozen and loses their turn!"))
                # Remove frozen
                attacker["status"] = [s for s in attacker["status"] if s["type"] != "frozen"]
                continue

            opponents = {s: p for s, p in alive.items() if s != attacker_socket}

            # ── Battlefield status ───────────
            turn_label = color(god_data['symbol'] + ' ' + attacker_god + "'s turn")
            broadcast_all(f"\n  {turn_label}  ({game.usernames[attacker_socket]})")
            broadcast_all(dim("  " + "─"*40))
            status_str = "  Battlefield: " + " | ".join(
                f"{GODS[p['god']]['color'](p['god'])} {GODS[p['god']]['symbol']} {p['hp']} HP"
                + (f" [{','.join(s['type'] for s in p['status'])}]" if p["status"] else "")
                for s, p in alive.items()
            )
            broadcast_all(status_str + "\n")

            # ── Move menu to active player ───
            send_msg(attacker_socket, color("  Your move:"))
            send_msg(attacker_socket,
                     "  [1] Attack    [2] Defend    [3] Alliance    [4] Special Power    [5] Steal HP")

            if opponents:
                send_msg(attacker_socket, "\n  Choose target:")
                opp_list = list(opponents.items())
                for i, (s, p) in enumerate(opp_list):
                    status_tag = f" [{','.join(st['type'] for st in p['status'])}]" if p["status"] else ""
                    send_msg(attacker_socket,
                             f"  [{i+1}] {GODS[p['god']]['color'](p['god'])} ({game.usernames[s]}) — {p['hp']} HP{status_tag}")
            send_msg(attacker_socket,
                     "\n  Enter move and target (e.g. '1 2' = Attack target 2): ")

            for s in list(game.players.keys()):
                if s != attacker_socket and game.players.get(s, {}).get("hp", 0) > 0:
                    send_msg(s, dim(f"  ⏳ {attacker_god} is thinking..."))

            # ── Read input ───────────────────
            try:
                attacker_socket.settimeout(30)
                data = attacker_socket.recv(1024).decode("utf-8").strip()
                attacker_socket.settimeout(None)
            except:
                data = "2"

            parts     = data.split()
            move      = parts[0] if parts else "2"
            target_idx = int(parts[1]) - 1 if len(parts) > 1 else 0

            target_socket = None
            if move in ["1", "3", "5"] and opponents:
                opp_keys      = list(opponents.keys())
                target_socket = opp_keys[target_idx % len(opp_keys)]

            process_move(attacker_socket, move, target_socket)
            time.sleep(1.5)

    # ─────────────────────────────────────────
    #  GAME OVER
    # ─────────────────────────────────────────
    game.phase = "ENDED"
    alive = alive_players()

    broadcast_all("\n" + gold("═"*52))
    broadcast_all(gold("  ⚡  THE BATTLE HAS ENDED  ⚡"))
    broadcast_all(gold("═"*52))

    if alive:
        winner_socket = list(alive.keys())[0]
        winner        = game.players[winner_socket]
        winner["stats"]["survived"] = True
        add_story(random.choice(WINNER_TEMPLATES).format(god=winner["god"]))
        broadcast_all(gold(f"\n  🏆 WINNER: {winner['god']}  ({game.usernames[winner_socket]})\n"))

    broadcast_all(generate_epic())

    broadcast_all("\n" + gold("═"*52))
    broadcast_all(gold("  📜  PERSONAL EPITAPHS"))
    broadcast_all(gold("═"*52))
    for s, p in game.players.items():
        broadcast_all(generate_epitaph(
            game.usernames[s], p["god"], GODS[p["god"]], p["stats"]))
        time.sleep(0.6)

    broadcast_all(gold("\n  Olympus will remember you all forever. 🏛️\n"))

# ─────────────────────────────────────────
#  CLIENT HANDLER
# ─────────────────────────────────────────
def handle_client(client, address):
    print(f"[+] New connection: {address}")
    try:
        send_msg(client, "\n" + gold("⚡  MYTHOS — THE EPIC OF OLYMPUS  ⚡"))
        send_msg(client, gold("═"*44))
        send_msg(client, "Enter your username: ")
        username = client.recv(1024).decode("utf-8").strip() or f"God_{random.randint(100,999)}"

        send_msg(client, f"\n{gold('Welcome,')} {username}! Choose your god:\n")
        for i, (name, data) in enumerate(GODS.items(), 1):
            send_msg(client,
                     data["color"](f"  [{i:>2}] {data['symbol']}  {name}  —  {data['description']}"))
            send_msg(client,
                     dim(f"        HP:{data['hp']}  ATK:{data['attack']}  DEF:{data['defense']}  "
                         f"Special: {data['special']}  |  Passive: {data['passive']} — {data['passive_desc']}"))
        send_msg(client, f"\nYour choice (1-{len(GODS)}): ")

        choice   = client.recv(1024).decode("utf-8").strip()
        god_list = list(GODS.keys())
        try:
            god_name = god_list[int(choice) - 1]
        except:
            god_name = random.choice(god_list)

        god_data = GODS[god_name]

        with game.lock:
            game.players[client] = {
                "god":  god_name,
                "hp":   god_data["hp"],
                "status": [],
                "undying_used": False,
                "stats": {
                    "kills": 0, "damage_dealt": 0, "alliances": 0,
                    "specials_used": 0, "survived": False, "dodges": 0
                }
            }
            game.usernames[client] = username
            game.turn_order.append(client)

        send_msg(client, f"\n{green('✅')} {god_data['symbol']}  {gold(god_name)} selected!\n")
        broadcast_all(gold(f"  ⚡ {god_name} ({username}) has entered the arena!"))
        broadcast_all(dim(f"  ({len(game.players)}/{MIN_PLAYERS} players connected)"))

        if len(game.players) >= MIN_PLAYERS and game.phase == "WAITING":
            game.phase = "PLAYING"
            threading.Thread(target=game_loop, daemon=True).start()

        while game.phase != "ENDED":
            time.sleep(1)

    except Exception as e:
        print(f"[!] Error ({address}): {e}")
    finally:
        with game.lock:
            game.players.pop(client, None)
            game.usernames.pop(client, None)
            if client in game.turn_order:
                game.turn_order.remove(client)
        client.close()
        print(f"[-] Connection closed: {address}")

# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_PLAYERS)
    print(f"[*] MYTHOS server running at {HOST}:{PORT}")
    print(f"[*] Game starts when {MIN_PLAYERS} players connect.\n")
    while True:
        client, address = server.accept()
        threading.Thread(target=handle_client, args=(client, address), daemon=True).start()

if __name__ == "__main__":
    start_server()
