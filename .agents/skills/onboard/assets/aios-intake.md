# Sahas AI OS: Intake

Source of truth for `/onboard`. Fill it by typing, voice-dictating, or running `/onboard` for a guided
conversation. **Hard cap: 7 questions**, each answerable in about a minute. Edit and re-run any time.

Never put PAN, Aadhaar, bank/UPI details, API keys, or clients' personal contact details here.

---

## Q1: Who are you, what does Sahas AI sell, and who do you sell it to?

Identity, offer (services, packages, typical price range), ICP (industry, size, city/region, decision-maker).

```
[Your answer here]
```

---

## Q2: Paste 1–2 things you've written recently. Don't edit them.

A client WhatsApp or email, a LinkedIn/Instagram post, a proposal. **Paste verbatim** and note where it
was used and its language. Don't type these mid-chat with Claude; chat-shaped samples are worse than none.

```
[Sample 1, paste raw | channel: | language: | date: ]
```

```
[Sample 2, paste raw | channel: | language: | date: ]
```

---

## Q3: What are your 2–3 biggest priorities for the next 90 days?

Each with a number, a deadline or a deliverable.

```
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

---

## Q4: Where does revenue actually land, and where is it tracked?

Tool names only (Razorpay, bank transfer, Zoho Invoice/Books, GHL, a sheet). No account numbers or UPI IDs.

```
[Your answer here]
```

---

## Q5: Where do you talk to clients, collaborators and the outside world day-to-day?

Zoho Mail (hello@sahasai.in)? WhatsApp Business? GHL conversations? Instagram/Facebook DMs? Phone?

```
[Your answer here]
```

---

## Q6: Where do meeting recordings, notes and important docs live?

Google Meet / a transcript tool? Google Drive (hello@sahasai.in)? The vault? Local folders?

```
[Your answer here]
```

---

## Q7: What's the one task that eats your week, and where do you track work?

The biggest time-suck or recurring drudgery, plus where tasks and projects live.

```
[Your answer here]
```

---

When this is filled, run `/onboard`. It writes the Day-1 context into the vault (`01_Agency/`), fills
`connections.md`, and updates `CLAUDE.md` and `hot.md`.
