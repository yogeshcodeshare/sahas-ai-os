# Connections

Registry of every system the Sahas AI OS can reach. Filled by `/onboard` (Q4–Q7), expanded as tools are
wired. `/audit` checks it for domain coverage and freshness. Never put key values here; names go in
`.env.example`, values in `.env`.

| # | Domain | Tool | Account | Mechanism | Scope | Auth | Last checked |
|---|---|---|---|---|---|---|---|
| 1 | Revenue / financials | n/a yet: business current account to open when pitching starts; invoicing tool TBD | | not yet connected | read-only | — | — |
| 2 | Customer interactions / CRM | GoHighLevel: leads, pipeline, contacts, conversations, calendar, workflows. API guide: `references/ghl-api.md` | Sahas GHL sub-account | key+ref (Private Integration Token; ref ready, token not added) | read-only first | — | 2026-11-01: blocked, sub-account paused by BizAutomation (reseller); retry after restore |
| 3 | Calendar | Google Calendar | hello@sahasai.in | not yet connected | read | — | — |
| 4 | Communication | Zoho Mail; WhatsApp API (Veblika); social DMs once channels launch. No client comms live yet | hello@sahasai.in | not yet connected | read-only first | — | — |
| 5 | Project / task tracking | Night-before to-do list + 15-day reviews (vault); GHL tasks later | | not yet connected | read | — | — |
| 6 | Meeting intelligence | none yet (no client meetings); AI-chat exports as PDFs in workspace | | not yet connected | read | — | — |
| 7 | Knowledge / files | Obsidian vault (+ Google Drive) | local / hello@sahasai.in | local filesystem | read+write | n/a | 2026-11-01 |

**Mechanism options:** `script` (a script hitting an API, in `scripts/`), `key+ref` (`.env` key +
`references/{tool}-api.md`), `cli` (e.g. `gws` with its own OAuth project on hello@sahasai.in), `export`
(CSV/JSON dump), `n8n` (an n8n workflow does the fetching), `mcp` (only when no lean API route exists),
`not yet connected`.

Also available: the **n8n** instance (MCP connected) for deterministic automations that should run 24/7.

## Wiring recipe (one tool at a time)
1. Prefer API + a saved reference over an MCP server (fewer tokens, narrower scope).
2. Research the API docs once and save the endpoints, auth flow and common queries to `references/<tool>-api.md`.
3. Use a dedicated or least-privilege key (Intern Rule): read-only until a skill needs write.
4. Add the key **name** to `.env.example`; Yogesh pastes the value into `.env` himself. Never paste keys in chat.
5. Run one narrow read-only test, then fill in Mechanism / Auth / Last checked.
6. Log it in `decisions/log.md`.

**Never wire:** the personal Gmail, any employer (work) account, or the org connectors attached to this Claude
session (Google Docs/Drive connector, Atlassian, Pulse).
