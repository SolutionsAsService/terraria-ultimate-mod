# terraria-ultimate-mod

The unified **Ultimate** pack for Terraria (tModLoader 1.4.4): our three content mods (**Khemet**, **Olympia**, **The Wilds Beyond**) balanced against each other and against the two big content mods, **Calamity** and **Thorium**, and extended to talk to them.

**Status: foundation.** The balance tooling exists and has run; the unified mod, the compatibility layer and the Thorium data do not yet. See [VISION.md](VISION.md) and [DESIGN.md](DESIGN.md).

## What is here

| | |
|---|---|
| `tools/extract_power_curve.py` | reads a reference mod's source and writes only **numbers** (weapon damage by rarity, boss stats) |
| `balance/calamity-power-curve.json` | that table for Calamity (732 weapons, 49 bosses; only 6 bosses have a literal life in source) |
| `tools/balance_report.py` | compares our mods' weapons with the curve per rarity tier; `--apply` clamps into the reference band |
| `pack.json` | the dependency manifest (mods the player subscribes to; none are redistributed) |

## First finding

Against Calamity's spread at the same rarity, our weapons run **1.2x to 2.0x** its median, and the top tier overshoots most: Sun Staff 170 and Thunderbolt of Zeus 176 against a Red-rarity band of 55 to 150; Labrys 42 and Hellfang Blade 46 against an Orange band of 16 to 32. `balance_report.py` lists every one. Nothing has been changed yet: rarity is a crude proxy for progression, and nothing has been play-tested.
