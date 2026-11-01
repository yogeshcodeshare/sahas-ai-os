---
name: grill-me
description: Interview Yogesh relentlessly about a plan, design or topic, checkpointing every answer to a brainstorm file so nothing is lost. Use when he wants to stress-test a plan (offer, pricing, client build, GMB Sarathi), run a discovery session, get what's in his head into notes, build up AI OS context over time, or says "grill me".
---

> Adapted from the AIS-OS `/grill-me` skill (MIT, © 2026 Nate Herk).

# Grill Me

Interview Yogesh about every branch of the topic until there's shared understanding, resolving dependencies
one by one. The real goal is to **get what's in his head into a durable markdown file** so nothing is
lost as context fills up.

## The capture file is the whole point
Checkpoint to disk after **every** answer. The file, not your context, is the source of truth. Never make
him ask you to save.

## Existing context
Read `AI OS/CLAUDE.md` and `hot.md`, then only the vault notes relevant to the topic (via `MOC.md` and
folder `_index.md`) and prior captures in `AI OS/brainstorms/`. Reuse known facts; ask about gaps,
changes, decisions and trade-offs.

## Setup (before Q1)
1. Create `AI OS/brainstorms/{YYYY-MM-DD}-{topic-slug}.md` (get the date from the shell: `Get-Date -Format yyyy-MM-dd`).
   Never overwrite. Same date/topic → add a time suffix. Resume an old capture only if he asks; read it and continue numbering.
   No topic given → `untitled-discovery`, goal pending, then ask what to explore.
2. Write the header immediately: title, date, goal, status, empty "Open flags".
3. Tell him the path in one line. Then ask Q1.

## Checkpoint rule (non-negotiable)
After every answer, before the next question:
- Append an entry: topic, key facts/decisions (his words where wording matters), flags (what he couldn't answer → who can).
- Update the running summary. If a later answer corrects an earlier one, mark the old entry superseded and link to the new one.
- Read the saved entry back. If saving fails, say so, keep the answer visible in chat, and don't keep collecting answers.

One answer per write, never batched.

## Interview method
- **One question at a time.** For decisions, offer a suggested answer grounded in context, labelled as a suggestion. For business facts, ask neutrally; never save your guess as his answer.
- Keep confirmed facts, tentative ideas, your suggestions and open questions clearly separate.
- Settle upstream decisions first.
- If a file, vault note or the code can answer it, read that instead of asking.
- Can't answer → flag with an owner (him, a client, a vendor) and move on.
- Stop immediately when he says stop. Near the end ask "anything we haven't touched?"

## Capture file structure
```
# {Topic}: Brainstorm / Discovery Notes
Date: {date} · Goal: {one line}
Status: in progress / paused / complete
Context sources: {vault notes used}

## Summary / key decisions
## Q&A log
### Q1 - {topic}
- Asked:
- Captured:
- Tentative / suggested:
- Flags:
## Open flags (pending input)
- {item} -> {who}
```

## At the end or on pause
- Check the capture for contradictions; mark unresolved ones, don't pick for him. Update status and resume point.
- If the session was about building AI OS context: merge **only user-confirmed** durable facts into the right
  **vault** note (following the vault `CLAUDE.md`: pull first, front-matter, append a dated update section,
  never delete; `source: brainstorm <path>`), then commit and push the vault. Log meaningful decisions in
  `AI OS/decisions/log.md` (business decisions in the vault `log.md`).
- Otherwise keep the capture as the output. Suggest `/link` to route a useful result or `/level-up` to act on it. Don't run either automatically.
- Recap: clickable capture path, notes actually updated, open flags, next step.

## Boundaries
- Local capture and requested vault updates only. No publishing, messages or external writes.
- Never record credentials, PAN, Aadhaar, bank/UPI details, or clients' personal contact details. Redact and say so.
- Captures are dated interview evidence, not automatically current truth.
