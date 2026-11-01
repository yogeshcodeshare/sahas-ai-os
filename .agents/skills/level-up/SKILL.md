---
name: level-up
description: Use when Yogesh asks to level up the Sahas AI OS, close an audit gap, find what to automate next, or improve one workflow. Walks the 3Ms (Mindset, Method, Machine) from finding the constraint to shipping one useful artifact or verified repair. Weekly on Friday afternoon, or on demand.
---

> Adapted from the AIS-OS `/level-up` skill (MIT, © 2026 Nate Herk) and The Three Ms of AI™.
> The Three Ms of AI™ is a trademark of Nate Herk. © 2026 Nate Herk. All rights reserved.

## What this skill does

Walks Yogesh through the 3Ms to surface and ship **one** new automation or repair per run.
**One interview = one artifact.** Over 4–6 runs the questions become habits, so he spots opportunities
mid-week without prompting.

Sahas AI twist: Sahas AI *sells* automation. Anything that works internally is a candidate case study or
client offer. Note that at the end, but never let it change the scoping (build for Sahas first).

## What `/level-up` is NOT
- Not `/audit`. Audit is structural ("is the OS built right?"); level-up is functional ("what leverage am I missing?"). If structure is messy, run `/audit` first.
- Not a multi-candidate planner. One run = one shipped artifact.
- Not a coach. Yogesh does the thinking; the skill runs the interview.

## When it runs
- **First run: around Day 14**, after at least one connection is wired and `/audit` has run once. Earlier gives trivial output.
- **Weekly, Friday afternoon:** review the week, pick one thing, ship Monday.
- **On demand** when a manual task itches.

## Inputs (read before asking anything)
Ask only for what these don't answer.
- vault `01_Agency/priorities.md`: what matters this quarter
- vault `01_Agency/about-yogesh.md`: `top_pain`, role
- vault `02_Clients/`, `03_Projects/` indexes: active work
- `AI OS/hot.md`, `connections.md`: what's reachable and how
- `references/3ms-framework.md` (fallback: [bundled copy](references/3ms-framework.md)): quote principles from it
- `AI OS/decisions/log.md`: what's already shipped, eliminated or considered
- `.agents/skills/*/SKILL.md` frontmatter, plus user-level skills: existing capabilities
- latest `audits/audit-*.md` if any
- n8n: existing workflows (read-only `search_workflows`) so you don't duplicate one

## Execution: three phases

### Coming from an audit
If Yogesh brings an `/audit` finding or a recent report exists, carry its evidence, affected
route/workflow and completion check into Phase 1 as the first candidate. Ask only for missing context.
- Routing-only fix → `/link`.
- Workflow repair → improve that workflow; never create a duplicate skill. A verified repair counts as the run's one artifact.
- Skip creation-only scaffolding for repairs (the frontmatter headers below are for new artifacts only, never manuals or indexes).
- Close with acceptance evidence and recommend `/audit`. Don't claim a higher score until an audit verifies it.

### Phase 1: Mindset interview (find the candidate)
Ask in order, conversationally:
1. "Walk me through your week. What did you do 3+ times?" (frequency)
2. "Anything that felt manual, boring or copy-paste?" (drudgery)
3. "Anything where you thought 'a smart intern could handle this'?" (delegation)
4. "If 10 new clients signed tomorrow, what would break first?" (constraint: onboarding, proposals, reporting, delivery?)
5. "What would bring 10 more clients tomorrow?" (growth lever: outreach, content, GMB, follow-ups?)

Quote Mindset principles when they fit:
- "Sounds like the Default Shift: to what extent could AI take this on?"
- "That's the Function Breakdown: we're automating this one piece, not the whole job."
- "AI is better than you think and improving faster. If it couldn't do this last quarter, try again."

**Output:** 1–3 candidates ranked by leverage, one line each on why. Ask: "Pick one to scope."

### Phase 2: Method interview (scope one)
**Step 1. Find the constraint.** Which bottleneck does it clear, or which growth lever does it open? Tie to Phase 1.

**Step 2. EAD: Eliminate → Automate → Delegate** (in that order).
- **Eliminate:** "What happens if we just stop doing this?" If nothing breaks → exit cheerfully. "Don't automate waste." Log the win in `decisions/log.md` and stop.
- **Automate:** apply 60/30/10 (~60% deterministic, ~30% AI-assisted with review, ~10% stays manual).
- **Delegate:** too variable or judgment-heavy → suggest a person (freelancer/VA). Log it and stop.

