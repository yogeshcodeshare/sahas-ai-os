---
name: onboard
description: Use on Day 1 of the Sahas AI OS, or when Yogesh says "set me up", "onboard me", "let's get started", "fill in my AIOS", or when his offer, clients or priorities change. Combined wizard that runs the 7-question intake AND scaffolds the Day-1 context into the Obsidian vault. Idempotent; re-run any time after editing aios-intake.md.
---

> Adapted from the AIS-OS `/onboard` skill (MIT, © 2026 Nate Herk) and The Three Ms of AI™. See `references/AIS-OS-LICENSE.txt`.

## What this skill does

One combined wizard. Reads or writes `aios-intake.md` (the canonical intake, in this folder), runs the
7-question interview for anything not yet answered, then writes the Day-1 context set **into the Sahas AI
vault** in one batch. The vault is the brain; this folder never holds a parallel copy of business facts.

**The wow moment:** at the end, suggest *"Try this: ask me what should I focus on this week?"* Yogesh runs
it once. The answer must sound like a teammate who knows Sahas AI, not a stranger.

## When NOT to run this

- Already onboarded and wants a refresh: still run, but skip answered questions (idempotent).
- Wants to add a new connection: that isn't onboarding. Point him to `connections.md`, or `/level-up`.
- Wants to dump a lot of knowledge on one topic: use `/grill-me` instead.

## Routes (Sahas AI layout, overrides the starter-kit defaults)

Vault root: `C:\Yogesh - personal\Claude\Cluade Projects\Ai Automation\SahasAI_Automation_Obsidian_Valut\SahasAI_Automation_Obsidian_Valut`

| Starter kit | Sahas AI destination |
|---|---|
| `context/about-me.md` | vault `01_Agency/about-yogesh.md` |
| `context/about-business.md` | vault `01_Agency/about-sahas-ai.md` |
| `context/priorities.md` | vault `01_Agency/priorities.md` |
| `references/voice.md` | vault `01_Agency/voice-samples.md` |
| `connections.md` | `AI OS/connections.md` (operator layer) |
| operating manual | `AI OS/CLAUDE.md` + `AI OS/AGENTS.md` (Context summary + Voice, kept identical) and `AI OS/hot.md` |

Before writing anything, read the vault's `CLAUDE.md` and the `_index.md` of each folder you'll write
into. **If an equivalent note already exists** (e.g. an agency overview under another name), update
that note instead of creating a duplicate, and tell Yogesh which note you used.

## Execution

### Step 0: Sync and read
1. `git pull` in the vault (vault golden rule: pull before you read).
2. Read `AI OS/CLAUDE.md`, the vault `CLAUDE.md`, `MOC.md`, and `01_Agency/_index.md`.
3. If `aios-intake.md` is missing, create it from the [intake template](assets/aios-intake.md) (7 sections with
   `[Your answer here]` placeholders). Pre-fill only answers clearly supported by existing vault notes,
   with a `(source: <note path>)` reference; leave everything else for the interview.

### Step 1: Read the intake
Check which Q1–Q7 have real content vs `[Your answer here]`.
- **All filled** → skip to Step 3.
- **Some filled** → "I see Q1, Q3, Q4 are answered. Fill the rest now, or scaffold from what's there?" His call.
- **None filled** → run Step 2.

### Step 2: The interview (7 questions, hard cap)
Ask **one at a time**. Write each answer into `aios-intake.md` immediately so he can resume if
interrupted. Encourage voice dictation and long answers.

**Q1. Who are you, what does Sahas AI sell, and who do you sell it to?**
Identity, offer (services, packages, typical price range), ICP (industry, size, city/region, who signs).
One paragraph each is fine.

**Q2. Paste 1–2 things you've written recently. Don't edit them.**
*The only question with a hard rule.* Samples must be pasted, not typed during this chat. If he starts
typing fresh prose, refuse:
> "Stop, paste it raw. If you type it here while we're talking, it's already shaped by our conversation.
> Open your last client WhatsApp/email, LinkedIn or Instagram post, or proposal and paste the unedited text.
> This is the one rule I can't bend."

Ask for two, and for where each was used (client message, social post, proposal). Note the language too
(English / Hinglish / Marathi), since tone differs by channel.

**Q3. What are your 2–3 biggest priorities for the next 90 days?**
Push back on vague answers like "grow Sahas AI". Make him name a number, a deadline or a deliverable
(e.g. "3 new retainer clients by 31 Jan", "GMB Sarathi v1 live by 15 Dec").

**Q4. Where does revenue actually land, and where is it tracked?**
e.g. Razorpay / bank transfers / UPI, invoices in Zoho Invoice/Books or a sheet, GHL. → Domain 1.
**Never record account numbers, UPI IDs, PAN or bank details**, only the tool names.

**Q5. Where do you talk to clients, collaborators and the outside world day-to-day?**
e.g. Zoho Mail (hello@sahasai.in), WhatsApp / WhatsApp Business, GHL conversations, Instagram/Facebook DMs,
phone. → Domains 2 + 4.

