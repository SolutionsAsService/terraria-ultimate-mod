#!/usr/bin/env python3
"""Extract a power curve from a reference mod's source: weapon damage by rarity, and boss life/damage/defense.

Only NUMBERS are read (damage, use time, rarity name, life, defense); no code, text or art is copied. Reference use only: the reference mod's licence
(Calamity Mod, Azafure LLC) allows its source to be used as a reference and forbids redistributing it, so this tool writes a small table of figures and nothing else.

usage: extract_power_curve.py <path to a mod source tree> <out.json>
"""
import json, re, statistics, sys
from collections import defaultdict
from pathlib import Path

VANILLA_ORDER = ["White", "Blue", "Green", "Orange", "LightRed", "Pink", "LightPurple", "Lime", "Yellow", "Cyan", "Red", "Purple"]


def num(rx, text):
    m = re.search(rx, text)
    return int(m.group(1)) if m else None


def main(src, out):
    src = Path(src)
    weapons, bosses = [], []
    for p in src.joinpath("Items", "Weapons").rglob("*.cs"):
        t = p.read_text(encoding="utf-8-sig", errors="ignore")
        dmg = num(r"Item\.damage\s*=\s*(\d+)\s*;", t)
        if dmg is None:
            continue
        rare = re.search(r"Item\.rare\s*=\s*(?:ItemRarityID\.(\w+)|ModContent\.RarityType<(\w+)>|RarityType<(\w+)>)", t)
        rname = next((g for g in rare.groups() if g), None) if rare else None
        weapons.append({"name": p.stem, "class": p.parent.name, "damage": dmg, "use_time": num(r"Item\.useTime\s*=\s*(\d+)\s*;", t) or num(r"Item\.useAnimation\s*=\s*(\d+)\s*;", t),
                        "rarity": rname, "vanilla_rarity": bool(rare and rare.group(1))})
    for p in src.joinpath("NPCs").rglob("*.cs"):
        t = p.read_text(encoding="utf-8-sig", errors="ignore")
        if "NPC.boss = true" not in t:
            continue
        life, dmg, dfn = num(r"NPC\.lifeMax\s*=\s*(\d+)\s*;", t), num(r"NPC\.damage\s*=\s*(\d+)\s*;", t), num(r"NPC\.defense\s*=\s*(\d+)\s*;", t)
        bosses.append({"name": p.stem, "life": life, "damage": dmg, "defense": dfn})
    by = defaultdict(list)
    for w in weapons:
        if w["rarity"]:
            by[w["rarity"]].append(w["damage"])
    curve = {r: {"n": len(v), "median_damage": statistics.median(v), "p25": statistics.quantiles(v, n=4)[0] if len(v) > 3 else min(v), "p75": statistics.quantiles(v, n=4)[2] if len(v) > 3 else max(v)} for r, v in by.items()}
    json.dump({"source": "reference mod source, numbers only", "weapons": sorted(weapons, key=lambda w: w["damage"]), "bosses": sorted([b for b in bosses if b["life"]], key=lambda b: b["life"]), "damage_by_rarity": curve,
               "vanilla_rarity_order": VANILLA_ORDER}, open(out, "w"), indent=1)
    print(f"{len(weapons)} weapons, {len(bosses)} bosses ({sum(1 for b in bosses if b['life'])} with a literal life)")
    for r in VANILLA_ORDER:
        if r in curve:
            c = curve[r]
            print(f"  {r:10} n={c['n']:3} median damage {c['median_damage']:6.1f}  (p25 {c['p25']:.0f}, p75 {c['p75']:.0f})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
