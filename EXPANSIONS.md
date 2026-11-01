# EXPANSIONS: what to add as the Sahas AI OS grows

Adapted from the AIS-OS kit (MIT, © 2026 Nate Herk). The OS ships lean on purpose. As it grows, use
`/link` to make new sources findable and `/audit` to check they stay findable and current.

The structure should look like a small, well-run business, not a hoarder's basement.

**Sahas AI difference:** business knowledge lives in the **Obsidian vault**, not in this folder. So
several of Nate's "add as you grow" folders already exist, in the vault or the workspace. Use those;
don't create copies here.

---

## What ships (don't remove)

| Folder / file | Purpose |
|---|---|
| `CLAUDE.md` + `AGENTS.md` | Operating manual for Claude Code / Codex. Same guidance, kept in sync. |
| `aios-intake.md` | Source of truth for `/onboard`. Edit and re-run any time. |
| `hot.md` | Short summary cache. Optional; the vault wins on any conflict. |
| `connections.md` | Registry of every system the OS can reach. |
| `context/README.md` | Pointer only. Context lives in vault `01_Agency/`. |
| `references/` | 3Ms framework, API guides, licence. |
| `decisions/log.md` | Append-only record of OS decisions and `/level-up` specs. |
| `audits/` | Dated `/audit` reports (git-ignored). |
| `brainstorms/` | `/grill-me` captures (git-ignored). |
| `archives/` | Old files. Don't delete; move here. |
| `scripts/sync-codex-skills.sh` | Regenerates `.agents/skills/` from `.claude/skills/`. |
| `.claude/skills/` | `onboard`, `audit`, `level-up`, `grill-me`, `link`, `3d-brain`. Add more only when they solve a real need. |

---

## What to add as you grow

| Nate's folder | Add when | Where it goes for Sahas AI |
|---|---|---|
| `projects/` | 2+ ongoing workstreams with their own context | **Already exists:** vault `03_Projects/` (and `02_Clients/`). Don't create one here. |
| `templates/` | You copy-paste the same prompts or doc scaffolds | Prompt/output templates → `AI OS/templates/`. Note templates stay in vault `_templates/`. |
| `brand-assets/` | You generate visuals (carousels, posts, slides, GMB images) | **Already exists:** workspace `Logo/` and `Digital Scholar/Brand Kit`. Route them with `/link`; add a brand-guide note in vault `01_Agency/`. |
| `references/sops/` | You document a recurring process (client onboarding, GMB audit, proposal) | SOP **content** → vault `01_Agency/SOPs/`. The skill that runs it → `.claude/skills/`. |
| `references/{tool}-api.md` | You wire a new API (Zoho Mail, GHL, Google, WhatsApp) | Here, in `references/`. Researched once, saved forever. `/audit` rewards it. |
| `scripts/` | You write a script for an API with no lean MCP | Here, in `scripts/`. Keys from `.env`. |
| `.claude/agents/` | A repeatable multi-step research/writing job needs its own context | Here. Mirror into `.agents/` if Codex needs it. |
| Sub-OS folders (e.g. `gmb-os/`, `content-os/`) | A vertical has its own data, scripts and workflows | Here, each with its own scoped `CLAUDE.md`. The root manual stays canonical. |
| n8n workflows | A task should run 24/7 or on a webhook | In n8n, logged in `decisions/log.md` and listed in `connections.md`. |

---

## Suggested cadences

- `decisions/log.md`: every meaningful OS decision (`/level-up` Phase 2 writes these automatically).
- `hot.md`: whenever priorities change; stale after 14 days.
- `connections.md` + `references/{tool}-api.md`: every time a tool is wired.
- `/audit`: weekly (Friday) while building, then monthly.
- `/level-up`: weekly (Friday afternoon), one artifact per run.
- `archives/`: quarterly cleanup of stale skills and old intake versions.
- `CLAUDE.md` / `AGENTS.md`: quarterly review, together.
- Vault `01_Agency/priorities.md`: start of each quarter (re-run `/onboard` Q3).

---

## What NOT to add

- **No raw email/WhatsApp/chat dumps in `references/`.** Interpreted facts go to the vault; raw exports go to vault `06_Sources/` via ingest.
- **No folder-of-folders for organisation theatre.** Flat with good names beats deep nesting.
- **No `notes/`, `misc/`, `tmp/` or `inbox/` here.** The vault already has `00_Inbox` for captures.
- **No empty pre-created folders.** Add them when the OS needs them.
- **No parallel `decisions.md`.** Use `decisions/log.md` (OS) and vault `log.md` (business).
- **No forked manuals.** One `CLAUDE.md` + `AGENTS.md` pair at the root. Sub-OS folders may have scoped ones.
- **No copy of vault knowledge here.** Route to it instead.
- **No secrets, PAN, Aadhaar, bank/UPI details or client personal contacts anywhere.**

---

## When to add a folder

1. **Is it conceptually new?** Or does it fit somewhere existing (here or in the vault)?
2. **Will I touch it 3+ times in the next month?**
3. **Could `/level-up` route a future skill into it naturally?**

Two yeses: add it. One yes: wait.