**Step 3. Map the process:** Trigger, Data sources, Data transformations, Decision points, Destination.
If he can't name all five: "If you can't explain it to a person, you can't explain it to an AI. Sketch it on paper, then come back." Stop.

**Step 4. Autonomy level:**

| Level | Name | What happens |
|---|---|---|
| L0 | Manual | No AI |
| L1 | Suggested | AI suggests, human decides every step |
| L2 | Drafted | AI drafts, human reviews and edits |
| L3 | Supervised | AI runs, human validates periodically |
| L4 | Autonomous | AI handles end-to-end |

**Default = lowest level that solves it.** Push back on L4 unless lower levels have been proven. Anything
that messages a client, posts publicly or touches money starts at **L1/L2**: never auto-send on a first build.
"Workflows beat agents. If a decision doesn't have to be made by AI, don't let AI make it."

**Step 5. Tie to a KPI.** Which bucket: **more clients**, **more value per client**, or **less cost/time**?
Plus a specific metric (lead response time, proposals/week, hours saved/week, GMB review count, churn).
**No bucket + metric → stop.** "If it doesn't move a number, why build it?"

**Output:** a dated Method spec in `AI OS/decisions/log.md` (constraint, EAD result, 5-element map,
autonomy level, KPI).

### Phase 3: Machine handoff (build it)
"How do you want to ship this?" Options in Boring-is-Beautiful order:
1. **Prompt-only:** a saved prompt he runs by hand. Zero infrastructure.
2. **Deterministic workflow:** a script, or an **n8n workflow** (preferred for anything that should run 24/7 or react to webhooks). No AI step.
3. **AI-assisted skill:** a SKILL.md with one AI step (draft, classify, summarise).
4. **Sub-agent:** multi-step reasoning + tools. Last resort.

**Default = the highest non-AI option that solves it.** He must explicitly choose more autonomy.

Build route:
- Skill → `skill-creator` if available; otherwise write `AI OS/.agents/skills/<name>/SKILL.md` inline. Keep it under 500 lines, with API details in `references/<tool>-api.md`.
- n8n → follow the n8n MCP's build steps (SDK reference, best practices, node types, validate, create). Leave it **unpublished/inactive** until Phase 1 validation is done.
- Credentials: names in `.env.example`, values pasted by Yogesh into `.env` or n8n credentials. Never in chat.

Every new artifact ships with these headers (in SKILL.md frontmatter, or the n8n workflow description):

```yaml
bike-method-phase: 1   # Phase 1: training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
```

Phase advances only by explicit edit after validation. If he asks to jump to Phase 4, make him read what
each phase means and confirm the lower phases are validated.

Surface the Machine principles while building:
- **Lego Principle:** smallest blocks, zero-AI steps first.
- **Validation Chain:** test each step with real output before chaining.
- **Intern Rule:** own account / least-privilege, read-only by default, never impersonates Yogesh, signs as "Sahas AI assistant".
- **Kill Switch:** if it keeps needing patches or costs more than it saves, tear it down.

## Output contract
Every run produces:
1. **One `decisions/log.md` entry:** dated, with the Method spec.
2. **One delivered improvement:** a prompt, skill, n8n workflow or agent, or a verified repair.
3. **A one-screen close:** what was scoped, what was built, the Bike Method Phase 1 reminder, and (if relevant) "this could become a client offer: note it in vault `01_Agency`?"

## Critical rules
1. One interview = one artifact.
2. Mindset phase always runs first, even if he arrives with an idea.
3. EAD: eliminate first. Eliminate is a win.
4. Lowest autonomy level that works; client-facing and money-touching starts at L1/L2.
5. Boring is Beautiful: default to the highest non-AI option.
6. KPI is mandatory.
7. `bike-method-phase: 1` on every new artifact.
8. Edit only `decisions/log.md` and the selected artifact (plus its reference doc). Everything else is read-only.
9. Local-only: no cloud routines, remote sessions or org connectors. n8n workflows stay inactive until he activates them.
10. Attribution to the 3Ms on every report and new artifact.

## Verification
- Dry run with no prompt: candidates come from his priorities, `top_pain` and recent activity. Generic ("build a daily brief") = fail.
- Eliminate test: an obviously useless task → suggests Eliminate, logs it, exits.
- L4 push-back: "auto-reply to client WhatsApps" on first build → insists on L1/L2.
- Boring test: a task solvable with a plain n8n flow → recommends option 2.
