# Sahas AI OS

Yogesh's personal AI Operating System for **Sahas AI**, built on Nate Herk's
[AIS-OS](https://github.com/nateherkai/AIS-OS) starter kit (MIT). It works in Claude Code (`CLAUDE.md`,
`.claude/skills/`) and Codex (`AGENTS.md`, `.agents/skills/`).

**Local only.** No cloud routines, remote sessions or org connectors. The only git remote is the vault's
private GitHub repo.

## Two layers
- **Brain:** the Obsidian vault (`..\Ai Automation\SahasAI_Automation_Obsidian_Valut\...`). All business knowledge.
- **Operator:** this folder. Skills, connections, API references, decisions, audits. It points to the vault and never copies it.

## The litmus test
> While you're not at your desk, the OS observes one real-world event and produces an output that's faster
> and more accurate than what you'd produce yourself.

## Two frameworks
**Three Ms (how you think)**, in `references/3ms-framework.md`:

| M | One-liner |
|---|---|
| Mindset | Default Shift, Function Breakdown, Curiosity Rule. *To what extent can AI be leveraged here?* |
| Method | Find the constraint → Eliminate/Automate/Delegate → map the process → pick autonomy level → tie to a KPI |
| Machine | Lego Principle, Validation Chain, Bike Method, Intern Rule, Kill Switch. *Boring is beautiful.* |

**Four Cs (what you build):**

| # | Layer | "In place" test |
|---|---|---|
| 1 | Context | A fresh session answers "what does Sahas AI do and for whom?" without browsing |
| 2 | Connections | "What's on my calendar tomorrow and what's due?" gives live data, no pasting |
| 3 | Capabilities | A short phrase triggers a multi-step workflow that produces an artifact |
| 4 | Cadence | Something useful runs on schedule without being asked (local task / n8n) |

Context can't be skipped. Connections and Capabilities can grow in parallel. Cadence comes last: don't
schedule what doesn't work manually.

> The Three Ms of AI™ and The Four Cs of an AI OS™ are trademarks of Nate Herk. © 2026 Nate Herk.

## Skills

| Skill | When |
|---|---|
| `/onboard` | Day 1, and whenever offer or priorities change. 7 questions → vault `01_Agency/` |
| `/grill-me` | Any time you want to unpack a plan or add context. Saves every answer to `brainstorms/` |
| `/audit` | Day 7, after a fix, and weekly. Rubric v2, read-only, saves to `audits/` |
| `/link` | When adding a project, file, folder or source to the routing |
| `/level-up` | Day 14, then every Friday. One 3Ms interview = one shipped artifact |
| `/3d-brain` | Explore the vault as a local 3D knowledge globe (Node 22+) |

In Codex, use `$onboard`, `$audit`, etc. After editing a skill in `.claude/skills/`, run
`bash scripts/sync-codex-skills.sh <skill-name>` to refresh its Codex copy.

## First steps
1. Fill in `aios-intake.md` (voice dictation is fine; paste writing samples raw).
2. Run `/onboard`.
3. Use it for a week with real questions; log decisions.
4. Day 2: wire one connection (`connections.md` recipe).
5. Day 7: `/audit`. Pick one gap.
6. Day 14: `/level-up`. Build one thing.

## How you'll know it's working
1. **Asked before you:** when someone asks you a business question, you check the OS first because it answers faster and with sources.
2. **Fewer tabs:** your first move on anything new is to ask the OS, not to open six apps.
3. **Knowledge leaves your head:** you stop trying to remember decisions and client details; you trust retrieval.

See `EXPANSIONS.md` for what to add as it grows.
