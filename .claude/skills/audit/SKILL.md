---
name: audit
description: Use when Yogesh asks to audit the Sahas AI OS, score the Four Cs (Context, Connections, Capabilities, Cadence), find stale paths or unlinked vault/project material, compare CLAUDE.md and AGENTS.md routing, or for the weekly Friday review. Read-only toward the system; automatically saves a dated report to audits/ and tracks findings across runs.
---

> Adapted from the AIS-OS `/audit` skill (MIT, © 2026 Nate Herk), rubric v2. See `references/AIS-OS-LICENSE.txt`.

# Sahas AI OS Audit

Check whether this AI OS can find the right information and do useful work reliably for Sahas AI, and
name the changes that would make Yogesh's work easier. Score **Context, Connections, Capabilities and
Cadence out of 25 each** using [rubric.md](rubric.md) (**v2**). Label the number **verified operational
reliability**, not overall usefulness. A folder, installed skill, API key or confident claim is not proof
of a working system.

Run locally in this project. No subagents unless Yogesh asks. Audit first; `/link` repairs a route and
`/level-up` closes one meaningful gap. Never inflate or deflate a score to encourage another run.

**Every audit saves its report in `AI OS/audits/`.** Read [history.md](history.md) for prior-report
selection, finding IDs and transitions, comparison rules and safe saving. Saving is part of this skill,
not a separate approval step. An explicit "don't save" overrides it. Nothing else changes.

## Sahas AI scope (read this first)

This OS has **two roots**. Audit both, as one system:

| Part | Path | Manuals |
|---|---|---|
| Operator | `C:\Yogesh - personal\Claude\Cluade Projects\AI OS` | `CLAUDE.md`, `hot.md`, `connections.md`, `.claude/skills/` |
| Brain (vault) | `C:\Yogesh - personal\Claude\Cluade Projects\Ai Automation\SahasAI_Automation_Obsidian_Valut\SahasAI_Automation_Obsidian_Valut` | vault `CLAUDE.md`, `AGENTS.md` (Codex/Hermes), `MOC.md`, folder `_index.md` files |

Also respect the workspace root `C:\Yogesh - personal\Claude\Cluade Projects\CLAUDE.md` (confidentiality
rules). Its local-only constraint is an **intentional design choice**, not a defect:
- Cadence's "intended unattended environment" is **this laptop** (local scheduled tasks) or **n8n**.
  Do not penalise or recommend cloud routines, remote sessions, artifacts or org connectors.
- `hot.md` is an optional cache. Per the rubric it earns no points for existing. Check it against the vault
  and flag drift; never recommend deleting it automatically.
- Runtimes: Claude Code operates `AI OS/`; the vault is also read by Codex and Hermes via `AGENTS.md`.
  Compare shared rules (privacy list, pull/push, note format) between vault `CLAUDE.md` and `AGENTS.md`.
  `AI OS/` has `CLAUDE.md` + `AGENTS.md`, which must carry the same guidance. Intentional differences:
  the root-manual load line (Codex must read it explicitly) and the skills path (`.agents/skills`).
  Also check `.agents/skills/` matches `.claude/skills/` after the documented path transform.

Do not `git pull`, commit or push during an audit. Read the vault as it is on disk and note if
`git status` shows it behind or dirty.

## 1. Establish scope and evidence
- Get the current date. Read the manuals above. Load the latest `audit_kind: aios` report and carried
  ledger from `audits/` per [history.md](history.md) **before** choosing probes.
- Use routing first: `AI OS/CLAUDE.md` → vault `MOC.md` → folder `_index.md` → notes. List immediate child
  folders of `01_Agency`, `02_Clients`, `03_Projects`, `04_Knowledge`, `05_Agent-Memory` after reading their
  indexes. Skip `.obsidian`, `.git`, `_templates`, `archives`, `node_modules`.
- Identify Yogesh's role, Sahas AI's offer, current priorities (`01_Agency/priorities.md`) and up to three
  important workflows from real context. Unfilled placeholders don't count.
- Inspect skill registries (`AI OS/.claude/skills`, plus user-level skills that matter, e.g.
  `ingest-sahasai-obsidian`), `connections.md`, `references/*-api.md`, and actual scheduler evidence
  (local scheduled tasks list and run history, n8n workflows/executions if the n8n MCP is reachable;
  read-only calls only).
- Record each finding as **verified**, **documented but unverified**, **missing**, **stale** or
  **conflicting**, with file/line or dated run reference.
- Privacy sweep (sampled): flag any PAN, Aadhaar, bank/UPI ID, key/token, or client personal contact
  detail found in the vault or `AI OS/`. Report the file and line only, **never the value**. This is a
  confirmed defect affecting C4 (source authority) and N4 (action boundaries).

