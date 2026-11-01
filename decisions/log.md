# Decisions log (AI OS)

Append-only record of meaningful decisions about the **OS itself** and why. `/level-up` Phase 2 writes
scoped automation specs here. Business decisions go to the vault `log.md`.

**Format per entry:**

```
## YYYY-MM-DD: Short title

**Decision:** what was decided.
**Why:** the reasoning, constraints, and what would change your mind.
**Alternatives considered:** what else was on the table.
**Owner:** who's accountable.
```

Keep it short. Capture the *why*, not just the *what*.

---

## 2026-11-01: Vault is the brain, AI OS is the operator

**Decision:** Keep the existing Obsidian vault as the single source of business knowledge. `AI OS/` holds only skills, connections, references, decisions and audits, and points to the vault.
**Why:** Avoids two drifting copies of business facts; the vault is already read by Codex/Hermes and synced via private Git.
**Alternatives considered:** Nate's default `context/` folder inside the OS (rejected: duplication).
**Owner:** Yogesh

## 2026-11-01: Sahas accounts only

**Decision:** Sahas identity = hello@sahasai.in for Google tools, Zoho Mail API for email. Personal Gmail and employer (work) accounts are never connected.
**Why:** Keeps business, personal and employer data separate.
**Alternatives considered:** Personal Gmail (rejected).
**Owner:** Yogesh

## 2026-11-01: Local-only mode

**Decision:** No cloud routines, remote sessions, artifacts or org connectors while on the employer-org Claude account. Cadence = local scheduled tasks or n8n.
**Why:** The confidentiality boundary in the workspace root `CLAUDE.md`.
**Alternatives considered:** Cloud routines (revisit after moving to a personal Claude subscription).
**Owner:** Yogesh

## 2026-11-01: APIs over MCP, least privilege

**Decision:** Wire tools via direct API + a saved `references/{tool}-api.md`, with dedicated read-only keys first.
**Why:** Fewer tokens, narrower blast radius (Intern Rule).
**Alternatives considered:** MCP servers for everything.
**Owner:** Yogesh

## 2026-11-01: Full AIS-OS kit adopted

**Decision:** Adopt all six AIS-OS skills (`onboard`, `audit` rubric v2, `level-up`, `grill-me`, `link`, `3d-brain`), the Codex mirror (`AGENTS.md`, `.agents/skills/`, sync script), `EXPANSIONS.md` and `README.md`, adapted to Sahas AI routes.
**Why:** Tool-agnostic (Claude Code or Codex) and evidence-based audits from day one.
**Alternatives considered:** A trimmed three-skill version (first draft, superseded).
**Owner:** Yogesh

## 2026-11-01: Onboarded into existing vault notes

**Decision:** `/onboard` reused existing vault notes instead of creating `about-sahas-ai.md`: business context is appended to `01_Agency/sahas-ai-overview.md`; new notes `about-yogesh.md`, `priorities.md`, `voice-samples.md`. Routes in both manuals, `context/` and the onboard skill now point there.
**Why:** No duplicate business notes; the overview already has backlinks.
**Alternatives considered:** A fresh `about-sahas-ai.md` (rejected: duplication).
**Owner:** Yogesh
