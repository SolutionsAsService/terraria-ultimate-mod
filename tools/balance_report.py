#!/usr/bin/env python3
"""Compare the SHADW mods' weapon damage against the reference power curve, per rarity tier; optionally write the clamped values back.

usage: balance_report.py <mod repo> [<mod repo> ...]            report only
       balance_report.py --apply <mod repo> [...]                clamp each weapon into the reference band [p25, p75] of its rarity tier (edits content/items.json)

The band is the reference mod's own spread at that rarity, so a weapon is neither the weakest nor the strongest of its tier unless the content author means it:
use "balance": "keep" on an item to opt out. Rarities with fewer than 8 reference weapons are skipped (too thin to trust).
"""
import json, sys
from pathlib import Path

CURVE = json.load(open(Path(__file__).resolve().parent.parent / "balance" / "calamity-power-curve.json"))["damage_by_rarity"]


def main(argv):
    apply = "--apply" in argv
    for repo in [a for a in argv if a != "--apply"]:
        path = Path(repo) / "content" / "items.json"
        items = json.load(open(path))
        changed = 0
        print(f"== {repo}")
        for it in items:
            if not it.get("damage"):
                continue
            c = CURVE.get(it.get("rarity", "White"))
            if not c or c["n"] < 8 or it.get("balance") == "keep":
                continue
            lo, hi = round(c["p25"]), round(c["p75"])
            d = it["damage"]
            flag = "ok" if lo <= d <= hi else ("HIGH" if d > hi else "low")
            new = min(max(d, lo), hi)
            print(f"  {it['id']:24} {it.get('rarity','White'):9} {d:4}  band {lo}-{hi}  median {c['median_damage']:.0f}  {flag}" + (f"  -> {new}" if new != d else ""))
            if apply and new != d:
                it["damage"] = new
                changed += 1
        if apply and changed:
            json.dump(items, open(path, "w"), indent=2, ensure_ascii=False)
            open(path, "a").write("\n")
            print(f"  wrote {changed} change(s)")


if __name__ == "__main__":
    main(sys.argv[1:])