**Q6. Where do meeting recordings, notes and important docs live?**
e.g. Google Meet recordings or a transcript tool, Google Drive on hello@sahasai.in, the vault, local
folders. → Domains 6 + 7.

**Q7. What's the one task that eats your week, and where do you track work?**
Capture `top_pain` (used by `/level-up`) + Domain 5 (tasks: GHL, a sheet, Notion, the vault, a notebook).

Domain 3 (Calendar) is inferred: Google Calendar on hello@sahasai.in unless he says otherwise. Confirm in Step 3.

Leave out PAN, Aadhaar, bank/UPI details, keys, and clients' personal phone numbers, emails, addresses or
health details. If he gives one, drop it and say so.

### Step 3: Scaffold the Day-1 context (one batch)
Once the intake is complete, write all of these in a single pass, with no multi-turn confirmation:

1. **`01_Agency/about-yogesh.md`**: from Q1 (identity, role) + Q7 (`top_pain`). One short paragraph each,
   plus a "Working with me" line if he stated preferences.
2. **`01_Agency/about-sahas-ai.md`**: from Q1 (offer, ICP) + Q4 (revenue model, tool names only).
3. **`01_Agency/priorities.md`**: from Q3. Numbered list, one line each, with deadline and measure.
4. **`01_Agency/voice-samples.md`**: from Q2. Samples **verbatim**, each with channel, language and date,
   under a header: "Match this register when drafting. Never send anything in my voice to a client or
   publish it without showing me first."
5. **`AI OS/connections.md`**: fill the 7-row table from Q4–Q7. Each row: `mechanism: not yet connected`,
   `auth: —`, `last checked: —`. Wiring happens Day 2.
6. **`AI OS/CLAUDE.md` and `AI OS/AGENTS.md`**: update only the "Context summary" section (name, top
   priority, one-line voice summary, connection summary) and the first line of "Voice", **identically in
   both files**. Preserve every other rule.
7. **`AI OS/hot.md`**: replace the priorities block; add "onboarded on <date>" under Recent.

Vault note rules (from the vault `CLAUDE.md`): front-matter with `title`, `created`, `tags`,
`source: aios-intake <date>`, `origin: human`, `author: yogesh`, `maturity: established`. **Never delete or
overwrite a user-authored note.** On re-runs, append a dated `## Update YYYY-MM-DD` section and bump
`updated:`. For files in this folder (`CLAUDE.md`, `connections.md`, `hot.md`, `aios-intake.md`), back up the
original to `archives/intake-{YYYY-MM-DD-HHMM}/` before changing it.

Then link the new notes from `01_Agency/_index.md` / `MOC.md` if they aren't already, add one line to the
vault `log.md`, and **commit and push the vault** (`git add` only the files you touched; message
`onboard: Day-1 context <date>`). The vault's private GitHub remote is pre-approved; nothing else is.
Add one dated line to `AI OS/decisions/log.md`.

### Step 4: The closing screen
Print one screen, three lines max:

```
✓ Day 1 done. Your AI OS knows who you are, what Sahas AI sells, what matters this quarter, and how you sound.

Today: ask me "what should I focus on this week?"
Tomorrow: pick one tool from connections.md and wire it (API + references/{tool}-api.md). Day 7: run /audit.
```

When he asks the closing prompt, answer using only the new context notes:
- 3 bullets, in his register from Q2
- each bullet tied to a stated Q3 priority
- final line: *"If I had to pick one thing for Monday, it'd be [X], because [reason]. Want me to draft the
  first step? And where could the Default Shift apply here: to what extent could AI take this on?"*

## Critical implementation rules

1. **7-question cap is non-negotiable.** No Q8 in conversation.
2. **Voice paste can't be skipped or typed mid-chat.**
3. **One-shot scaffold.** After Step 2, write Step 3 in one batch. He iterates by editing `aios-intake.md` and re-running.
4. **Idempotent.** Re-runs refresh only what changed; vault notes get dated update sections, operator files get archived first.
5. **No parallel context.** Business facts live in the vault only; `AI OS/` holds summaries and routes.
6. **Closing screen is three lines.** Not a menu.
7. **No extra skills generated.** He authors more through `/level-up`.
8. **No `.env` writes and no API keys on Day 1.** Connections come Day 2.
9. **Read-only on `references/3ms-framework.md`.**
10. **Local-only.** No cloud routines, connectors, uploads or messages. Only the vault `git push` above.

## Verification
- Cold test: fill 7 answers → scaffold → ask the wow prompt. The answer must cite Q1 + Q3 + Q7 specifics. Generic = fail.
- Idempotency: change one Q3 priority, re-run. Only `priorities.md` gets an update section and `CLAUDE.md`/`hot.md` change; backup appears in `archives/`.
- Voice rejection: type a sample mid-chat. The skill refuses and asks for a paste.
- Privacy: give a UPI ID in Q4. It's dropped and flagged.
