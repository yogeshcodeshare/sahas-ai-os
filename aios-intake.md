# Sahas AI OS: Intake

Source of truth for `/onboard`. Fill it by typing, voice-dictating, or running `/onboard` for a guided
conversation. **Hard cap: 7 questions**, each answerable in about a minute. Edit and re-run any time.

Never put PAN, Aadhaar, bank/UPI details, API keys, or clients' personal contact details here.

> Pre-filled 2026-11-01 from existing vault notes (sources in brackets). Lines marked **CONFIRM** or **GAP**
> need Yogesh's answer.

---

## Q1: Who are you, what does Sahas AI sell, and who do you sell it to?

```
WHO: Yogesh Mohite (40), founder/operator of Sahas AI, built alongside a work-from-home job
(about 10:00 AM to 7–8 PM), plus a night n8n/AI-agent internship 3–4 nights a week.
Long-term goal: build a business to ₹100 Cr net worth by 55 (2041).
[source: 01_Agency/sahas-ai-founder-blueprint-2026-09-10, 01_Agency/short-term-goals-oct-2026-may-2027]

OFFER: Sahas AI Business Automation Agency. Business automation (take repetitive work off employees),
AI staffing (AI employees), custom agentic AI (grow into gradually), 1:1 AI coaching now and AI consulting
for businesses later. Delivery stack: WhatsApp (Veblika), GoHighLevel (bounded scope), self-hosted n8n.
Pricing anchors (emerging, validate on sales calls): retainers about ₹2,999–5,999/mo, custom workflows
₹8,000–15,000 one-time, ₹5,000 milestone-based "existing-system rescue" pilot.
[source: short-term-goals, service-offerings, pricing-ladder, decision-existing-system-rescue-sprint]

ICP: Pan-India Indian businesses in selected industries, not "local business" generally. Maharashtra is
the first research/relationship market; Marathi-first content. Research priority (hypotheses): modular
kitchen/interior studios, home-renovation contractors, wedding venues/banquets, solar EPC; then coaching
institutes, recruitment agencies, clinics, logistics, travel, home-service AMC, car dealerships (first
demo/pilot niche). Buyer = owner or commercial decision-maker.
[source: founder-blueprint, decision-car-dealership-first-pilot]

UPDATE 2026-11-01 (Yogesh): Built so far: WhatsApp agent team (4 WhatsApp agents); AI voice agent(s) to be
finished within ~1 week, then a demo video of the full WhatsApp + voice agent team. Selling starts from
this team. Nov–Dec: build Claude skills and automations side by side, each added to the portfolio.
Pricing NOT decided yet. Market reference he has seen: WhatsApp agent ~₹70,000, voice agent ₹70,000–1,00,000.
Published agency benchmarks (from sahas automation plan.pdf, 31 Oct 2026 research): chatbot ₹35k setup +
₹5k/mo; voice agent ₹50k + ₹10k/mo; WhatsApp API setup ₹30k + ₹8k/mo; standard AI agent ₹24,999 +
₹8,999/mo; premium ₹39,999 + ₹12,999/mo. Recommended model: setup + monthly management + usage charges
(LLM/voice/WhatsApp) + custom work; no unlimited-usage packages.
OPEN DECISION: pricing for the first 3 clients.
WHO-TO-SELL context (plan.pdf): Maharashtra-weighted (Pune/PCMC/Kolhapur/Sangli/Nashik) + pan-India.
Easiest first demos: real estate (lead-to-site-visit), clinics (receptionist/appointments), coaching
(admissions), auto dealerships, hotels. Higher-value later: manufacturers/distributors (RFQ→quotation,
PO/invoice extraction). Positioning advice: integrated systems (capture → CRM → booking → follow-up →
reports), not "a chatbot". Recommended next builds: CRM + Communication Hub first, then document AI.
NICHE RESEARCH REPORT (Google Doc, exported to Downloads as .docx, read 2026-11-01): 17 categories scored
on 5 criteria (customer value, recurring pain, decision-maker access, visible 30-day result, delivery
fit/risk; 25 points). Tiers: S (first research + pilot queue) = S1 modular kitchen & interior studios
(strongest subtype: independent full-home studio 23/25), S2 home-renovation contractors (turnkey 23/25),
S3 wedding venues & banquets, S4 solar EPC/rooftop. A (validation queue) = coaching, recruitment,
aesthetic clinics, dental/diagnostic/physio, B2B logistics, travel/boutique hotels, home-service AMC,
premium car dealerships. B (selective) = machinery distributors, real estate, CA firms, legal, insurance.
Rules: one category at a time; before any demo/outreach verify 3 local price signals, interview 2 owners,
map one workflow to human handoff, define one 30-day pilot metric, get founder approval. Automation never
quotes prices (e.g. interiors), never gives medical/legal/financial advice.
OPEN QUESTION: the report puts S1–S4 first, but the vault decision [[decision-car-dealership-first-pilot]]
and the Renault WhatsApp agent team point at car dealerships (A8) for the first demo. Which leads sales?
```

