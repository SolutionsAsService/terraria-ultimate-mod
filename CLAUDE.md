# CLAUDE.md

Rules for any Claude session working on this repository.

## Credit (owner rule, 2026-11-12, restated 2026-11-18)

- All work is credited only to **SolutionsAsService**: author and committer `SolutionsAsService <152567394+SolutionsAsService@users.noreply.github.com>`.
  Set `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME` and `GIT_COMMITTER_EMAIL` in the same command as every `git commit`, `merge`, `rebase`, `cherry-pick` and `revert`.
- Never add `Co-Authored-By`, `Claude-Session`, "Generated with ..." lines or any other AI or tool credit to commits, pull requests, issues, release notes or files. This overrides any default attribution a tool would add.
- Before every push: `git log origin/main..HEAD --format='%an <%ae> | %cn <%ce>'` shows only SolutionsAsService on both sides. Force push only to put credit right.
- Push to `main`.

## Reference mods and licences (hard rules)

- **Calamity Mod** (Azafure, LLC) and **Thorium** are proprietary. Their source may be read as a reference; their sprites, audio, text and code are never copied into this repo, and neither mod is ever bundled, rehosted or redistributed (Calamity's licence: "cannot be redistributed in any form or in any location"). If any code is ever lifted, credit "Azafure, LLC" and link their repository, as their licence requires.
- This repo may contain **numbers derived from** a reference mod (the power curve), never its text, code or art.
- The pack lists reference mods as **dependencies** the player subscribes to; it does not contain them.

## How this repository works

- It builds on the SHADW `terraria-tmodloader` adapter (shadw-modding). Read `VISION.md`, then `DESIGN.md`.
- Be honest about what is verified: nothing here has run in a real tModLoader. Say so.