## 2. Test routing and context retrieval
Make a compact map: **need → manual/index → source → freshness rule**. Then run five probes through the
declared routes, adapted to Sahas AI:

1. What does Sahas AI sell, to whom, and what matters this quarter?
2. Where is the authoritative current priority or commitment, and how would I verify it?
3. For one active project (e.g. GMB Sarathi) or client: latest deliverable and next step?
4. Where is a past decision or lesson (vault `log.md`, `05_Agent-Memory`, `AI OS/decisions/log.md`) and its source?
5. Where is a commonly needed external record or asset (proposal, invoice tracker, logo/brand file, client
   folder) and how is it accessed?

For each: question, route tried, source, result, and **direct / fallback search / not found**. A broad
search that finds the answer doesn't prove the route works. Check freshness explicitly (front-matter
`updated:`, dates inside notes) and whether a fresh session could resume a project without this chat.

## 3. Verify the other three Cs
First run the [routing and compatibility checks](compatibility.md) for the runtimes above.

**Connections:** the 7 domains (revenue, customer/CRM, calendar, communication, tasks, meetings,
knowledge/files) plus any material extra (e.g. content/social for Sahas AI's own marketing). For each:
relevance, mechanism, route, successful-read evidence and date, limits. A `.env` key or MCP listing does
not prove auth. Use only narrow read-only checks; never print secrets or bulk private records.
Allowed accounts are hello@sahasai.in (Google tools), Zoho Mail, and Sahas-owned tools. **Any connection
using the personal Gmail or an employer (work) account is a confirmed defect.**

**Capabilities:** up to three workflows tied to stated priorities (chosen before looking at outputs).
Check trigger, inputs, output destination, real outputs, verification, failure handling, repeated use.
Missing workflows stay gaps. Don't run paid or side-effecting work to audit it.

**Cadence:** actual enabled local scheduled tasks, n8n schedules/triggers, hooks, or an explicit human
ritual (e.g. Friday `/audit` + `/level-up`) and their execution records. Manual rituals get limited credit,
labelled manual. A local task only runs while the laptop is awake; say so.

## 4. Score and prioritise
Read the full [rubric.md](rubric.md). Assign all 20 criteria (0/1/3/5 only), apply the caps, show four
subtotals, raw sum, caps with reasons, final score and stage. Distinguish **unverified** from **known
broken**. Rank gaps by effect on Yogesh's work (wrong or stale answers and missing access first). Up to
three concrete fixes, each labelled repair / verify / optional, with a completion check. Don't invent
three faults in a healthy system. Group findings into confirmed defects, verification gaps, improvement
opportunities; list intentional differences (local-only, the two documented CLAUDE/AGENTS differences) separately. Stable IDs
`AIOS-<run-id>-NN`, reused across sections.

## 5. Report (chat concise, saved file complete)
1. **AIOS Audit: date, Sahas AI OS, rubric v2.** Scope, runtimes, limits, plain conclusion: what works and the most consequential mismatch.
2. **CLAUDE.md / AGENTS.md findings.** Name each manual inspected (operator `CLAUDE.md`, operator `AGENTS.md`, vault `CLAUDE.md`, vault `AGENTS.md`, workspace `CLAUDE.md`) as checked / missing / not checked, then the table:

   | File and section/line | Rule or missing route | Finding and practical effect | Recommended change |
   |---|---|---|---|

   Separate problems in the manual from problems in files it routes to. Say what the manuals do well. If none: "No operating-manual issues found in the inspected scope." End with "No operating manuals were changed."
3. **Routing and compatibility** matrix and findings from [compatibility.md](compatibility.md).
4. **Routing check:** five probes with direct/fallback/unresolved.
5. **What works:** up to three evidence-backed strengths.
6. **Verified operational reliability:** four rows `/25` with criterion IDs and points, raw total, caps, final `/100`, stage.
7. **Top improvements:** up to three ranked actions with evidence, next action, benefit and completion check.
8. **Progress since the previous audit:** per [history.md](history.md). No prior report = first recorded baseline.
9. **Next run:** a ready `/level-up` prompt carrying the top gap (or `/link <target> <purpose>` for a routing-only fix).
10. **Saved record:** write with [templates/report.md](templates/report.md) to `audits/audit-YYYY-MM-DD-HHMMSS-<suffix>.md` (UTC, exclusive create), read it back, and link the saved path. Never say saved without confirming it.

Recommend re-running `/audit` after the chosen fix and weekly (Friday) during setup.

**Read-only:** no repairs, moves, installs, scheduler changes, messages, git operations or external writes.
The only write is the new report under `audits/`. Redact secrets and private records. Don't update the
vault, `hot.md` or `decisions/log.md` from audit observations.