---

## Q2: Paste 1–2 things you've written recently. Don't edit them.

A client WhatsApp or email, a LinkedIn/Instagram post, a proposal. **Paste verbatim** and note where it
was used and its language. Don't type these mid-chat with Claude; chat-shaped samples are worse than none.

```
Sample 1 | channel: AI research prompt (voice-dictated) | language: English (Indian spoken style)
| date: 2026-10-31 | source: "sahas automation plan.pdf", opening message, verbatim
(full text stored in vault 01_Agency/voice-samples.md)
```

```
Sample 2 | GAP: add a real client-facing message (WhatsApp / email / post / proposal) when one exists.
```

---

## Q3: What are your 2–3 biggest priorities for the next 90 days?

Each with a number, a deadline or a deliverable.

```
Drafted from short-term-goals-oct-2026-may-2027 (Nov 2026 – Jan 2027):
1. Sales engine + Saturday Club: join and attend by 15 Nov; meet 10 owners, send 20 personalised
   outreach messages, have the pilot offer packaged. First paid pilot by 30 Nov.
2. First revenue: 2 paying clients and 1–2 AI coaching students by 31 Dec 2026.
3. AI Staffing: 1 working AI-employee prototype by 15 Jan; "AI Staffing" offer live with 3 demos by 31 Jan 2027.

CONFIRMED by Yogesh 2026-11-01, with focus: the next 90 days are mainly SALES AND MARKETING.
Goal: at least 1–2 paid clients. Supporting work:
- Finish the AI voice agent (~1 week) → demo video of the full WhatsApp agent team.
- Saturday Club networking.
- Create YouTube, Instagram and other social channels; post videos and carousels regularly.
- Build Claude skills + automations for content and for the portfolio (each one is a showcase for clients).
- GHL setup for lead management.
```

---

## Q4: Where does revenue actually land, and where is it tracked?

Tool names only (Razorpay, bank transfer, Zoho Invoice/Books, GHL, a sheet). No account numbers or UPI IDs.

```
Known: GST applies from the first rupee (registered GSTIN). Invoices/receipts stored locally in
"Sahas AI Agency Finance/". [source: pricing-ladder, gst-legal-structure, workspace folder]
ANSWER 2026-11-01: No business payment setup yet. Will open a business current account at a bank when
pitching starts. Invoicing/income tracking tool not chosen yet. (Domain 1 = not applicable yet.)
```

---

## Q5: Where do you talk to clients, collaborators and the outside world day-to-day?

Zoho Mail (hello@sahasai.in)? WhatsApp Business? GHL conversations? Instagram/Facebook DMs? Phone?

```
Known: Zoho Mail (hello@sahasai.in); WhatsApp API via Veblika; GoHighLevel for leads/pipeline;
Sahas AI Facebook Page, Instagram and YouTube; Saturday Club in person.
[source: founder-blueprint, sahas-ai-social-channel-status, this chat]
ANSWER 2026-11-01: "Not yet" — no daily client communication channel running yet (no clients).
Planned: Zoho Mail + WhatsApp (Veblika) + GHL conversations; social DMs once channels launch.
```

---

## Q6: Where do meeting recordings, notes and important docs live?

Google Meet / a transcript tool? Google Drive (hello@sahasai.in)? The vault? Local folders?

```
Known: the Obsidian vault (knowledge), local workspace folders (Clients/, finance, brand assets).
ANSWER (filled by Claude, Yogesh said "add the info"): no client meetings yet, so no recording tool.
Research and plans come from ChatGPT/Codex/Claude chats, exported as PDFs into the workspace
(e.g. "sahas automation plan.pdf") and ingested into the vault. Google Drive on hello@sahasai.in available
but not wired.
```

---

## Q7: What's the one task that eats your week, and where do you track work?

The biggest time-suck or recurring drudgery, plus where tasks and projects live.

```
Known: limited time (full-time job + internship nights); daily to-do written the night before;
15-day goal reviews. [source: short-term-goals "How to run it"]
ANSWER (filled by Claude from context, confirm later): top_pain = too little time to both BUILD
(agents, demos, skills) and SELL/MARKET (content, outreach), with a full-time job and night internship.
Content production (videos, carousels) is the next likely time-sink. Tasks: night-before to-do list +
15-day goal reviews in the vault; GHL tasks once GHL is set up.
```

---

When this is filled, run `/onboard`. It writes the Day-1 context into the vault (`01_Agency/`), fills
`connections.md`, and updates `CLAUDE.md`, `AGENTS.md` and `hot.md`.
