# GoHighLevel (GHL) API v2 reference

Researched once, saved here. **Read the Quick start and the recipe you need; search the catalog
(Ctrl+F the path or summary) for anything else.** Don't re-research the web unless a call fails.

- **Source:** official OpenAPI specs in [GoHighLevel/highlevel-api-docs](https://github.com/GoHighLevel/highlevel-api-docs)
  (the same content that powers https://marketplace.gohighlevel.com/docs/). Catalog generated 2026-11-01.
- **Used by Sahas AI for:** lead management, pipeline, contacts, conversations, calendar booking, workflows.
- **Account:** Sahas AI sub-account (location) in GHL via the BizAutomation package. Never a client's account
  without their written OK, never an employer account.

---

## 1. Quick start

### Auth: Private Integration Token (recommended for us)
Use a **sub-account Private Integration Token** (no OAuth app needed). In GHL: *Sub-account → Settings →
Private Integrations → Create new integration*. Give it a name like `sahas-ai-os` and tick **only the
scopes you need** (start read-only, see §3). Copy the token once. The specs confirm the bearer token can be
"the Access Token generated with user type Sub-Account (OR) Private Integration Token of Sub-Account".

Put it in `AI OS/.env` yourself (never paste it in chat):
```
GHL_PRIVATE_TOKEN=
GHL_LOCATION_ID=
```
`GHL_LOCATION_ID` = the sub-account ID (visible in the GHL URL: `/v2/location/<LOCATION_ID>/...`, or
Settings → Business Profile).

OAuth 2.0 (Marketplace app) is only needed if we later build an app installed into **client** sub-accounts.
Docs: `docs/oauth/Overview.md`, `Authorization.md`, `Scopes.md` in the docs repo.

### Base URL and headers
```
Base URL:       https://services.leadconnectorhq.com
Authorization:  Bearer $GHL_PRIVATE_TOKEN
Version:        2021-07-28        # most APIs
Version:        2021-04-15        # Conversations and Calendars (see the Version column in the catalog)
Accept:         application/json
Content-Type:   application/json  # for POST/PUT bodies
```
A wrong or missing `Version` header is a common cause of 4xx errors. Check the catalog column.

### Loading the token (Git Bash, from `AI OS/`)
```bash
set -a; . ./.env; set +a          # loads GHL_PRIVATE_TOKEN and GHL_LOCATION_ID; never echo them
GHL=https://services.leadconnectorhq.com
H=(-H "Authorization: Bearer $GHL_PRIVATE_TOKEN" -H "Accept: application/json")
```
All recipes below assume these three lines. Add `-H "Version: ..."` per call.

### Rate limits (from `docs/oauth/Faqs.md`)
- Burst: **100 requests per 10 seconds** per app per location.
- Daily: **200,000 requests per day** per app per location.
- Watch headers `X-RateLimit-Remaining` / `X-RateLimit-Max`; on **429** back off and retry.

### Common errors
| Code | Usually means | Fix |
|---|---|---|
| 401 | Token wrong/revoked, or missing scope | Re-check `.env`; add the scope to the Private Integration |
| 403 | Token's sub-account ≠ `locationId` you sent | Use the matching location ID |
| 404 | Wrong path, trailing slash, or ID | Compare with the catalog path exactly |
| 422 | Body validation failed | Check required (`*`) fields in the catalog |
| 429 | Rate limit | Wait and retry with backoff |

---

## 2. Safety rules (Sahas AI)
- **Read-only by default.** Writes (create/update/delete, tags, workflows) only when a skill or Yogesh needs it.
- **Never send a message to a lead or client** (`POST /conversations/messages`) without Yogesh approving the
  exact text in chat. Drafts first (Bike Method Phase 1).
- **No deletes** unless Yogesh asks for that specific record.
- Never print the token, and don't dump bulk contact data into chat or files; summarise.
- Phone numbers in E.164 (`+91XXXXXXXXXX`). Respect DND fields on contacts.
- WhatsApp sends must follow Meta's 24-hour window / approved-template rules.

---

## 3. Scopes to tick (least privilege)
| Need | Scopes |
|---|---|
| Read leads & pipeline (start here) | `contacts.readonly`, `opportunities.readonly`, `locations.readonly`, `locations/customFields.readonly`, `locations/tags.readonly`, `users.readonly` |
| Read conversations | `conversations.readonly`, `conversations/message.readonly` |
| Read calendar | `calendars.readonly`, `calendars/events.readonly` |
| Read workflows & forms | `workflows.readonly`, `forms.readonly` |
| Write leads (later) | `contacts.write`, `opportunities.write` |
| Book appointments (later) | `calendars/events.write` |
| Send messages (later, with approval) | `conversations/message.write` |

---

## 4. Recipes (curl)

### Location (sub-account) details
```bash
curl -s "$GHL/locations/$GHL_LOCATION_ID" "${H[@]}" -H "Version: 2021-07-28"
```

### Users in the sub-account
```bash
curl -s "$GHL/users/?locationId=$GHL_LOCATION_ID" "${H[@]}" -H "Version: 2021-07-28"
```

### Pipelines and stage IDs (save IDs into skills once known)
```bash
curl -s "$GHL/opportunities/pipelines?locationId=$GHL_LOCATION_ID" "${H[@]}" -H "Version: 2021-07-28"
```

### Contacts
```bash
# List (simple)
curl -s "$GHL/contacts/?locationId=$GHL_LOCATION_ID&limit=20" "${H[@]}" -H "Version: 2021-07-28"

# Search (advanced filters). The spec leaves the body schema open; this shape is the documented pattern —
# verify on first use and fix here if it differs.
curl -s -X POST "$GHL/contacts/search" "${H[@]}" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"locationId":"'"$GHL_LOCATION_ID"'","page":1,"pageLimit":20,"query":"renault"}'

# Get one
curl -s "$GHL/contacts/CONTACT_ID" "${H[@]}" -H "Version: 2021-07-28"

# Upsert (create or update by phone/email; respects the location's duplicate setting)
curl -s -X POST "$GHL/contacts/upsert" "${H[@]}" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"locationId":"'"$GHL_LOCATION_ID"'","firstName":"Test","phone":"+919999999999","source":"sahas-ai-os","tags":["test-lead"]}'

# Add tags
curl -s -X POST "$GHL/contacts/CONTACT_ID/tags" "${H[@]}" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"tags":["hot-lead"]}'

# Add a note (body* required)
curl -s -X POST "$GHL/contacts/CONTACT_ID/notes" "${H[@]}" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"body":"Asked for test-drive slot on Saturday."}'

# Create a follow-up task (title*, dueDate*, completed* required)
curl -s -X POST "$GHL/contacts/CONTACT_ID/tasks" "${H[@]}" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"title":"Call back lead","dueDate":"2026-11-05T05:30:00Z","completed":false}'
```
Create without upsert: `POST /contacts/` (only `locationId*` required). Custom fields go in
`customFields: [{"id":"FIELD_ID","field_value":"..."}]`; get IDs from `GET /locations/{locationId}/customFields`.

### Opportunities (pipeline deals)
```bash
# Search (query params; location_id* required)
curl -s "$GHL/opportunities/search?location_id=$GHL_LOCATION_ID&pipeline_id=PIPELINE_ID&status=open&limit=20" \
  "${H[@]}" -H "Version: 2021-07-28"

# Create (pipelineId*, locationId*, name*, status*, contactId* required)
curl -s -X POST "$GHL/opportunities/" "${H[@]}" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"pipelineId":"PIPELINE_ID","locationId":"'"$GHL_LOCATION_ID"'","name":"Test lead - Renault","status":"open","contactId":"CONTACT_ID","pipelineStageId":"STAGE_ID","monetaryValue":0}'

# Move stage
curl -s -X PUT "$GHL/opportunities/OPP_ID" "${H[@]}" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"pipelineStageId":"NEW_STAGE_ID"}'

# Won / lost (status: open | won | lost | abandoned)
curl -s -X PUT "$GHL/opportunities/OPP_ID/status" "${H[@]}" -H "Version: 2021-07-28" -H "Content-Type: application/json" \
  -d '{"status":"won"}'
```
Also: `POST /opportunities/upsert`, `GET /opportunities/lost-reason`.

### Conversations (Version 2021-04-15)
```bash
# Recent conversations (optionally &contactId=...)
curl -s "$GHL/conversations/search?locationId=$GHL_LOCATION_ID&limit=20&sortBy=last_message_date&sort=desc" \
  "${H[@]}" -H "Version: 2021-04-15"

# Messages in one conversation
curl -s "$GHL/conversations/CONVERSATION_ID/messages" "${H[@]}" -H "Version: 2021-04-15"

# SEND a message — ONLY after Yogesh approves the exact text.
# type*: SMS | RCS | Email | WhatsApp | IG | FB | Custom | Live_Chat | TIKTOK  (spec also lists subType*, status*)
curl -s -X POST "$GHL/conversations/messages" "${H[@]}" -H "Version: 2021-04-15" -H "Content-Type: application/json" \
  -d '{"type":"WhatsApp","contactId":"CONTACT_ID","message":"APPROVED TEXT"}'
```
Logging an inbound message from another channel: `POST /conversations/messages/inbound`.

### Calendars (Version 2021-04-15)
```bash
# List calendars
curl -s "$GHL/calendars/?locationId=$GHL_LOCATION_ID" "${H[@]}" -H "Version: 2021-04-15"

# Free slots (startDate*, endDate* — epoch milliseconds; timezone optional)
curl -s "$GHL/calendars/CALENDAR_ID/free-slots?startDate=1762300800000&endDate=1762905600000&timezone=Asia/Kolkata" \
  "${H[@]}" -H "Version: 2021-04-15"

# Events in a range (locationId*, startTime*, endTime* — epoch ms; plus calendarId or userId or groupId)
curl -s "$GHL/calendars/events?locationId=$GHL_LOCATION_ID&calendarId=CALENDAR_ID&startTime=1762300800000&endTime=1762905600000" \
  "${H[@]}" -H "Version: 2021-04-15"

# Book an appointment (calendarId*, locationId*, contactId*, startTime* required)
curl -s -X POST "$GHL/calendars/events/appointments" "${H[@]}" -H "Version: 2021-04-15" -H "Content-Type: application/json" \
  -d '{"calendarId":"CALENDAR_ID","locationId":"'"$GHL_LOCATION_ID"'","contactId":"CONTACT_ID","startTime":"2026-11-08T11:00:00+05:30","endTime":"2026-11-08T11:30:00+05:30","title":"Test drive","appointmentStatus":"confirmed","toNotify":false}'
```

### Workflows
```bash
# List workflows (read-only API: you cannot build workflows via API)
curl -s "$GHL/workflows/?locationId=$GHL_LOCATION_ID" "${H[@]}" -H "Version: 2021-07-28"

# Enrol a contact into a workflow
curl -s -X POST "$GHL/contacts/CONTACT_ID/workflow/WORKFLOW_ID" "${H[@]}" -H "Version: 2021-07-28" \
  -H "Content-Type: application/json" -d '{}'
```

### Forms, tags, custom fields
```bash
curl -s "$GHL/forms/?locationId=$GHL_LOCATION_ID" "${H[@]}" -H "Version: 2021-07-28"
curl -s "$GHL/forms/submissions?locationId=$GHL_LOCATION_ID&limit=20" "${H[@]}" -H "Version: 2021-07-28"
curl -s "$GHL/locations/$GHL_LOCATION_ID/tags" "${H[@]}" -H "Version: 2021-07-28"
curl -s "$GHL/locations/$GHL_LOCATION_ID/customFields" "${H[@]}" -H "Version: 2021-07-28"
```

### Pagination
List endpoints use `limit` with `page`, `startAfter`/`startAfterId`, or a `meta.nextPageUrl` in the response,
depending on the API. Check the response `meta` and the catalog params; never loop without a cap.

### n8n
n8n has a native HighLevel node, or use the **HTTP Request** node with the same base URL and headers
(store the token as an n8n credential, not in the workflow JSON).

---

## 5. Known IDs (fill in as discovered; IDs are not secrets)
| Thing | ID | Notes |
|---|---|---|
| Location (sub-account) | in `.env` as `GHL_LOCATION_ID` | |
| Main lead pipeline | | from `GET /opportunities/pipelines` |
| Stages | | |
| Booking calendar | | |
| Key workflows | | |

When a skill uses specific endpoints and IDs, copy them into that skill so it doesn't read this whole file.

---

## 6. Full endpoint catalog
Search this section for any path or action. `*` = required. Bodies list top-level fields only; see the
spec file in the docs repo for nested objects.

<!-- CATALOG:START -->
Generated from GoHighLevel/highlevel-api-docs @ 0af86a4 2026-06-19: 576 endpoints in 41 APIs. Regenerate with `scripts/build-ghl-api-catalog.py`.

**Index:** Ad Manager API · Affiliate Manager API · Agent Studio APIs · Associations API · Blogs API · Brand Boards API · Business API · Calendars API · Campaigns API · Companies API · Contacts API · Conversation AI API · Conversations API · MEMBERSHIPS API · Custom Fields V2 · Custom menus API · Email ISV API · Email API · Forms API · Funnels API · Invoice API · Knowledge Base API · Trigger Links API · Sub-Account · Developer marketplace API · Media Storage API · OAuth 2.0 · CUSTOM_OBJECTS API · Opportunities API · Payments API · Phone System API · Products API · Documents and Contracts API · SaaS API · Snapshots API · Social Media Posting API · Store API · Surveys API · Users API · Voice AI API · workflows API

### Ad Manager API (`apps/ad-manager.json`, 94 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/ad-publishing/facebook/reporting` | Get reporting data | adPublishing.readonly | 2021-07-28 | locationId*, groupBy*, startDate*, endDate*, type*, fields* |  |
| GET | `/ad-publishing/facebook/reporting/campaign/{campaignId}` | Get campaign reporting | adPublishing.readonly | 2021-07-28 | campaignId*, locationId*, startDate*, endDate* |  |
| GET | `/ad-publishing/facebook/reporting/list` | Get reporting list | adPublishing.readonly | 2021-07-28 | locationId*, listType*, startDate*, endDate*, campaignId*, type* |  |
| GET | `/ad-publishing/facebook/me` | Get current Facebook user | adPublishing.readonly | 2021-07-28 | locationId* |  |
| GET | `/ad-publishing/facebook/pages` | Get Facebook pages | adPublishing.readonly | 2021-07-28 | locationId*, fetchExisting |  |
| GET | `/ad-publishing/facebook/page/{pageId}/instagram` | Get Instagram accounts for page | adPublishing.readonly | 2021-07-28 | pageId*, locationId*, type |  |
| GET | `/ad-publishing/facebook/page/{pageId}/forms` | Get page lead forms | adPublishing.readonly | 2021-07-28 | pageId*, locationId* |  |
| POST | `/ad-publishing/facebook/page/{pageId}/forms` | Create page lead form | adPublishing.write | 2021-07-28 | pageId* | type*, name*, locationId*, greetingCard, questions*, questionPageHeadline, privacyPolicyLink*, privacyPolicyText, customDisclaimer, thankYouPage* |
| GET | `/ad-publishing/facebook/ad-accounts` | Get ad accounts | adPublishing.readonly | 2021-07-28 | locationId*, type, next, fetchAll, limit |  |
| GET | `/ad-publishing/facebook/ad-accounts/{adAccountId}` | Get ad account details | adPublishing.readonly | 2021-07-28 | adAccountId*, locationId* |  |
| DELETE | `/ad-publishing/facebook/ad-accounts/{adAccountId}` | Delete ad account | adPublishing.write | 2021-07-28 | adAccountId* | locationId* |
| GET | `/ad-publishing/facebook/conversation-forms` | Get conversation forms | adPublishing.readonly | 2021-07-28 | locationId* |  |
| POST | `/ad-publishing/facebook/conversation-forms` | Create conversation form | adPublishing.write | 2021-07-28 |  | locationId*, name*, text*, questions* |
| POST | `/ad-publishing/facebook/integration` | Create Facebook integration | adPublishing.write | 2021-07-28 |  | locationId*, pageId*, adAccountId |
| GET | `/ad-publishing/facebook/integration` | Get Facebook integration | adPublishing.readonly | 2021-07-28 | locationId* |  |
| DELETE | `/ad-publishing/facebook/integration` | Delete Facebook integration | adPublishing.write | 2021-07-28 |  | locationId* |
| GET | `/ad-publishing/facebook/targeting/search` | Search targeting options | — | 2021-07-28 | type*, query*, searchType |  |
| POST | `/ad-publishing/facebook/campaigns/{campaignId}/publish` | Publish campaign | adPublishing.write | 2021-07-28 | campaignId* | locationId* |
| DELETE | `/ad-publishing/facebook/page` | Delete page connection | adPublishing.write | 2021-07-28 | locationId*, pageId* |  |
| GET | `/ad-publishing/facebook/pixels` | Get conversion pixels | adPublishing.readonly | 2021-07-28 | locationId*, channel, pageId, igUserId |  |
| PUT | `/ad-publishing/facebook/pixels` | Upsert conversion pixel | adPublishing.write | 2021-07-28 |  | locationId*, conversionPixelId, name, igUserId, type* |
| GET | `/ad-publishing/facebook/custom-audience` | Get custom audiences | adPublishing.readonly | 2021-07-28 | locationId*, type*, source, adAccountId* |  |
| DELETE | `/ad-publishing/facebook/custom-audience/{audienceId}` | Delete custom audience | adPublishing.write | 2021-07-28 | audienceId*, locationId* |  |
| PUT | `/ad-publishing/facebook/custom-audience/{audienceId}` | Update custom audience | adPublishing.write | 2021-07-28 | audienceId* | locationId*, name*, description* |
| GET | `/ad-publishing/facebook/custom-audience/{audienceId}` | Get custom audience by ID | adPublishing.readonly | 2021-07-28 | audienceId*, locationId* |  |
| PUT | `/ad-publishing/facebook/custom-audience/{audienceId}/member` | Add custom audience member | adPublishing.write | 2021-07-28 | audienceId* | locationId*, contactId*, fbAdAccountId |
| DELETE | `/ad-publishing/facebook/custom-audience/{audienceId}/member` | Remove custom audience member | adPublishing.write | 2021-07-28 | audienceId* | locationId*, contactId*, fbAdAccountId |
| PUT | `/ad-publishing/facebook/custom-audience/{audienceId}/member/batch` | Batch update audience members | adPublishing.write | 2021-07-28 | audienceId* | locationId*, csvPath, operationType*, smartlistIds, dynamicAudience |
| PUT | `/ad-publishing/facebook/page/default` | Set default page | adPublishing.write | 2021-07-28 | locationId* | pageId* |
| GET | `/ad-publishing/facebook/lead-form/{leadFormId}` | Get lead form by ID | adPublishing.readonly | 2021-07-28 | leadFormId*, locationId* |  |
| GET | `/ad-publishing/facebook/campaign/{campaignId}` | Get campaign with linked entities | adPublishing.readonly | 2021-07-28 | campaignId*, locationId*, fields, source |  |
| GET | `/ad-publishing/facebook/entity` | Get entities | adPublishing.readonly | 2021-07-28 | locationId*, type*, next, fetchAll, campaignId, adSetId, entityType*, searchId, selectedAdAccountId |  |
| PUT | `/ad-publishing/facebook/campaigns` | Upsert campaign | adPublishing.write | 2021-07-28 |  | id, locationId*, name, objective, specialAdCategories, source |
| PUT | `/ad-publishing/facebook/adsets` | Upsert adset | adPublishing.write | 2021-07-28 |  | id, locationId*, name, pageId, instagramActorId, messagingPlatforms, whatsappNumber, audience, budget, conversionLocation, customEventType, pixelId, campaignId* |
| PUT | `/ad-publishing/facebook/ads-v2` | Upsert ad | adPublishing.write | 2021-07-28 |  | id, locationId*, name, primaryText, headline, description, imageUrl, mediaType, media, multiAdvertiserAds, campaignId*, adsetId*, cta, conversationFormId … |
| POST | `/ad-publishing/facebook/campaigns/{campaignId}/pause` | Pause campaign | adPublishing.write | 2021-07-28 | campaignId* | locationId* |
| POST | `/ad-publishing/facebook/campaigns/{campaignId}/resume` | Resume campaign | adPublishing.write | 2021-07-28 | campaignId* | locationId* |
| POST | `/ad-publishing/facebook/campaigns/{campaignId}/duplicate` | Duplicate campaign | adPublishing.write | 2021-07-28 | campaignId* | locationId* |
| DELETE | `/ad-publishing/facebook/campaigns/{campaignId}` | Delete campaign | adPublishing.write | 2021-07-28 | campaignId* | locationId* |
| POST | `/ad-publishing/facebook/adsets/{adsetId}/pause` | Pause ad set | adPublishing.write | 2021-07-28 | adsetId* | locationId* |
| POST | `/ad-publishing/facebook/adsets/{adsetId}/resume` | Resume ad set | adPublishing.write | 2021-07-28 | adsetId* | locationId* |
| POST | `/ad-publishing/facebook/adsets/{adsetId}/duplicate` | Duplicate ad set | adPublishing.write | 2021-07-28 | adsetId* |  |
| DELETE | `/ad-publishing/facebook/adsets/{adsetId}` | Delete ad set | adPublishing.write | 2021-07-28 | adsetId* | locationId* |
| POST | `/ad-publishing/facebook/ads/{adId}/pause` | Pause ad | adPublishing.write | 2021-07-28 | adId* | locationId* |
| POST | `/ad-publishing/facebook/ads/{adId}/resume` | Resume ad | adPublishing.write | 2021-07-28 | adId* | locationId* |
| POST | `/ad-publishing/facebook/ads/{adId}/duplicate` | Duplicate ad | adPublishing.write | 2021-07-28 | adId* |  |
| DELETE | `/ad-publishing/facebook/ads/{adId}` | Delete ad | adPublishing.write | 2021-07-28 | adId* | locationId* |
| GET | `/ad-publishing/google/reporting` | Get reporting data | adPublishing.readonly | 2021-07-28 | locationId*, groupBy, startDate*, endDate*, type*, fields* |  |
| GET | `/ad-publishing/google/reporting/list` | Get reporting list | adPublishing.readonly | 2021-07-28 | locationId*, listType*, startDate*, endDate*, campaignId, type* |  |
| GET | `/ad-publishing/google/reporting/campaign/{campaignId}` | Get campaign reporting | adPublishing.readonly | 2021-07-28 | campaignId*, locationId*, startDate*, endDate* |  |
| GET | `/ad-publishing/google/conversions` | Get conversions | adPublishing.readonly | 2021-07-28 | locationId*, type, conversionType, category, startDate, endDate |  |
| PUT | `/ad-publishing/google/conversions` | Upsert conversion | adPublishing.write | 2021-07-28 |  | locationId*, conversionId, name*, type*, category*, valueSettings*, countingType*, attributionModel*, clickThroughWindow* |
| GET | `/ad-publishing/google/conversions/{conversionId}` | Get conversion by ID | adPublishing.readonly | 2021-07-28 | conversionId*, locationId* |  |
| DELETE | `/ad-publishing/google/conversions/{conversionId}` | Delete conversion | adPublishing.write | 2021-07-28 | conversionId*, locationId* |  |
| GET | `/ad-publishing/google/integration` | Get Google integration | adPublishing.readonly | 2021-07-28 | locationId* |  |
| POST | `/ad-publishing/google/integration` | Create Google integration | adPublishing.write | 2021-07-28 |  | locationId*, adAccountId*, mccId* |
| GET | `/ad-publishing/google/me` | Get current Google user | adPublishing.readonly | 2021-07-28 | locationId* |  |
| GET | `/ad-publishing/google/ad-accounts` | Get Google ad accounts | adPublishing.readonly | 2021-07-28 | locationId*, type |  |
| GET | `/ad-publishing/google/ad-accounts/{adAccountId}` | Get ad account details | adPublishing.readonly | 2021-07-28 | locationId*, adAccountId* |  |
| DELETE | `/ad-publishing/google/ad-accounts/{adAccountId}` | Delete ad account | adPublishing.write | 2021-07-28 | adAccountId* | locationId* |
| POST | `/ad-publishing/google/ads/{adId}/publish` | Publish ad | adPublishing.write | 2021-07-28 | adId* |  |
| GET | `/ad-publishing/google/targeting/search` | Search targeting options | adPublishing.readonly | 2021-07-28 | type*, query, locationId* |  |
| POST | `/ad-publishing/google/keyword-ideas` | Get keyword ideas | adPublishing.readonly | 2021-07-28 | locationId* | url*, languageCode, locations, keywords |
| GET | `/ad-publishing/google/assets` | Get assets | adPublishing.readonly | 2021-07-28 | locationId*, type*, id, advertiserOnly |  |
| POST | `/ad-publishing/google/assets` | Upsert assets | adPublishing.write | 2021-07-28 |  | locationId*, type*, payload* |
| GET | `/ad-publishing/google/entity` | Get entities | adPublishing.readonly | 2021-07-28 | locationId*, type*, campaignId, adGroupId, entityType*, searchId, startDate, endDate, selectedAdAccountId |  |
| GET | `/ad-publishing/google/target-interests` | Get target interests | adPublishing.readonly | 2021-07-28 | locationId*, type*, advertisingChannelType* |  |
| GET | `/ad-publishing/google/segments` | Get segments | adPublishing.readonly | 2021-07-28 | locationId*, type |  |
| PUT | `/ad-publishing/google/segments` | Upsert segment | adPublishing.write | 2021-07-28 | locationId*, type* | name*, description, members, status, type, id, membershipStatus, ruleBasedUserList, membershipLifeSpan, seedUserListIds, countryCodes, expansionLevel |
| DELETE | `/ad-publishing/google/segments/{segmentId}` | Delete segment | adPublishing.write | 2021-07-28 | segmentId*, locationId*, type* |  |
| GET | `/ad-publishing/google/segments/{segmentId}` | Get segment by ID | adPublishing.readonly | 2021-07-28 | segmentId*, locationId*, type* |  |
| POST | `/ad-publishing/google/segments/offline-user-list-job` | Create offline user list job | adPublishing.write | 2021-07-28 |  | locationId*, smartListIds, csvPath, userListId, isDynamic |
| PUT | `/ad-publishing/google/audiences` | Upsert audience | adPublishing.write | 2021-07-28 |  | locationId*, resourceName, name*, dimensions, exclusionDimension |
| GET | `/ad-publishing/google/audiences` | Get audiences | adPublishing.readonly | 2021-07-28 | locationId* |  |
| GET | `/ad-publishing/google/audiences/{audienceId}` | Get audience by ID | adPublishing.readonly | 2021-07-28 | audienceId*, locationId* |  |
| PUT | `/ad-publishing/google/ads` | Upsert Google campaign | adPublishing.write | 2021-07-28 |  | id, name*, locationId*, advertisingChannelType*, advertisingChannelSubType, goalType, budget, audience, networkSettings, biddingStrategy, assets, isEuPoliticalAds, adGroups, campaignGoal … |
| GET | `/ad-publishing/google/ads/{adId}` | Get Google campaign by ID | adPublishing.readonly | 2021-07-28 | adId*, locationId* |  |
| GET | `/ad-publishing/google/conversion-goals` | Get conversion goals | adPublishing.readonly | 2021-07-28 | locationId* |  |
| GET | `/ad-publishing/linkedin/integration` | Get LinkedIn integration | adPublishing.readonly | 2021-07-28 | locationId* |  |
| POST | `/ad-publishing/linkedin/integration` | Create LinkedIn integration | adPublishing.write | 2021-07-28 |  | locationId*, adAccountId*, adAccountName*, currencyCode*, organizationId* |
| GET | `/ad-publishing/linkedin/ad-accounts` | Get LinkedIn ad accounts | adPublishing.readonly | 2021-07-28 | locationId* |  |
| GET | `/ad-publishing/linkedin/ad-account` | Get ad account details | adPublishing.readonly | 2021-07-28 | locationId*, adAccountId* |  |
| DELETE | `/ad-publishing/linkedin/ad-account` | Delete ad account | adPublishing.write | 2021-07-28 | locationId*, adAccountId* |  |
| GET | `/ad-publishing/linkedin/me` | Get current LinkedIn user | adPublishing.readonly | 2021-07-28 | locationId* |  |
| GET | `/ad-publishing/linkedin/ads/{adId}` | Get ad campaign group | adPublishing.readonly | 2021-07-28 | adId*, locationId* |  |
| POST | `/ad-publishing/linkedin/ads/{adId}/publish` | Publish ad campaign group | adPublishing.write | 2021-07-28 | adId* | locationId* |
| PUT | `/ad-publishing/linkedin/ads` | Upsert ad campaign group | adPublishing.write | 2021-07-28 |  | id, locationId*, budget, adCampaigns, adBudgetOptimization, objectiveType, name, adCampaignGroupId, publishingStatus, linkedInAdAccountId, unpublishedChanges, meta, linkedInError |
| GET | `/ad-publishing/linkedin/targeting/search` | Search targeting options | adPublishing.readonly | 2021-07-28 | locationId*, facet*, query, q |  |
| GET | `/ad-publishing/linkedin/{accountId}/forms` | Get lead forms | adPublishing.readonly | 2021-07-28 | accountId*, locationId* |  |
| POST | `/ad-publishing/linkedin/{accountId}/form` | Create lead form | adPublishing.write | 2021-07-28 | locationId* | owner*, creationLocale*, name*, state*, content*, hiddenFields |
| PATCH | `/ad-publishing/linkedin/{adId}/status` | Update ad status | adPublishing.write | 2021-07-28 | adId*, locationId* | operationType*, type* |
| GET | `/ad-publishing/linkedin/reporting` | Get ad analytics | adPublishing.readonly | 2021-07-28 | locationId*, pivot, groupBy, startDate*, endDate*, entityUrns, fields |  |
| GET | `/ad-publishing/linkedin/reporting/list` | Get reporting list | adPublishing.readonly | 2021-07-28 | locationId*, listType*, campaignId*, campaignGroupId*, startDate*, endDate*, fields |  |
| GET | `/ad-publishing/linkedin/reporting/campaign-group/{campaignGroupId}` | Get campaign group reporting | adPublishing.readonly | 2021-07-28 | campaignGroupId*, locationId*, startDate*, endDate*, fields, campaignGroupId |  |

### Affiliate Manager API (`apps/affiliate-manager.json`, 4 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/affiliate-manager/{locationId}/affiliates` | List Affiliates | affiliate-manager.readonly | 2021-07-28 | locationId*, query, active, campaignId, skip, limit, fromDate, toDate |  |
| GET | `/affiliate-manager/{locationId}/affiliates/{affiliateId}` | Get Affiliate | affiliate-manager.readonly | 2021-07-28 | locationId*, affiliateId* |  |
| GET | `/affiliate-manager/{locationId}/payouts` | List Payouts | affiliate-manager.readonly | 2021-07-28 | locationId*, status, query, affiliateId, campaignId, skip, limit, start, end |  |
| GET | `/affiliate-manager/{locationId}/commissions` | List Commissions | affiliate-manager.readonly | 2021-07-28 | locationId*, campaignId, affiliateId, status, query, skip, limit, fromDate, toDate |  |

### Agent Studio APIs (`apps/agent-studio.json`, 11 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/agent-studio/agent` | Create Agent | agent-studio.write | 2021-04-15 | source | locationId*, name, description, agencyId, authorId, authorName, authorEmail, status*, version*, nodes, edges |
| GET | `/agent-studio/agent` | List Agents | agent-studio.readonly | 2021-04-15 | locationId*, isPublished, limit*, offset*, source |  |
| PATCH | `/agent-studio/agent/versions/{versionId}` | Update Agent | agent-studio.write | 2021-04-15 | versionId*, source | locationId*, versionName, description, nodes, edges, globalVariables, inputVariables, runtimeVariables, globalConfig, userId, userName |
| PATCH | `/agent-studio/agent/{agentId}` | Update Agent Metadata | agent-studio.write | 2021-04-15 | agentId*, source | locationId*, name, description, status |
| DELETE | `/agent-studio/agent/{agentId}` | Delete Agent | agent-studio.write | 2021-04-15 | agentId*, locationId*, source |  |
| GET | `/agent-studio/agent/{agentId}` | Get Agent | agent-studio.readonly | 2021-04-15 | agentId*, locationId*, source |  |
| POST | `/agent-studio/agent/versions/{versionId}/publish` | Promote to Production | agent-studio.write | 2021-04-15 | versionId*, source | locationId*, userId, userName, userEmail |
| POST | `/agent-studio/agent/{agentId}/execute` | Execute Agent | agent-studio.write | 2021-04-15 | agentId*, source | message*, executionId, inputVariables, versionId, attachments, locationId*, contactId |
| GET | `/agent-studio/public-api/agents` | List Agents (Deprecated) | agent-studio.readonly | 2021-04-15 | locationId*, limit*, offset*, source |  |
| GET | `/agent-studio/public-api/agents/{agentId}` | Get Agent (Deprecated) | agent-studio.readonly | 2021-04-15 | agentId*, locationId*, source |  |
| POST | `/agent-studio/public-api/agents/{agentId}/execute` | Execute Agent (Deprecated) | agent-studio.write | 2021-04-15 | agentId*, source | message*, executionId, inputVariables, versionId, attachments, locationId*, contactId |

### Associations API (`apps/associations.json`, 10 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/associations/relations` | Create Relation for you associated entities. | associations/relation.write | 2021-07-28 |  | locationId*, associationId*, firstRecordId*, secondRecordId* |
| GET | `/associations/relations/{recordId}` | Get all relations By record Id | associations/relation.readonly | 2021-07-28 | recordId*, locationId*, skip*, limit*, associationIds |  |
| DELETE | `/associations/relations/{relationId}` | Delete Relation | associations/relation.write | 2021-07-28 | relationId*, locationId* |  |
| GET | `/associations/key/{key_name}` | Get association key by key name | associations.readonly | 2021-07-28 | key_name*, locationId* |  |
| GET | `/associations/objectKey/{objectKey}` | Get association by object keys | associations.readonly | 2021-07-28 | objectKey, locationId |  |
| PUT | `/associations/{associationId}` | Update Association By Id | associations.write | 2021-07-28 | associationId* | firstObjectLabel*, secondObjectLabel* |
| DELETE | `/associations/{associationId}` | Delete Association | associations.write | 2021-07-28 | associationId* |  |
| GET | `/associations/{associationId}` | Get association by ID | associations.readonly | 2021-07-28 | associationId* |  |
| POST | `/associations/` | Create Association | associations.write | 2021-07-28 |  | locationId*, key*, firstObjectLabel*, firstObjectKey*, secondObjectLabel*, secondObjectKey* |
| GET | `/associations/` | Get all associations for a sub-account / location | associations.readonly | 2021-07-28 | locationId*, skip*, limit* |  |

### Blogs API (`apps/blogs.json`, 7 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/blogs/posts/url-slug-exists` | Check url slug | blogs/check-slug.readonly | 2021-07-28 | urlSlug*, locationId*, postId |  |
| PUT | `/blogs/posts/{postId}` | Update Blog Post | blogs/post-update.write | 2021-07-28 |  | title*, locationId*, blogId*, imageUrl*, description*, rawHTML*, status*, imageAltText*, categories*, tags, author*, urlSlug*, canonicalLink, publishedAt* |
| POST | `/blogs/posts` | Create Blog Post | blogs/post.write | 2021-07-28 |  | title*, locationId*, blogId*, imageUrl*, description*, rawHTML*, status*, imageAltText*, categories*, tags, author*, urlSlug*, canonicalLink, publishedAt* |
| GET | `/blogs/authors` | Get all authors | blogs/author.readonly | 2021-07-28 | locationId*, limit*, offset* |  |
| GET | `/blogs/categories` | Get all categories | blogs/category.readonly | 2021-07-28 | locationId*, limit*, offset* |  |
| GET | `/blogs/posts/all` | Get Blog posts by Blog ID | blogs/posts.readonly | 2021-07-28 | locationId*, blogId*, limit*, offset*, searchTerm, status |  |
| GET | `/blogs/site/all` | Get Blogs by Location ID | blogs/list.readonly | 2021-07-28 | locationId*, skip*, limit*, searchTerm |  |

### Brand Boards API (`apps/brand-boards.json`, 5 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/brand-boards/{locationId}` | Get Brand Boards | brand-boards/design-kit.readonly | 2021-07-28 | locationId*, limit, offset, search, deleted |  |
| GET | `/brand-boards/{locationId}/{id}` | Get Brand Board | brand-boards/design-kit.readonly | 2021-07-28 | locationId*, id* |  |
| PATCH | `/brand-boards/{locationId}/{id}` | Update a Brand Board | brand-boards/design-kit.write | 2021-07-28 | locationId*, id* | name, logos, colors, fonts, default, parentId |
| DELETE | `/brand-boards/{locationId}/{id}` | Delete a Brand Board | brand-boards/design-kit.write | 2021-07-28 | locationId*, id* |  |
| POST | `/brand-boards/` | Create a new brand board | brand-boards/design-kit.write | 2021-07-28 |  | locationId*, name*, logos, colors, fonts, default, brandBoardId, parentId, type |

### Business API (`apps/businesses.json`, 5 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| PUT | `/businesses/{businessId}` | Update Business | businesses.write | 2021-07-28 | businessId* | name, phone, email, postalCode, website, address, state, city, country, description |
| DELETE | `/businesses/{businessId}` | Delete Business | businesses.write | 2021-07-28 | businessId* |  |
| GET | `/businesses/{businessId}` | Get Business | businesses.readonly | 2021-07-28 | businessId* |  |
| GET | `/businesses/` | Get Businesses by Location | businesses.readonly | 2021-07-28 | locationId*, limit, skip |  |
| POST | `/businesses/` | Create Business | businesses.write | 2021-07-28 |  | name*, locationId*, phone, email, website, address, city, postalCode, state, country, description |

### Calendars API (`apps/calendars.json`, 41 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/calendars/groups` | Get Groups | calendars/groups.readonly | 2021-04-15 | locationId* |  |
| POST | `/calendars/groups` | Create Calendar Group | calendars/groups.write | 2021-04-15 |  | locationId*, name*, description*, slug*, isActive |
| POST | `/calendars/groups/validate-slug` | Validate group slug | calendars/groups.write | 2021-04-15 |  | locationId*, slug* |
| DELETE | `/calendars/groups/{groupId}` | Delete Group | calendars/groups.write | 2021-04-15 | groupId* |  |
| PUT | `/calendars/groups/{groupId}` | Update Group | calendars/groups.write | 2021-04-15 | groupId* | name*, description*, slug* |
| PUT | `/calendars/groups/{groupId}/status` | Disable Group | calendars/groups.write | 2021-04-15 | groupId* | isActive* |
| POST | `/calendars/events/appointments` | Create appointment | calendars/events.write | 2021-04-15 |  | title, meetingLocationType, meetingLocationId, overrideLocationConfig, appointmentStatus, assignedUserId, description, address, ignoreDateRange, toNotify, ignoreFreeSlotValidation, rrule, calendarId*, locationId* … |
| PUT | `/calendars/events/appointments/{eventId}` | Update Appointment | calendars/events.write | 2021-04-15 | eventId* | title, meetingLocationType, meetingLocationId, overrideLocationConfig, appointmentStatus, assignedUserId, description, address, ignoreDateRange, toNotify, ignoreFreeSlotValidation, rrule, calendarId, startTime … |
| GET | `/calendars/events/appointments/{eventId}` | Get Appointment | calendars/events.readonly | 2021-04-15 | eventId* |  |
| GET | `/calendars/events` | Get Calendar Events | calendars/events.readonly | 2021-04-15 | locationId*, userId, calendarId, groupId, startTime*, endTime* |  |
| GET | `/calendars/blocked-slots` | Get Blocked Slots | calendars/events.readonly | 2021-04-15 | locationId*, userId, calendarId, groupId, startTime*, endTime* |  |
| POST | `/calendars/events/block-slots` | Create Block Slot | calendars/events.write | 2021-04-15 |  | title, calendarId*, assignedUserId, locationId*, startTime, endTime |
| PUT | `/calendars/events/block-slots/{eventId}` | Update Block Slot | calendars/events.write | 2021-04-15 | eventId* | title, calendarId*, assignedUserId, locationId*, startTime, endTime |
| GET | `/calendars/{calendarId}/free-slots` | Get Free Slots | calendars.readonly | 2021-04-15 | calendarId*, startDate*, endDate*, timezone, userId, userIds |  |
| PUT | `/calendars/{calendarId}` | Update Calendar | calendars.write | 2021-04-15 | calendarId* | notifications, groupId, teamMembers, eventType, name, description, slug, widgetSlug, widgetType, eventTitle, eventColor, locationConfigurations, meetingLocation, slotDuration … |
| GET | `/calendars/{calendarId}` | Get Calendar | calendars.readonly | 2021-04-15 | calendarId* |  |
| DELETE | `/calendars/{calendarId}` | Delete Calendar | calendars.write | 2021-04-15 | calendarId* |  |
| DELETE | `/calendars/events/{eventId}` | Delete Event | calendars/events.write | 2021-04-15 | eventId* |  |
| GET | `/calendars/appointments/{appointmentId}/notes` | Get Notes | calendars/events.readonly | 2021-04-15 | limit*, offset*, appointmentId* |  |
| POST | `/calendars/appointments/{appointmentId}/notes` | Create Note | calendars/events.write | 2021-04-15 | appointmentId* | userId, body* |
| PUT | `/calendars/appointments/{appointmentId}/notes/{noteId}` | Update Note | calendars/events.write | 2021-04-15 | appointmentId* | userId, body* |
| DELETE | `/calendars/appointments/{appointmentId}/notes/{noteId}` | Delete Note | calendars/events.write | 2021-04-15 | appointmentId* |  |
| GET | `/calendars/resources/{resourceType}/{id}` | Get Calendar Resource | calendars/resources.readonly | 2021-04-15 | resourceType*, id* |  |
| PUT | `/calendars/resources/{resourceType}/{id}` | Update Calendar Resource | calendars/resources.write | 2021-04-15 | resourceType*, id* | locationId, name, description, quantity, outOfService, capacity, calendarIds, isActive |
| DELETE | `/calendars/resources/{resourceType}/{id}` | Delete Calendar Resource | calendars/resources.write | 2021-04-15 | resourceType*, id* |  |
| GET | `/calendars/resources/{resourceType}` | List Calendar Resources | calendars/resources.readonly | 2021-04-15 | resourceType*, locationId*, limit*, skip* |  |
| POST | `/calendars/resources/{resourceType}` | Create Calendar Resource | calendars/resources.write | 2021-04-15 | resourceType* | locationId*, name*, description*, quantity*, outOfService*, capacity*, calendarIds* |
| GET | `/calendars/{calendarId}/notifications` | Get notifications | calendars/events.readonly | 2021-04-15 | calendarId*, isActive, deleted, limit, skip |  |
| POST | `/calendars/{calendarId}/notifications` | Create notification | calendars/events.write | 2021-04-15 | calendarId* |  |
| GET | `/calendars/{calendarId}/notifications/{notificationId}` | Get notification | calendars/events.readonly | 2021-04-15 | calendarId*, notificationId* |  |
| PUT | `/calendars/{calendarId}/notifications/{notificationId}` | Update notification | calendars/events.write | 2021-04-15 | calendarId*, notificationId* | receiverType, additionalEmailIds, additionalPhoneNumbers, selectedUsers, channel, notificationType, isActive, deleted, templateId, body, subject, afterTime, beforeTime, fromAddress … |
| DELETE | `/calendars/{calendarId}/notifications/{notificationId}` | Delete Notification | calendars/events.write | 2021-04-15 | calendarId*, notificationId* |  |
| GET | `/calendars/schedules/search` | List user availability schedule | calendars.readonly | 2021-04-15 | locationId*, userId*, calendarId, skip, limit |  |
| GET | `/calendars/schedules/{id}` | Get user availability schedule | calendars.readonly | 2021-04-15 | id* |  |
| PUT | `/calendars/schedules/{id}` | Update user availability schedule | calendars.write | 2021-04-15 | id* | name, rules, timezone |
| DELETE | `/calendars/schedules/{id}` | Delete user availability schedule | calendars.write | 2021-04-15 | id* |  |
| POST | `/calendars/schedules` | Create user availability schedule | calendars.write | 2021-04-15 |  | rules, timezone*, locationId*, name*, userId*, calendarIds |
| PUT | `/calendars/schedules/{id}/associations/{calendarId}` | Apply user availability schedule to a calendar | calendars.write | 2021-04-15 | id*, calendarId* |  |
| DELETE | `/calendars/schedules/{id}/associations/{calendarId}` | Remove user availability schedule from a calendar | calendars.write | 2021-04-15 | id*, calendarId* |  |
| GET | `/calendars/` | Get Calendars | calendars.readonly | 2021-04-15 | locationId*, groupId, showDrafted |  |
| POST | `/calendars/` | Create Calendar | calendars.write | 2021-04-15 |  | isActive, notifications, locationId*, groupId, teamMembers, eventType, name*, description, slug, widgetSlug, calendarType, widgetType, eventTitle, eventColor … |

### Campaigns API (`apps/campaigns.json`, 1 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/campaigns/` | Get Campaigns | campaigns.readonly | 2021-07-28 | locationId*, status |  |

### Companies API (`apps/companies.json`, 1 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/companies/{companyId}` | Get Company | companies.readonly | 2021-07-28 | companyId* |  |

### Contacts API (`apps/contacts.json`, 32 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/contacts/search` | Search Contacts | contacts.readonly | 2021-07-28 |  |  |
| GET | `/contacts/search/duplicate` | Get Duplicate Contact | contacts.readonly | 2021-07-28 | locationId*, number, email |  |
| GET | `/contacts/{contactId}/tasks` | Get all Tasks | contacts.readonly | 2021-07-28 | contactId* |  |
| POST | `/contacts/{contactId}/tasks` | Create Task | contacts.write | 2021-07-28 | contactId* | title*, body, dueDate*, completed*, assignedTo |
| GET | `/contacts/{contactId}/tasks/{taskId}` | Get Task | contacts.readonly | 2021-07-28 | contactId*, taskId* |  |
| PUT | `/contacts/{contactId}/tasks/{taskId}` | Update Task | contacts.write | 2021-07-28 | contactId*, taskId* | title, body, dueDate, completed, assignedTo |
| DELETE | `/contacts/{contactId}/tasks/{taskId}` | Delete Task | contacts.write | 2021-07-28 | contactId*, taskId* |  |
| PUT | `/contacts/{contactId}/tasks/{taskId}/completed` | Update Task Completed | contacts.write | 2021-07-28 | contactId*, taskId* | completed* |
| GET | `/contacts/{contactId}/appointments` | Get Appointments for Contact | contacts.readonly | 2021-07-28 | contactId* |  |
| POST | `/contacts/{contactId}/tags` | Add Tags | contacts.write | 2021-07-28 | contactId* | tags* |
| DELETE | `/contacts/{contactId}/tags` | Remove Tags | contacts.write | 2021-07-28 | contactId* | tags* |
| GET | `/contacts/{contactId}/notes` | Get All Notes | contacts.readonly | 2021-07-28 | contactId* |  |
| POST | `/contacts/{contactId}/notes` | Create Note | contacts.write | 2021-07-28 | contactId* | userId, body*, title, color, pinned |
| GET | `/contacts/{contactId}/notes/{id}` | Get Note | contacts.readonly | 2021-07-28 | contactId*, id* |  |
| PUT | `/contacts/{contactId}/notes/{id}` | Update Note | contacts.write | 2021-07-28 | contactId*, id* | userId, body, title, color, pinned |
| DELETE | `/contacts/{contactId}/notes/{id}` | Delete Note | contacts.write | 2021-07-28 | contactId*, id* |  |
| POST | `/contacts/bulk/tags/update/{type}` | Update Contacts Tags | — | 2021-07-28 |  | contacts*, tags*, locationId*, removeAllTags |
| POST | `/contacts/bulk/business` | Add/Remove Contacts From Business | — | 2021-07-28 |  | locationId*, ids*, businessId* |
| GET | `/contacts/{contactId}` | Get Contact | contacts.readonly | 2021-07-28 | contactId* |  |
| PUT | `/contacts/{contactId}` | Update Contact | contacts.write | 2021-07-28 | contactId* | firstName, lastName, name, email, phone, address1, city, state, postalCode, website, timezone, dnd, dndSettings, inboundDndSettings … |
| DELETE | `/contacts/{contactId}` | Delete Contact | contacts.write | 2021-07-28 | contactId* |  |
| POST | `/contacts/upsert` | Upsert Contact | contacts.write | 2021-07-28 |  | firstName, lastName, name, email, locationId*, gender, phone, address1, city, state, postalCode, website, timezone, dnd … |
| GET | `/contacts/business/{businessId}` | Get Contacts By BusinessId | contacts.readonly | 2021-07-28 | businessId*, limit, locationId*, skip, query |  |
| POST | `/contacts/{contactId}/followers` | Add Followers | contacts.write | 2021-07-28 | contactId* | followers* |
| DELETE | `/contacts/{contactId}/followers` | Remove Followers | contacts.write | 2021-07-28 | contactId* | followers* |
| POST | `/contacts/{contactId}/campaigns/{campaignId}` | Add Contact to Campaign | contacts.write | 2021-07-28 | contactId*, campaignId* |  |
| DELETE | `/contacts/{contactId}/campaigns/{campaignId}` | Remove Contact From Campaign | contacts.write | 2021-07-28 | contactId*, campaignId* |  |
| DELETE | `/contacts/{contactId}/campaigns/removeAll` | Remove Contact From Every Campaign | contacts.write | 2021-07-28 | contactId* |  |
| POST | `/contacts/{contactId}/workflow/{workflowId}` | Add Contact to Workflow | contacts.write | 2021-07-28 | contactId*, workflowId* | eventStartTime |
| DELETE | `/contacts/{contactId}/workflow/{workflowId}` | Delete Contact from Workflow | contacts.write | 2021-07-28 | contactId*, workflowId* | eventStartTime |
| POST | `/contacts/` | Create Contact | contacts.write | 2021-07-28 |  | firstName, lastName, name, email, locationId*, gender, phone, address1, city, state, postalCode, website, timezone, dnd … |
| GET | `/contacts/` | Get Contacts | contacts.readonly | 2021-07-28 | locationId*, startAfterId, startAfter, query, limit |  |

### Conversation AI API (`apps/conversation-ai.json`, 12 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/conversation-ai/agents/{agentId}/actions` | Attach Action to Agent | conversation-ai.write | 2021-04-15 | agentId* | type*, name*, details* |
| GET | `/conversation-ai/agents/{agentId}/actions/list` | List Actions for an Agent | conversation-ai.readonly | 2021-04-15 | agentId* |  |
| GET | `/conversation-ai/agents/{agentId}/actions/{actionId}` | Get Action by ID | conversation-ai.readonly | 2021-04-15 | actionId*, agentId* |  |
| PUT | `/conversation-ai/agents/{agentId}/actions/{actionId}` | Update Action | conversation-ai.write | 2021-04-15 | actionId*, agentId* | type*, name*, details* |
| DELETE | `/conversation-ai/agents/{agentId}/actions/{actionId}` | Remove Action from Agent | conversation-ai.write | 2021-04-15 | actionId*, agentId* |  |
| PATCH | `/conversation-ai/agents/{agentId}/followup-settings` | Update Followup Settings | conversation-ai.write | 2021-04-15 | agentId* | actionIds*, followupSettings* |
| POST | `/conversation-ai/agents` | Create an Agent | conversation-ai.write | 2021-04-15 |  | name*, businessName, mode, channels, isPrimary, waitTime, waitTimeUnit, sleepEnabled, sleepTime, sleepTimeUnit, personality*, goal*, instructions*, autoPilotMaxMessages … |
| GET | `/conversation-ai/agents/search` | Search Agents | conversation-ai.readonly | 2021-04-15 | startAfter, limit, query |  |
| PUT | `/conversation-ai/agents/{agentId}` | Update Agent | conversation-ai.write | 2021-04-15 | agentId* | name, businessName, mode, channels, isPrimary, waitTime, waitTimeUnit, sleepEnabled, sleepTime, sleepTimeUnit, personality, goal, instructions, autoPilotMaxMessages* … |
| GET | `/conversation-ai/agents/{agentId}` | Get Agent | conversation-ai.readonly | 2021-04-15 | agentId* |  |
| DELETE | `/conversation-ai/agents/{agentId}` | Delete Agent | conversation-ai.write | 2021-04-15 | agentId* |  |
| GET | `/conversation-ai/generations` | Get the generation details | conversation-ai.readonly | 2021-04-15 | messageId*, source* |  |

### Conversations API (`apps/conversations.json`, 29 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/conversations/search` | Search Conversations | conversations.readonly | 2021-04-15 | locationId*, contactId, assignedTo, followers, mentions, query, sort, startAfterDate, id, limit, lastMessageType, lastMessageAction, lastMessageDirection, status, sortBy, sortScoreProfile, scoreProfile, scoreProfileMin, scoreProfileMax, startDate, endDate |  |
| GET | `/conversations/{conversationId}` | Get Conversation | conversations.readonly | 2021-04-15 | conversationId* |  |
| PUT | `/conversations/{conversationId}` | Update Conversation | conversations.write | 2021-04-15 | conversationId* | locationId*, unreadCount, starred, feedback |
| DELETE | `/conversations/{conversationId}` | Delete Conversation | conversations.write | 2021-04-15 | conversationId* |  |
| GET | `/conversations/preferences/custom-subtypes` | Get All Custom Subtypes | — | 2021-04-15 | locationId* |  |
| POST | `/conversations/preferences/custom-subtypes` | Create Custom Subtype | — | 2021-04-15 | locationId* | name*, description, channel*, language* |
| PUT | `/conversations/preferences/custom-subtypes/{id}` | Update Custom Subtype | — | 2021-04-15 | id*, locationId* | name, description, archived, resubscription_legal_form_id |
| GET | `/conversations/preferences/unsubscriptions/status` | Get Contact Unsubscription Status | — | 2021-04-15 | locationId*, contactId*, email |  |
| POST | `/conversations/preferences/unsubscriptions/user-change` | User Subscription Change | — | 2021-04-15 |  | locationId*, contactId*, email*, subscription_action*, legal_reason, legal_description |
| GET | `/conversations/messages/email/{id}` | Get email by Id | — | — |  |  |
| DELETE | `/conversations/messages/email/{emailMessageId}/schedule` | Cancel a scheduled email message. | — | — | emailMessageId* |  |
| GET | `/conversations/messages/export` | Export messages by location ID | conversations/message.readonly | 2021-04-15 | locationId*, limit, cursor, sortBy, sortOrder, conversationId, contactId, channel, startDate, endDate |  |
| GET | `/conversations/messages/{id}` | Get message by message id | conversations/message.readonly | 2021-04-15 |  |  |
| GET | `/conversations/{conversationId}/messages` | Get messages by conversation id | conversations/message.readonly | 2021-04-15 | conversationId*, lastMessageId, limit, type |  |
| POST | `/conversations/messages` | Send a new message | conversations/message.write | 2021-04-15 |  | type*, subType*, contactId*, appointmentId, attachments, emailFrom, emailCc, emailBcc, html, message, subject, replyMessageId, templateId, threadId … |
| POST | `/conversations/messages/inbound` | Add an inbound message | conversations/message.write | 2021-04-15 |  | type*, attachments, message, conversationId*, contactId*, conversationProviderId*, html, subject, emailFrom, emailTo, emailCc, emailBcc, emailMessageId, altId … |
| POST | `/conversations/messages/outbound` | Add an external outbound call | conversations/message.write | 2021-04-15 |  | type*, attachments, conversationId*, conversationProviderId*, altId, date, call |
| POST | `/conversations/messages/review-reply` | Send a review reply to Google My Business | conversations/message.write | 2021-04-15 |  | conversationId*, locationId*, message* |
| DELETE | `/conversations/messages/{messageId}/schedule` | Cancel a scheduled message. | conversations/message.write | 2021-04-15 | messageId* |  |
| POST | `/conversations/messages/upload` | Upload file attachments | conversations/message.write | 2021-04-15 |  |  |
| POST | `/conversations/messages/upload/initiate` | Initiate file upload to GCS | conversations/message.write | 2021-04-15 |  | locationId*, conversationId*, filename*, contentType*, fileSize, channel* |
| POST | `/conversations/messages/upload/complete` | Complete file upload | conversations/message.write | 2021-04-15 |  | uploadId*, filePath*, locationId*, conversationId*, filename* |
| PUT | `/conversations/messages/{messageId}/status` | Update message status | conversations/message.write | 2021-04-15 | messageId* | status*, error, emailMessageId, recipients |
| PUT | `/conversations/messages/{messageId}/attachments` | Add message attachments | conversations/message.write | 2021-04-15 | messageId* | attachments* |
| GET | `/conversations/messages/{messageId}/locations/{locationId}/recording` | Get Recording by Message ID | conversations/message.readonly | 2021-04-15 | locationId*, messageId* |  |
| GET | `/conversations/locations/{locationId}/messages/{messageId}/transcription` | Get transcription by Message ID | conversations/message.readonly | 2021-04-15 | locationId*, messageId* |  |
| GET | `/conversations/locations/{locationId}/messages/{messageId}/transcription/download` | Download transcription by Message ID | conversations/message.readonly | 2021-04-15 | locationId*, messageId* |  |
| POST | `/conversations/providers/live-chat/typing` | Agent/Ai-Bot is typing a message indicator for live chat | conversations/livechat.write | 2021-04-15 |  | locationId*, isTyping*, visitorId*, conversationId* |
| POST | `/conversations/` | Create Conversation | conversations.write | 2021-04-15 |  | locationId*, contactId* |

### MEMBERSHIPS API (`apps/courses.json`, 1 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/courses/courses-exporter/public/import` | Import Courses | — | 2021-07-28 |  | locationId*, userId, products* |

### Custom Fields V2 (`apps/custom-fields.json`, 8 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/custom-fields/{id}` | Get Custom Field / Folder By Id | locations/customFields.readonly | 2021-07-28 | id* |  |
| PUT | `/custom-fields/{id}` | Update Custom Field By Id | locations/customFields.write | 2021-07-28 | id* | locationId*, name, description, placeholder, showInForms*, options, acceptedFormats, maxFileLimit |
| DELETE | `/custom-fields/{id}` | Delete Custom Field By Id | locations/customFields.write | 2021-07-28 | id* |  |
| GET | `/custom-fields/object-key/{objectKey}` | Get Custom Fields By Object Key | locations/customFields.readonly | 2021-07-28 | objectKey*, locationId* |  |
| POST | `/custom-fields/folder` | Create Custom Field Folder | locations/customFields.write | 2021-07-28 |  | objectKey*, name*, locationId* |
| PUT | `/custom-fields/folder/{id}` | Update Custom Field Folder Name | locations/customFields.write | 2021-07-28 | id* | name*, locationId* |
| DELETE | `/custom-fields/folder/{id}` | Delete Custom Field Folder | locations/customFields.write | 2021-07-28 | id*, locationId* |  |
| POST | `/custom-fields/` | Create Custom Field | locations/customFields.write | 2021-07-28 |  | locationId*, name, description, placeholder, showInForms*, options, acceptedFormats, dataType*, fieldKey*, objectKey*, maxFileLimit, allowCustomOption, parentId* |

### Custom menus API (`apps/custom-menus.json`, 5 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/custom-menus/{customMenuId}` | Get Custom Menu Link | custom-menu-link.readonly | 2021-07-28 | customMenuId* |  |
| DELETE | `/custom-menus/{customMenuId}` | Delete Custom Menu Link | custom-menu-link.write | 2021-07-28 | customMenuId* |  |
| PUT | `/custom-menus/{customMenuId}` | Update Custom Menu Link | custom-menu-link.write | 2021-07-28 | customMenuId* | title, url, icon, showOnCompany, showOnLocation, showToAllLocations, openMode, locations, userRole, allowCamera, allowMicrophone |
| GET | `/custom-menus/` | Get Custom Menu Links | custom-menu-link.readonly | 2021-07-28 | locationId, skip, limit, query, showOnCompany |  |
| POST | `/custom-menus/` | Create Custom Menu Link | custom-menu-link.write | 2021-07-28 |  | title*, url*, icon*, showOnCompany*, showOnLocation*, showToAllLocations*, openMode*, locations*, userRole*, allowCamera, allowMicrophone |

### Email ISV API (`apps/email-isv.json`, 1 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/email/verify` | Email Verification | — | 2021-07-28 | locationId* | type*, verify* |

### Email API (`apps/emails.json`, 5 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/emails/schedule` | Get Campaigns | emails/schedule.readonly | 2021-07-28 | locationId*, limit, offset, status, emailStatus, name, parentId, limitedFields, archived, campaignsOnly, showStats |  |
| POST | `/emails/builder` | Create a new template | emails/builder.write | 2021-07-28 |  | locationId*, title, type*, updatedBy, builderVersion, name, parentId, templateDataUrl, importProvider*, importURL, templateSource, isPlainText |
| GET | `/emails/builder` | Fetch email templates | emails/builder.readonly | 2021-07-28 | locationId*, limit, offset, search, sortByDate, archived, builderVersion, name, parentId, originId, templatesOnly |  |
| DELETE | `/emails/builder/{locationId}/{templateId}` | Delete a template | — | 2021-07-28 | locationId*, templateId* |  |
| POST | `/emails/builder/data` | Update a template | emails/builder.write | 2021-07-28 |  | locationId*, templateId*, updatedBy*, dnd*, html*, editorType*, previewText, isPlainText |

### Forms API (`apps/forms.json`, 3 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/forms/submissions` | Get Forms Submissions | forms.readonly | 2021-07-28 | locationId*, page, limit, formId, q, startAt, endAt |  |
| POST | `/forms/upload-custom-files` | Upload files to custom fields | forms.write | 2021-07-28 | contactId*, locationId* |  |
| GET | `/forms/` | Get Forms | forms.readonly | 2021-07-28 | locationId*, skip, limit, type |  |

### Funnels API (`apps/funnels.json`, 7 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/funnels/lookup/redirect` | Create Redirect | funnels/redirect.write | 2021-07-28 |  | locationId*, domain*, path*, target*, action* |
| PATCH | `/funnels/lookup/redirect/{id}` | Update Redirect By Id | funnels/redirect.write | 2021-07-28 | id* | target*, action*, locationId* |
| DELETE | `/funnels/lookup/redirect/{id}` | Delete Redirect By Id | funnels/redirect.write | 2021-07-28 | id*, locationId* |  |
| GET | `/funnels/lookup/redirect/list` | Fetch List of Redirects | funnels/redirect.readonly | 2021-07-28 | locationId*, limit*, offset*, search |  |
| GET | `/funnels/funnel/list` | Fetch List of Funnels | — | — | locationId*, type, category, offset, limit, parentId, name |  |
| GET | `/funnels/page` | Fetch list of funnel pages | — | — | locationId*, funnelId*, name, limit*, offset* |  |
| GET | `/funnels/page/count` | Fetch count of funnel pages | — | — | locationId*, funnelId*, name |  |

### Invoice API (`apps/invoices.json`, 42 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/invoices/template` | Create template | invoices/template.write | 2021-07-28 |  | altId*, altType*, internal, name*, businessDetails*, currency*, items*, automaticTaxesEnabled, discount, termsNotes, title, tipsConfiguration, lateFeesConfiguration, invoiceNumberPrefix … |
| GET | `/invoices/template` | List templates | invoices/template.readonly | 2021-07-28 | altId*, altType*, status, startAt, endAt, search, paymentMode, limit*, offset* |  |
| GET | `/invoices/template/{templateId}` | Get an template | invoices/template.readonly | 2021-07-28 | templateId*, altId*, altType* |  |
| PUT | `/invoices/template/{templateId}` | Update template | invoices/template.write | 2021-07-28 | templateId* | altId*, altType*, internal, name*, businessDetails*, currency*, items*, discount, termsNotes, title, miscellaneousCharges |
| DELETE | `/invoices/template/{templateId}` | Delete template | invoices/template.write | 2021-07-28 | templateId*, altId*, altType* |  |
| PATCH | `/invoices/template/{templateId}/late-fees-configuration` | Update template late fees configuration | — | 2021-07-28 | templateId* | altId*, altType*, lateFeesConfiguration* |
| PATCH | `/invoices/template/{templateId}/payment-methods-configuration` | Update template late fees configuration | — | 2021-07-28 | templateId* | altId*, altType*, paymentMethods |
| POST | `/invoices/schedule` | Create Invoice Schedule | invoices/schedule.write | 2021-07-28 |  | altId*, altType*, name*, contactDetails*, schedule*, liveMode*, businessDetails*, currency*, items*, automaticTaxesEnabled, discount*, termsNotes, title, tipsConfiguration … |
| GET | `/invoices/schedule` | List schedules | invoices/schedule.readonly | 2021-07-28 | altId*, altType*, status, startAt, endAt, search, paymentMode, limit*, offset* |  |
| GET | `/invoices/schedule/{scheduleId}` | Get an schedule | invoices/schedule.readonly | 2021-07-28 | scheduleId*, altId*, altType* |  |
| PUT | `/invoices/schedule/{scheduleId}` | Update schedule | invoices/schedule.write | 2021-07-28 | scheduleId* | altId*, altType*, name*, contactDetails*, schedule*, liveMode*, businessDetails*, currency*, items*, discount*, termsNotes, title, attachments, miscellaneousCharges |
| DELETE | `/invoices/schedule/{scheduleId}` | Delete schedule | invoices/schedule.write | 2021-07-28 | scheduleId*, altId*, altType* |  |
| POST | `/invoices/schedule/{scheduleId}/updateAndSchedule` | Update scheduled recurring invoice | invoices/schedule.write | 2021-07-28 | scheduleId* |  |
| POST | `/invoices/schedule/{scheduleId}/schedule` | Schedule an schedule invoice | invoices/schedule.write | 2021-07-28 | scheduleId* | altId*, altType*, liveMode*, autoPayment |
| POST | `/invoices/schedule/{scheduleId}/auto-payment` | Manage Auto payment for an schedule invoice | invoices/schedule.write | 2021-07-28 | scheduleId* | altId*, altType*, id*, autoPayment* |
| POST | `/invoices/schedule/{scheduleId}/cancel` | Cancel an scheduled invoice | invoices/schedule.write | 2021-07-28 | scheduleId* | altId*, altType* |
| POST | `/invoices/text2pay` | Create & Send | invoices.write | 2021-07-28 |  | altId*, altType*, name*, currency*, items*, termsNotes, title, contactDetails*, invoiceNumber, issueDate*, dueDate, sentTo*, liveMode*, automaticTaxesEnabled … |
| GET | `/invoices/generate-invoice-number` | Generate Invoice Number | invoices.readonly | 2021-07-28 | altId*, altType* |  |
| GET | `/invoices/settings` | Get Invoice Settings | invoices.readonly | 2021-07-28 | altId*, altType* |  |
| GET | `/invoices/{invoiceId}` | Get invoice | invoices.readonly | 2021-07-28 | invoiceId*, altId*, altType* |  |
| PUT | `/invoices/{invoiceId}` | Update invoice | invoices.write | 2021-07-28 | invoiceId* | altId*, altType*, name*, title, currency*, description, businessDetails, invoiceNumber, contactId, contactDetails, termsNotes, discount, invoiceItems*, automaticTaxesEnabled … |
| DELETE | `/invoices/{invoiceId}` | Delete invoice | invoices.write | 2021-07-28 | invoiceId*, altId*, altType* |  |
| PATCH | `/invoices/{invoiceId}/late-fees-configuration` | Update invoice late fees configuration | — | 2021-07-28 | invoiceId* | altId*, altType*, lateFeesConfiguration* |
| POST | `/invoices/{invoiceId}/void` | Void invoice | invoices.write | 2021-07-28 | invoiceId* | altId*, altType* |
| POST | `/invoices/{invoiceId}/send` | Send invoice | invoices.write | 2021-07-28 | invoiceId* | altId*, altType*, userId*, action*, liveMode*, sentFrom, autoPayment |
| POST | `/invoices/{invoiceId}/record-payment` | Record a manual payment for an invoice | invoices.write | 2021-07-28 | invoiceId* | altId*, altType*, mode*, card*, cheque*, notes*, amount, meta, paymentScheduleIds, fulfilledAt |
| PATCH | `/invoices/stats/last-visited-at` | Update invoice last visited at | — | 2021-07-28 |  | invoiceId* |
| POST | `/invoices/estimate` | Create New Estimate | invoices/estimate.write | 2021-07-28 |  | altId*, altType*, name*, businessDetails*, currency*, items*, liveMode, discount*, termsNotes, title, contactDetails*, estimateNumber, issueDate, expiryDate … |
| PUT | `/invoices/estimate/{estimateId}` | Update Estimate | invoices/estimate.write | 2021-07-28 | estimateId* | altId*, altType*, name*, businessDetails*, currency*, items*, liveMode, discount*, termsNotes, title, contactDetails*, estimateNumber, issueDate, expiryDate … |
| DELETE | `/invoices/estimate/{estimateId}` | Delete Estimate | invoices/estimate.write | 2021-07-28 | estimateId* | altId*, altType* |
| GET | `/invoices/estimate/number/generate` | Generate Estimate Number | invoices/estimate.readonly | 2021-07-28 | altId*, altType* |  |
| POST | `/invoices/estimate/{estimateId}/send` | Send Estimate | invoices/estimate.write | 2021-07-28 | estimateId* | altId*, altType*, action*, liveMode*, userId*, sentFrom, estimateName |
| POST | `/invoices/estimate/{estimateId}/invoice` | Create Invoice from Estimate | invoices/estimate.write | 2021-07-28 | estimateId* | altId*, altType*, markAsInvoiced*, version |
| GET | `/invoices/estimate/list` | List Estimates | invoices/estimate.readonly | 2021-07-28 | altId*, altType*, startAt, endAt, search, status, contactId, limit*, offset* |  |
| PATCH | `/invoices/estimate/stats/last-visited-at` | Update estimate last visited at | — | 2021-07-28 |  | estimateId* |
| GET | `/invoices/estimate/template` | List Estimate Templates | invoices/estimate.readonly | 2021-07-28 | altId*, altType*, search, limit*, offset* |  |
| POST | `/invoices/estimate/template` | Create Estimate Template | invoices/estimate.write | 2021-07-28 |  | altId*, altType*, name*, businessDetails*, currency*, items*, liveMode, discount*, termsNotes, title, automaticTaxesEnabled, meta, sendEstimateDetails, estimateNumberPrefix … |
| PUT | `/invoices/estimate/template/{templateId}` | Update Estimate Template | invoices/estimate.write | 2021-07-28 | templateId* | altId*, altType*, name*, businessDetails*, currency*, items*, liveMode, discount*, termsNotes, title, automaticTaxesEnabled, meta, sendEstimateDetails, estimateNumberPrefix … |
| DELETE | `/invoices/estimate/template/{templateId}` | Delete Estimate Template | invoices/estimate.write | 2021-07-28 | templateId* | altId*, altType* |
| GET | `/invoices/estimate/template/preview` | Preview Estimate Template | invoices/estimate.readonly | 2021-07-28 | altId*, altType*, templateId* |  |
| POST | `/invoices/` | Create Invoice | invoices.write | 2021-07-28 |  | altId*, altType*, name*, businessDetails*, currency*, items*, discount*, termsNotes, title, contactDetails*, invoiceNumber, issueDate*, dueDate, sentTo* … |
| GET | `/invoices/` | List invoices | invoices.readonly | 2021-07-28 | altId*, altType*, status, startAt, endAt, search, paymentMode, contactId, limit*, offset*, sortField, sortOrder |  |

### Knowledge Base API (`apps/knowledge-base.json`, 14 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/knowledge-bases/faqs` | Get all FAQs by knowledge base with pagination support | — | 2021-04-15 | knowledgeBaseId*, locationId*, limit, lastFaqId |  |
| POST | `/knowledge-bases/faqs` | Create a new FAQ inside knowledge base | — | 2021-04-15 |  | locationId*, question*, answer*, knowledgeBaseId* |
| PUT | `/knowledge-bases/faqs/{id}` | Update an existing knowledge base FAQ | — | 2021-04-15 | id* | question*, answer* |
| DELETE | `/knowledge-bases/faqs/{id}` | Delete an existing knowledge base FAQ | — | 2021-04-15 | id* |  |
| GET | `/knowledge-bases/crawler` | Get all trained page links by knowledge base | — | 2021-04-15 | knowledgeBaseId*, locationId*, page, pageLength, query |  |
| POST | `/knowledge-bases/crawler` | Start crawling and discover pages for training | — | 2021-04-15 |  | locationId*, url*, option*, knowledgeBaseId* |
| DELETE | `/knowledge-bases/crawler` | Delete trained pages | — | 2021-04-15 |  | knowledgeBaseId*, locationId*, urlIds* |
| GET | `/knowledge-bases/crawler/status` | Get crawling status for the latest operation | — | 2021-04-15 | locationId*, operationId*, knowledgeBaseId* |  |
| POST | `/knowledge-bases/crawler/train` | Train discovered website pages and ingest into the knowledge base | — | 2021-04-15 |  | locationId*, urlIds*, knowledgeBaseId*, operationId* |
| GET | `/knowledge-bases/{knowledgeBaseId}` | Get knowledge base by ID | — | 2021-04-15 | knowledgeBaseId* |  |
| DELETE | `/knowledge-bases/{knowledgeBaseId}` | Delete a knowledge base | — | 2021-04-15 | knowledgeBaseId* |  |
| PUT | `/knowledge-bases/{id}` | Update a knowledge base | — | 2021-04-15 | id* | name, description |
| GET | `/knowledge-bases/` | Get all knowledge bases for a location by location Id (paginated) | — | 2021-04-15 | locationId*, query, limit, lastKnowledgeBaseId |  |
| POST | `/knowledge-bases/` | Create a new knowledge base (max 15 knowledge bases per location) | — | 2021-04-15 |  | name*, description, locationId* |

### Trigger Links API (`apps/links.json`, 6 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/links/id/{linkId}` | Get Link by ID | — | 2021-07-28 | locationId*, linkId* |  |
| PUT | `/links/{linkId}` | Update Link | links.write | 2021-07-28 | linkId* | name*, redirectTo* |
| DELETE | `/links/{linkId}` | Delete Link | links.write | 2021-07-28 | linkId* |  |
| GET | `/links/search` | Search Trigger Links | — | 2021-04-15 | locationId*, query, skip, limit |  |
| GET | `/links/` | Get Links | links.readonly | 2021-07-28 | locationId* |  |
| POST | `/links/` | Create Link | links.write | 2021-07-28 |  | locationId*, name*, redirectTo* |

### Sub-Account (Formerly location) API (`apps/locations.json`, 29 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/locations/search` | Search | locations.readonly | 2021-07-28 | companyId, skip, limit, order, email |  |
| GET | `/locations/{locationId}` | Get Sub-Account (Formerly Location) | locations.readonly | 2021-07-28 | locationId* |  |
| PUT | `/locations/{locationId}` | Put Sub-Account (Formerly Location) | locations.write | 2021-07-28 | locationId* | name, phone, companyId*, address, city, state, country, postalCode, website, timezone, prospectInfo, settings, social, twilio … |
| DELETE | `/locations/{locationId}` | Delete Sub-Account (Formerly Location) | locations.internal-access-only | 2021-07-28 | locationId*, deleteTwilioAccount* |  |
| GET | `/locations/{locationId}/tags` | Get Tags | locations/tags.readonly | 2021-07-28 | locationId* |  |
| POST | `/locations/{locationId}/tags` | Create Tag | locations/tags.write | 2021-07-28 | locationId* | name* |
| GET | `/locations/{locationId}/tags/{tagId}` | Get tag by id | — | 2021-07-28 | locationId*, tagId* |  |
| PUT | `/locations/{locationId}/tags/{tagId}` | Update tag | — | 2021-07-28 | locationId*, tagId* | name* |
| DELETE | `/locations/{locationId}/tags/{tagId}` | Delete tag | — | 2021-07-28 | locationId*, tagId* |  |
| POST | `/locations/{locationId}/tasks/search` | Task Search Filter | locations/tasks.readonly | 2021-07-28 | locationId* | contactId, completed, assignedTo, query, limit, skip, businessId |
| GET | `/locations/{locationId}/recurring-tasks/{id}` | Get Recurring Task By Id | — | 2021-07-28 | id*, locationId* |  |
| PUT | `/locations/{locationId}/recurring-tasks/{id}` | Update Recurring Task | — | 2021-07-28 | id*, locationId* | title, description, contactIds, owners, rruleOptions, ignoreTaskCreation |
| DELETE | `/locations/{locationId}/recurring-tasks/{id}` | Delete Recurring Task | — | 2021-07-28 | id*, locationId* |  |
| POST | `/locations/{locationId}/recurring-tasks` | Create Recurring Task | — | 2021-07-28 | locationId* | title*, description, contactIds, owners, rruleOptions*, ignoreTaskCreation |
| GET | `/locations/{locationId}/customFields` | Get Custom Fields | locations/customFields.readonly | 2021-07-28 | locationId*, model |  |
| POST | `/locations/{locationId}/customFields` | Create Custom Field | locations/customFields.write | 2021-07-28 | locationId* | name*, dataType*, placeholder, acceptedFormat, isMultipleFile, maxNumberOfFiles, textBoxListOptions, position, model |
| GET | `/locations/{locationId}/customFields/{id}` | Get Custom Field | — | 2021-07-28 | locationId*, id* |  |
| PUT | `/locations/{locationId}/customFields/{id}` | Update Custom Field | — | 2021-07-28 | locationId*, id* | name*, placeholder, acceptedFormat, isMultipleFile, maxNumberOfFiles, textBoxListOptions, position, model |
| DELETE | `/locations/{locationId}/customFields/{id}` | Delete Custom Field | — | 2021-07-28 | locationId*, id* |  |
| POST | `/locations/{locationId}/customFields/upload` | Uploads File to customFields | locations/customFields.write | 2021-07-28 | locationId* |  |
| GET | `/locations/{locationId}/customValues` | Get Custom Values | locations/customValues.readonly | 2021-07-28 | locationId* |  |
| POST | `/locations/{locationId}/customValues` | Create Custom Value | locations/customValues.write | 2021-07-28 | locationId* | name*, value* |
| GET | `/locations/{locationId}/customValues/{id}` | Get Custom Value | — | 2021-07-28 | locationId*, id* |  |
| PUT | `/locations/{locationId}/customValues/{id}` | Update Custom Value | — | 2021-07-28 | locationId*, id* | name*, value* |
| DELETE | `/locations/{locationId}/customValues/{id}` | Delete Custom Value | — | 2021-07-28 | locationId*, id* |  |
| GET | `/locations/{locationId}/timezones` | Fetch Timezones | locations.readonly | 2021-07-28 |  |  |
| GET | `/locations/{locationId}/templates` | GET all or email/sms templates | locations/templates.readonly | 2021-07-28 | deleted, skip, limit, type, originId*, locationId* |  |
| DELETE | `/locations/{locationId}/templates/{id}` | DELETE an email/sms template | — | 2021-07-28 | locationId*, id* |  |
| POST | `/locations/` | Create Sub-Account (Formerly Location) | locations.write | 2021-07-28 |  | name*, phone, companyId*, address, city, state, country, postalCode, website, timezone, prospectInfo, settings, social, twilio … |

### Developer marketplace API (`apps/marketplace.json`, 9 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/marketplace/billing/charges` | Create a new wallet charge | charges.write | — |  | appId*, meterId*, eventId*, userId, locationId*, companyId*, description*, price, units*, eventTime |
| GET | `/marketplace/billing/charges` | Get all wallet charges | charges.readonly | — | meterId, eventId, userId, startDate, endDate, skip, limit |  |
| DELETE | `/marketplace/billing/charges/{chargeId}` | Delete a wallet charge | charges.write | — | chargeId* |  |
| GET | `/marketplace/billing/charges/{chargeId}` | Get specific wallet charge details | charges.readonly | — | chargeId* |  |
| GET | `/marketplace/billing/charges/has-funds` | Check if account has sufficient funds | charges.readonly | — |  |  |
| DELETE | `/marketplace/app/{appId}/installations` | Uninstall an application | oauth.write | 2021-07-28 | appId* | companyId, locationId, reason |
| GET | `/marketplace/app/{appId}/installations` | Get Installer Details | marketplace-installer-details.readonly | 2021-07-28 | appId* |  |
| GET | `/marketplace/app/{appId}/rebilling-config/location/{locationId}` | Get rebilling config for an app subscription and usage plans | oauth.readonly | 2021-07-28 | appId*, locationId* |  |
| POST | `/marketplace/external-auth/migration` | Migrate external authentication connection | marketplace-external-auth-migration.write | 2021-07-28 |  | type*, locationId*, appId*, appVersionId*, accountId*, apiKey, basicCredentials, accessToken, refreshToken, expiryIn, expiryAt, scopes, displayName, isDefault |

### Media Storage API (`apps/medias.json`, 7 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/medias/files` | Get List of Files/ Folders | medias.readonly | 2021-07-28 | offset, limit, sortBy*, sortOrder*, type*, query, altType*, altId*, parentId, fetchAll |  |
| POST | `/medias/upload-file` | Upload File into Media Storage | medias.write | 2021-07-28 |  |  |
| DELETE | `/medias/{id}` | Delete File or Folder | medias.write | 2021-07-28 | id*, altType*, altId* |  |
| POST | `/medias/{id}` | Update File/ Folder | — | 2021-07-28 | id* | name*, altType*, altId* |
| POST | `/medias/folder` | Create Folder | — | 2021-07-28 |  | altId*, altType*, name*, parentId |
| PUT | `/medias/update-files` | Bulk Update Files/ Folders | — | 2021-07-28 |  | altId*, altType*, filesToBeUpdated* |
| PUT | `/medias/delete-files` | Bulk Delete / Trash Files or Folders | — | 2021-07-28 |  | filesToBeDeleted*, altType*, altId*, status* |

### OAuth 2.0 (`apps/oauth.json`, 3 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/oauth/token` | Get Access Token | — | — |  |  |
| POST | `/oauth/locationToken` | Get Location Access Token from Agency Token | oauth.write | 2021-07-28 |  |  |
| GET | `/oauth/installedLocations` | Get Location where app is installed | oauth.readonly | 2021-07-28 | skip, limit, query, isInstalled, companyId*, appId*, versionId, onTrial, planId, locationId |  |

### CUSTOM_OBJECTS API (`apps/objects.json`, 9 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/objects/{key}` | Get Object Schema by key / id | objects/schema.readonly | 2021-07-28 | key*, locationId*, fetchProperties |  |
| PUT | `/objects/{key}` | Update Object Schema By Key / Id | objects/schema.write | 2021-07-28 | key* | labels, description, locationId*, searchableProperties* |
| GET | `/objects/{schemaKey}/records/{id}` | Get Record By Id | — | 2021-07-28 | schemaKey*, id* |  |
| PUT | `/objects/{schemaKey}/records/{id}` | Update Record | — | 2021-07-28 | schemaKey*, id*, locationId* |  |
| DELETE | `/objects/{schemaKey}/records/{id}` | Delete Record | — | 2021-07-28 | schemaKey*, id* |  |
| POST | `/objects/{schemaKey}/records` | Create Record | objects/record.write | 2021-07-28 | schemaKey* |  |
| POST | `/objects/{schemaKey}/records/search` | Search Object Records | objects/record.readonly | 2021-07-28 | schemaKey | locationId*, page*, pageLimit*, query*, searchAfter* |
| GET | `/objects/` | Get all objects for a location | objects/schema.readonly | 2021-07-28 | locationId* |  |
| POST | `/objects/` | Create Custom Object | objects/schema.write | 2021-07-28 |  | labels*, key*, description, locationId*, primaryDisplayPropertyDetails* |

### Opportunities API (`apps/opportunities.json`, 12 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/opportunities/lost-reason` | Get lost reason | opportunities.readonly | 2021-07-28 | locationId*, name, deleted, query, skip, limit, getCount |  |
| GET | `/opportunities/search` | Search Opportunity | opportunities.readonly | 2021-07-28 | q, location_id*, pipeline_id, pipeline_stage_id, contact_id, status, assigned_to, campaignId, id, order, endDate, startAfter, startAfterId, date, country, page, limit, getTasks, getNotes, getCalendarEvents |  |
| POST | `/opportunities/search` | Search Opportunities | opportunities.readonly | 2021-07-28 |  | locationId*, query*, limit*, page*, searchAfter*, additionalDetails* |
| GET | `/opportunities/pipelines` | Get Pipelines | opportunities.readonly | 2021-07-28 | locationId* |  |
| GET | `/opportunities/{id}` | Get Opportunity | opportunities.readonly | 2021-07-28 | id* |  |
| DELETE | `/opportunities/{id}` | Delete Opportunity | opportunities.write | 2021-07-28 | id* |  |
| PUT | `/opportunities/{id}` | Update Opportunity | opportunities.write | 2021-07-28 | id* | pipelineId, name, pipelineStageId, status, monetaryValue, assignedTo, customFields |
| PUT | `/opportunities/{id}/status` | Update Opportunity Status | opportunities.write | 2021-07-28 | id* | status*, lostReasonId |
| POST | `/opportunities/upsert` | Upsert Opportunity | opportunities.write | 2021-07-28 |  | id, pipelineId*, locationId*, followers*, isRemoveAllFollowers*, followersActionType*, name, status, pipelineStageId, monetaryValue, assignedTo, lostReasonId |
| POST | `/opportunities/{id}/followers` | Add Followers | opportunities.write | 2021-07-28 | id* | followers* |
| DELETE | `/opportunities/{id}/followers` | Remove Followers | opportunities.write | 2021-07-28 | id*, isRemoveAllFollowers | followers* |
| POST | `/opportunities/` | Create Opportunity | opportunities.write | 2021-07-28 |  | pipelineId*, locationId*, name*, pipelineStageId, status*, contactId*, monetaryValue, assignedTo, customFields |

### Payments API (`apps/payments.json`, 23 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/payments/integrations/provider/whitelabel` | Create White-label Integration Provider | payments/integration.write | 2021-07-28 |  | altId*, altType*, uniqueName*, title*, provider*, description*, imageUrl* |
| GET | `/payments/integrations/provider/whitelabel` | List White-label Integration Providers | payments/integration.readonly | 2021-07-28 | altId*, altType*, limit, offset |  |
| GET | `/payments/orders` | List Orders | payments/orders.readonly | 2021-07-28 | locationId, altId*, status, paymentStatus, paymentMode, startAt, endAt, search, contactId, funnelProductIds, sourceId, limit, offset |  |
| GET | `/payments/orders/{orderId}` | Get Order by ID | payments/orders.readonly | 2021-07-28 | orderId*, locationId, altId* |  |
| POST | `/payments/orders/{orderId}/record-payment` | Record Order Payment | payments/orders.collectPayment | 2021-07-28 | orderId* | altId*, altType*, mode*, card, cheque, notes, amount, meta, isPartialPayment |
| POST | `/payments/orders/{orderId}/fulfillments` | Create order fulfillment | payments/orders.write | 2021-07-28 | orderId* | altId*, altType*, trackings*, items*, notifyCustomer* |
| GET | `/payments/orders/{orderId}/fulfillments` | List fulfillment | payments/orders.readonly | 2021-07-28 | altId*, altType*, orderId* |  |
| GET | `/payments/orders/{orderId}/notes` | List Order Notes | — | 2021-07-28 | altId*, altType*, orderId* |  |
| GET | `/payments/transactions` | List Transactions | payments/transactions.readonly | 2021-07-28 | locationId, altId*, altType*, paymentMode, startAt, endAt, entitySourceType, entitySourceSubType, search, subscriptionId, entityId, contactId, limit, offset |  |
| GET | `/payments/transactions/{transactionId}` | Get Transaction by ID | payments/transactions.readonly | 2021-07-28 | transactionId*, locationId, altId*, altType* |  |
| GET | `/payments/subscriptions` | List Subscriptions | payments/subscriptions.readonly | 2021-07-28 | altId*, altType*, entityId, paymentMode, startAt, endAt, entitySourceType, search, contactId, id, limit, offset, getPaymentsCollectedCount |  |
| GET | `/payments/subscriptions/{subscriptionId}` | Get Subscription by ID | payments/subscriptions.readonly | 2021-07-28 | subscriptionId*, altId*, altType* |  |
| GET | `/payments/coupon/list` | List Coupons | payments/coupons.readonly | 2021-07-28 | altId*, altType*, limit, offset, status, search |  |
| POST | `/payments/coupon` | Create Coupon | payments/coupons.write | 2021-07-28 |  | altId*, altType*, name*, code*, discountType*, discountValue*, startDate*, endDate, usageLimit, productIds, applyToFuturePayments, applyToFuturePaymentsConfig, limitPerCustomer |
| PUT | `/payments/coupon` | Update Coupon | payments/coupons.write | 2021-07-28 |  | altId*, altType*, name*, code*, discountType*, discountValue*, startDate*, endDate, usageLimit, productIds, applyToFuturePayments, applyToFuturePaymentsConfig, limitPerCustomer, id* |
| DELETE | `/payments/coupon` | Delete Coupon | payments/coupons.write | 2021-07-28 |  | altId*, altType*, id* |
| GET | `/payments/coupon` | Fetch Coupon | payments/coupons.readonly | 2021-07-28 | altId*, altType*, id*, code* |  |
| POST | `/payments/custom-provider/provider` | Create new integration | payments/custom-provider.write | 2021-07-28 | locationId* | name*, description*, paymentsUrl*, queryUrl*, imageUrl*, supportsSubscriptionSchedule* |
| DELETE | `/payments/custom-provider/provider` | Deleting an existing integration | payments/custom-provider.write | 2021-07-28 | locationId* |  |
| GET | `/payments/custom-provider/connect` | Fetch given provider config | payments/custom-provider.readonly | 2021-07-28 | locationId* |  |
| POST | `/payments/custom-provider/connect` | Create new provider config | payments/custom-provider.write | 2021-07-28 | locationId* | live*, test* |
| POST | `/payments/custom-provider/disconnect` | Disconnect existing provider config | payments/custom-provider.write | 2021-07-28 | locationId* | liveMode* |
| PUT | `/payments/custom-provider/capabilities` | Custom-provider marketplace app update capabilities | payments/custom-provider.write | 2021-07-28 |  | supportsSubscriptionSchedules*, companyId, locationId |

### Phone System API (`apps/phone-system.json`, 4 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/phone-system/number-pools` | List Number Pools | numberpools.read | 2021-07-28 | locationId |  |
| GET | `/phone-system/numbers/location/{locationId}/available` | List available phone numbers | phonenumbers.read | 2021-07-28 | locationId*, countryCode*, numberTypes, firstPart, lastPart, anywhere, smsEnabled, mmsEnabled, voiceEnabled |  |
| POST | `/phone-system/numbers/location/{locationId}/purchase` | Purchase a phone number | phonenumbers.write | 2021-07-28 | locationId* | phoneNumber*, countryCode, numberType, addressSid, bundleSid, locality, region, fingerprintId, skipLocationKYC |
| GET | `/phone-system/numbers/location/{locationId}` | List active numbers | phonenumbers.read | 2021-07-28 | locationId*, pageSize, page, searchFilter, skipNumberPool |  |

### Products API (`apps/products.json`, 27 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/products/bulk-update` | Bulk Update Products | products.write | 2021-07-28 |  | altId*, altType*, type*, productIds*, filters, price, compareAtPrice, availability, collectionIds, currency |
| POST | `/products/bulk-update/edit` | Bulk Edit Products and Prices | — | 2021-07-28 |  | altId*, altType*, products* |
| POST | `/products/{productId}/price` | Create Price for a Product | products/prices.write | 2021-07-28 | productId* | name*, type*, currency*, amount*, recurring, description, membershipOffers, trialPeriod, totalCycles, setupFee, variantOptionIds, compareAtPrice, locationId*, userId … |
| GET | `/products/{productId}/price` | List Prices for a Product | products/prices.readonly | 2021-07-28 | productId*, limit, offset, locationId*, ids |  |
| GET | `/products/inventory` | List Inventory | products/prices.readonly | 2021-07-28 | limit, offset, altId*, altType*, search |  |
| POST | `/products/inventory` | Update Inventory | products/prices.write | 2021-07-28 |  | altId*, altType*, items* |
| GET | `/products/{productId}/price/{priceId}` | Get Price by ID for a Product | products/prices.readonly | 2021-07-28 | productId*, priceId*, locationId* |  |
| PUT | `/products/{productId}/price/{priceId}` | Update Price by ID for a Product | products/prices.write | 2021-07-28 | productId*, priceId* | name*, type*, currency*, amount*, recurring, description, membershipOffers, trialPeriod, totalCycles, setupFee, variantOptionIds, compareAtPrice, locationId*, userId … |
| DELETE | `/products/{productId}/price/{priceId}` | Delete Price by ID for a Product | products/prices.write | 2021-07-28 | productId*, priceId*, locationId* |  |
| GET | `/products/store/{storeId}/stats` | Fetch Product Store Stats | products.readonly | 2021-07-28 | storeId*, altId*, altType*, search, collectionIds |  |
| POST | `/products/store/{storeId}` | Action to include/exclude the product in store | products.write | 2021-07-28 | storeId* | altId*, altType*, action*, productIds* |
| POST | `/products/store/{storeId}/priority` | Update product display priorities in store | — | 2021-07-28 | storeId* | altId*, altType*, products* |
| GET | `/products/collections` | Fetch Product Collections | products/collection.readonly | 2021-07-28 | limit, offset, altId*, altType*, collectionIds, name |  |
| POST | `/products/collections` | Create Product Collection | products/collection.write | 2021-07-28 |  | altId*, altType*, collectionId, name*, slug*, image, seo |
| GET | `/products/collections/{collectionId}` | Get Details about individual product collection | products/collection.readonly | 2021-07-28 | collectionId*, altId* |  |
| PUT | `/products/collections/{collectionId}` | Update Product Collection | products/collection.write | 2021-07-28 | collectionId* | altId*, altType*, name, slug, image, seo |
| DELETE | `/products/collections/{collectionId}` | Delete Product Collection | products/collection.write | 2021-07-28 | collectionId*, altId*, altType* |  |
| GET | `/products/reviews` | Fetch Product Reviews | products.readonly | 2021-07-28 | altId*, altType*, limit, offset, sortField, sortOrder, rating, startDate, endDate, productId, storeId |  |
| GET | `/products/reviews/count` | Fetch Review Count as per status | products.readonly | 2021-07-28 | altId*, altType*, rating, startDate, endDate, productId, storeId |  |
| PUT | `/products/reviews/{reviewId}` | Update Product Reviews | products.write | 2021-07-28 | reviewId* | altId*, altType*, productId*, status*, reply, rating, headline, detail |
| DELETE | `/products/reviews/{reviewId}` | Delete Product Review | products.write | 2021-07-28 | reviewId*, altId*, altType*, productId* |  |
| POST | `/products/reviews/bulk-update` | Update Product Reviews | products.write | 2021-07-28 |  | altId*, altType*, reviews*, status* |
| GET | `/products/{productId}` | Get Product by ID | products.readonly | 2021-07-28 | productId*, locationId*, sendWishlistStatus |  |
| DELETE | `/products/{productId}` | Delete Product by ID | products.write | 2021-07-28 | productId*, locationId*, sendWishlistStatus |  |
| PUT | `/products/{productId}` | Update Product by ID | products.write | 2021-07-28 | productId* | name*, locationId*, description, productType*, image, statementDescriptor, availableInStore, medias, variants, collectionIds, isTaxesEnabled, taxes, automaticTaxCategoryId, isLabelEnabled … |
| POST | `/products/` | Create Product | products.write | 2021-07-28 |  | name*, locationId*, description, productType*, image, statementDescriptor, availableInStore, medias, variants, collectionIds, isTaxesEnabled, taxes, automaticTaxCategoryId, isLabelEnabled … |
| GET | `/products/` | List Products | products.readonly | 2021-07-28 | limit, offset, locationId*, search, collectionIds, collectionSlug, expand, productIds, storeId, includedInStore, availableInStore, sortOrder |  |

### Documents and Contracts API (`apps/proposals.json`, 4 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/proposals/document` | List documents | — | 2021-07-28 | locationId*, status, paymentStatus, limit, skip, query, dateFrom, dateTo |  |
| POST | `/proposals/document/send` | Send document | — | 2021-07-28 |  | locationId*, documentId*, documentName, medium, ccRecipients, notificationSettings, sentBy* |
| GET | `/proposals/templates` | List templates | — | 2021-07-28 | locationId*, dateFrom, dateTo, type, name, isPublicDocument, userId, limit, skip |  |
| POST | `/proposals/templates/send` | Send template | — | 2021-07-28 |  | templateId*, userId*, sendDocument, locationId*, contactId*, opportunityId |

### SaaS API (`apps/saas-api.json`, 22 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/saas-api/public-api/locations` | Get locations by stripeId with companyId | — | 2021-04-15 | customerId, subscriptionId, companyId* |  |
| PUT | `/saas-api/public-api/update-saas-subscription/{locationId}` | Update SaaS subscription | — | 2021-04-15 | locationId* | subscriptionId*, customerId*, companyId* |
| POST | `/saas-api/public-api/bulk-disable-saas/{companyId}` | Disable SaaS for locations | — | 2021-04-15 | companyId* | locationIds* |
| POST | `/saas-api/public-api/enable-saas/{locationId}` | Enable SaaS for Sub-Account (Formerly Location) | — | 2021-04-15 | locationId* | stripeAccountId, name, email, stripeCustomerId, companyId*, isSaaSV2*, contactId, providerLocationId, description, saasPlanId, priceId |
| POST | `/saas-api/public-api/pause/{locationId}` | Pause location | — | 2021-04-15 | locationId* | paused*, companyId* |
| POST | `/saas-api/public-api/update-rebilling/{companyId}` | Update Rebilling | — | 2021-04-15 | companyId* | product*, locationIds*, config* |
| GET | `/saas-api/public-api/agency-plans/{companyId}` | Get Agency Plans | — | 2021-04-15 | companyId* |  |
| GET | `/saas-api/public-api/get-saas-subscription/{locationId}` | Get Location Subscription Details | — | 2021-04-15 | locationId*, companyId* |  |
| POST | `/saas-api/public-api/bulk-enable-saas/{companyId}` | Bulk Enable SaaS | — | 2021-04-15 | companyId* | locationIds*, isSaaSV2*, actionPayload* |
| GET | `/saas-api/public-api/saas-locations/{companyId}` | Get SaaS Locations | — | 2021-04-15 | companyId*, page |  |
| GET | `/saas-api/public-api/saas-plan/{planId}` | Get SaaS Plan | — | 2021-04-15 | planId*, companyId* |  |
| GET | `/saas/locations` | Get locations by stripeId with companyId | — | 2021-04-15 | customerId*, subscriptionId*, companyId* |  |
| PUT | `/saas/update-saas-subscription/{locationId}` | Update SaaS subscription | — | 2021-04-15 | locationId* | subscriptionId*, customerId*, companyId* |
| POST | `/saas/bulk-disable-saas/{companyId}` | Disable SaaS for locations | — | 2021-04-15 | companyId* | locationIds* |
| POST | `/saas/enable-saas/{locationId}` | Enable SaaS for Sub-Account (Formerly Location) | — | 2021-04-15 | locationId* | stripeAccountId, name, email, stripeCustomerId, companyId*, isSaaSV2*, contactId, providerLocationId, description, saasPlanId, priceId |
| POST | `/saas/pause/{locationId}` | Pause location | — | 2021-04-15 | locationId* | paused*, companyId* |
| POST | `/saas/update-rebilling/{companyId}` | Update Rebilling | — | 2021-04-15 | companyId* | product*, locationIds*, config* |
| GET | `/saas/agency-plans/{companyId}` | Get Agency Plans | — | 2021-04-15 | companyId* |  |
| GET | `/saas/get-saas-subscription/{locationId}` | Get Location Subscription Details | — | 2021-04-15 | locationId*, companyId* |  |
| POST | `/saas/bulk-enable-saas/{companyId}` | Bulk Enable SaaS | — | 2021-04-15 | companyId* | locationIds*, isSaaSV2*, actionPayload* |
| GET | `/saas/saas-locations/{companyId}` | Get SaaS Locations | — | 2021-04-15 | companyId*, page* |  |
| GET | `/saas/saas-plan/{planId}` | Get SaaS Plan | — | 2021-04-15 | planId*, companyId* |  |

### Snapshots API (`apps/snapshots.json`, 4 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/snapshots/` | Get Snapshots | — | 2021-07-28 | companyId* |  |
| POST | `/snapshots/share/link` | Create Snapshot Share Link | — | 2021-07-28 | companyId* | snapshot_id*, share_type*, relationship_number, share_location_id |
| GET | `/snapshots/snapshot-status/{snapshotId}` | Get Snapshot Push between Dates | — | 2021-07-28 | snapshotId*, companyId*, from*, to*, lastDoc*, limit* |  |
| GET | `/snapshots/snapshot-status/{snapshotId}/location/{locationId}` | Get Last Snapshot Push | — | 2021-07-28 | companyId*, snapshotId*, locationId* |  |

### Social Media Posting API (`apps/social-media-posting.json`, 40 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/social-media-posting/oauth/google/start` | Starts OAuth For Google Account | socialplanner/oauth.readonly | 2021-07-28 | locationId*, userId*, page, reconnect |  |
| GET | `/social-media-posting/oauth/{locationId}/google/locations/{accountId}` | Get google business locations | — | 2021-07-28 | locationId*, accountId* |  |
| POST | `/social-media-posting/oauth/{locationId}/google/locations/{accountId}` | Set google business locations | — | 2021-07-28 | locationId*, accountId* | location, account, companyId |
| POST | `/social-media-posting/{locationId}/posts/list` | Get posts | socialplanner/post.readonly | 2021-07-28 | locationId* | type, accounts, skip*, limit*, fromDate*, toDate*, includeUsers*, postType |
| POST | `/social-media-posting/{locationId}/posts` | Create post | socialplanner/post.write | 2021-07-28 | locationId* | accountIds*, summary, media, status, scheduleDate, createdBy, followUpComment, ogTagsDetails, type*, postApprovalDetails, scheduleTimeUpdated, tags, categoryId, tiktokPostDetails … |
| GET | `/social-media-posting/{locationId}/posts/{id}` | Get post | — | 2021-07-28 | locationId*, id* |  |
| PUT | `/social-media-posting/{locationId}/posts/{id}` | Edit post | — | 2021-07-28 | locationId*, id* | accountIds, summary, media, status, scheduleDate, createdBy, followUpComment, ogTagsDetails, type*, postApprovalDetails, scheduleTimeUpdated, tags, categoryId, tiktokPostDetails … |
| DELETE | `/social-media-posting/{locationId}/posts/{id}` | Delete Post | — | 2021-07-28 | locationId*, id* |  |
| POST | `/social-media-posting/{locationId}/posts/bulk-delete` | Bulk Delete Social Planner Posts | — | 2021-07-28 |  | postIds |
| GET | `/social-media-posting/{locationId}/accounts` | Get Accounts | socialplanner/account.readonly | 2021-07-28 | locationId* |  |
| DELETE | `/social-media-posting/{locationId}/accounts/{id}` | Delete Account | — | 2021-07-28 | locationId*, id*, companyId, userId |  |
| GET | `/social-media-posting/oauth/facebook/start` | Starts OAuth For Facebook Account | — | 2021-07-28 | locationId*, userId*, page, reconnect |  |
| GET | `/social-media-posting/oauth/{locationId}/facebook/accounts/{accountId}` | Get facebook pages | — | 2021-07-28 | locationId*, accountId* |  |
| POST | `/social-media-posting/oauth/{locationId}/facebook/accounts/{accountId}` | Attach facebook pages | — | 2021-07-28 | locationId*, accountId* | type, originId, name, avatar, companyId |
| GET | `/social-media-posting/oauth/instagram/start` | Starts OAuth For Instagram Account | socialplanner/oauth.readonly | 2021-07-28 | locationId*, userId*, page, reconnect |  |
| GET | `/social-media-posting/oauth/{locationId}/instagram/accounts/{accountId}` | Get Instagram Professional Accounts | — | 2021-07-28 | locationId*, accountId* |  |
| POST | `/social-media-posting/oauth/{locationId}/instagram/accounts/{accountId}` | Attach Instagram Professional Accounts | — | 2021-07-28 | locationId*, accountId* | originId, name, avatar, pageId*, companyId |
| GET | `/social-media-posting/oauth/linkedin/start` | Starts OAuth For LinkedIn Account | — | 2021-07-28 | locationId*, userId*, page, reconnect |  |
| GET | `/social-media-posting/oauth/{locationId}/linkedin/accounts/{accountId}` | Get Linkedin pages and profile | — | 2021-07-28 | locationId*, accountId* |  |
| POST | `/social-media-posting/oauth/{locationId}/linkedin/accounts/{accountId}` | Attach linkedin pages and profile | — | 2021-07-28 | locationId*, accountId* | type, originId, name, avatar, urn, companyId |
| GET | `/social-media-posting/oauth/twitter/start` | Starts OAuth For Twitter Account | socialplanner/oauth.readonly | 2021-07-28 | locationId*, userId*, page, reconnect |  |
| GET | `/social-media-posting/oauth/{locationId}/twitter/accounts/{accountId}` | Get Twitter profile | — | 2021-07-28 | locationId*, accountId* |  |
| POST | `/social-media-posting/oauth/{locationId}/twitter/accounts/{accountId}` | Attach Twitter profile | — | 2021-07-28 | locationId*, accountId* | originId, name, username, avatar, protected, verified, companyId |
| POST | `/social-media-posting/{locationId}/csv` | Upload CSV | socialplanner/csv.write | 2021-07-28 | locationId* |  |
| GET | `/social-media-posting/{locationId}/csv` | Get Upload Status | — | 2021-07-28 | locationId*, skip, limit, includeUsers, userId |  |
| POST | `/social-media-posting/{locationId}/set-accounts` | Set Accounts | socialplanner/csv.write | 2021-07-28 | locationId* | accountIds*, filePath*, rowsCount*, fileName*, approver, userId |
| GET | `/social-media-posting/{locationId}/csv/{id}` | Get CSV Post | — | 2021-07-28 | locationId*, id*, skip, limit |  |
| PATCH | `/social-media-posting/{locationId}/csv/{id}` | Start CSV Finalize | — | 2021-07-28 | locationId*, id* | userId |
| DELETE | `/social-media-posting/{locationId}/csv/{id}` | Delete CSV | — | 2021-07-28 | locationId*, id* |  |
| DELETE | `/social-media-posting/{locationId}/csv/{csvId}/post/{postId}` | Delete CSV Post | — | 2021-07-28 | locationId*, postId*, csvId* |  |
| GET | `/social-media-posting/oauth/tiktok/start` | Starts OAuth For Tiktok Account | socialplanner/oauth.readonly | 2021-07-28 | locationId*, userId*, page, reconnect |  |
| GET | `/social-media-posting/oauth/{locationId}/tiktok/accounts/{accountId}` | Get Tiktok profile | — | 2021-07-28 | locationId*, accountId* |  |
| POST | `/social-media-posting/oauth/{locationId}/tiktok/accounts/{accountId}` | Attach Tiktok profile | — | 2021-07-28 | locationId*, accountId* | type, originId, name, avatar, verified, username, companyId |
| GET | `/social-media-posting/oauth/tiktok-business/start` | Starts OAuth For Tiktok Business Account | socialplanner/oauth.readonly | 2021-07-28 | locationId*, userId*, page, reconnect |  |
| GET | `/social-media-posting/oauth/{locationId}/tiktok-business/accounts/{accountId}` | Get Tiktok Business profile | — | 2021-07-28 | locationId*, accountId* |  |
| GET | `/social-media-posting/{locationId}/categories` | Get categories by location id | socialplanner/category.readonly | 2021-07-28 | locationId*, searchText, limit, skip |  |
| GET | `/social-media-posting/{locationId}/categories/{id}` | Get categories by id | — | 2021-07-28 | id*, locationId* |  |
| GET | `/social-media-posting/{locationId}/tags` | Get tags by location id | — | 2021-07-28 | locationId*, searchText, limit, skip |  |
| POST | `/social-media-posting/{locationId}/tags/details` | Get tags by ids | — | 2021-07-28 | locationId* | tagIds* |
| POST | `/social-media-posting/statistics` | Get Social Media Statistics | — | 2021-07-28 | locationId* |  |

### Store API (`apps/store.json`, 18 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/store/shipping-zone` | Create Shipping Zone | — | — |  | altId*, altType*, name*, countries* |
| GET | `/store/shipping-zone` | List Shipping Zones | — | — | altId*, altType*, limit, offset, withShippingRate |  |
| GET | `/store/shipping-zone/{shippingZoneId}` | Get Shipping Zone | — | — | shippingZoneId*, altId*, altType*, withShippingRate |  |
| PUT | `/store/shipping-zone/{shippingZoneId}` | Update Shipping Zone | — | — | shippingZoneId* | altId, altType, name, countries |
| DELETE | `/store/shipping-zone/{shippingZoneId}` | Delete shipping zone | — | — | shippingZoneId*, altId*, altType* |  |
| POST | `/store/shipping-zone/shipping-rates` | Get available shipping rates | — | — |  | altId*, altType*, country*, address, amountAvailable, totalOrderAmount*, weightAvailable, totalOrderWeight*, source*, products*, couponCode |
| POST | `/store/shipping-zone/{shippingZoneId}/shipping-rate` | Create Shipping Rate | — | — | shippingZoneId* | altId*, altType*, name*, description, currency*, amount*, conditionType*, minCondition*, maxCondition*, isCarrierRate, shippingCarrierId*, percentageOfRateFee, shippingCarrierServices |
| GET | `/store/shipping-zone/{shippingZoneId}/shipping-rate` | List Shipping Rates | — | — | shippingZoneId*, altId*, altType*, limit, offset |  |
| GET | `/store/shipping-zone/{shippingZoneId}/shipping-rate/{shippingRateId}` | Get Shipping Rate | — | — | shippingZoneId*, shippingRateId*, altId*, altType* |  |
| PUT | `/store/shipping-zone/{shippingZoneId}/shipping-rate/{shippingRateId}` | Update Shipping Rate | — | — | shippingZoneId*, shippingRateId* | altId, altType, name, description, currency, amount, conditionType, minCondition, maxCondition, isCarrierRate, shippingCarrierId, percentageOfRateFee, shippingCarrierServices |
| DELETE | `/store/shipping-zone/{shippingZoneId}/shipping-rate/{shippingRateId}` | Delete shipping rate | — | — | shippingZoneId*, shippingRateId*, altId*, altType* |  |
| POST | `/store/shipping-carrier` | Create Shipping Carrier | — | — |  | altId*, altType*, name*, callbackUrl*, services, allowsMultipleServiceSelection |
| GET | `/store/shipping-carrier` | List Shipping Carriers | — | — | altId*, altType* |  |
| GET | `/store/shipping-carrier/{shippingCarrierId}` | Get Shipping Carrier | — | — | shippingCarrierId*, altId*, altType* |  |
| PUT | `/store/shipping-carrier/{shippingCarrierId}` | Update Shipping Carrier | — | — | shippingCarrierId* | altId, altType, name, callbackUrl, services, allowsMultipleServiceSelection |
| DELETE | `/store/shipping-carrier/{shippingCarrierId}` | Delete shipping carrier | — | — | shippingCarrierId*, altId*, altType* |  |
| POST | `/store/store-setting` | Create/Update Store Settings | — | — |  | altId*, altType*, shippingOrigin*, storeOrderNotification, storeOrderFulfillmentNotification |
| GET | `/store/store-setting` | Get Store Settings | — | — | altId*, altType* |  |

### Surveys API (`apps/surveys.json`, 2 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/surveys/submissions` | Get Surveys Submissions | surveys.readonly | 2021-07-28 | locationId*, page, limit, surveyId, q, startAt, endAt |  |
| GET | `/surveys/` | Get Surveys | surveys.readonly | 2021-07-28 | locationId*, skip, limit, type |  |

### Users API (`apps/users.json`, 7 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/users/search` | Search Users | users.readonly | 2021-07-28 | companyId*, query, skip, limit, locationId, type, role, ids, sort, sortDirection, enabled2waySync |  |
| POST | `/users/search/filter-by-email` | Filter Users by Email | users.readonly | 2021-07-28 |  | companyId*, emails*, deleted, skip, limit, projection |
| GET | `/users/{userId}` | Get User | users.readonly | 2021-07-28 | userId* |  |
| PUT | `/users/{userId}` | Update User | users.write | 2021-07-28 |  | firstName, lastName, email, password, phone, type, role, companyId, locationIds, permissions, scopes, scopesAssignedToOnly, profilePhoto, twilioPhone … |
| DELETE | `/users/{userId}` | Delete User | users.write | 2021-07-28 |  |  |
| GET | `/users/` | Get User by Location | users.readonly | 2021-07-28 | locationId* |  |
| POST | `/users/` | Create User | users.write | 2021-07-28 |  | companyId*, firstName*, lastName*, email*, password*, phone, type*, role*, locationIds*, permissions, scopes, scopesAssignedToOnly, profilePhoto, twilioPhone … |

### Voice AI API (`apps/voice-ai.json`, 11 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| POST | `/voice-ai/agents` | Create Agent | voice-ai-agents.write | 2021-04-15 |  | locationId*, agentName, businessName, welcomeMessage, agentPrompt, voiceId, language, patienceLevel, maxCallDuration, sendUserIdleReminders, reminderAfterIdleTimeSeconds, inboundNumber, numberPoolId, callEndWorkflowIds … |
| GET | `/voice-ai/agents` | List Agents | voice-ai-agents.readonly | 2021-04-15 | page, pageSize, locationId*, query |  |
| PATCH | `/voice-ai/agents/{agentId}` | Patch Agent | voice-ai-agents.write | 2021-04-15 | agentId*, locationId* | agentName, businessName, welcomeMessage, agentPrompt, voiceId, language, patienceLevel, maxCallDuration, sendUserIdleReminders, reminderAfterIdleTimeSeconds, inboundNumber, numberPoolId, callEndWorkflowIds, sendPostCallNotificationTo … |
| GET | `/voice-ai/agents/{agentId}` | Get Agent | voice-ai-agents.readonly | 2021-04-15 | agentId*, locationId* |  |
| DELETE | `/voice-ai/agents/{agentId}` | Delete Agent | voice-ai-agents.write | 2021-04-15 | agentId*, locationId* |  |
| GET | `/voice-ai/dashboard/call-logs` | List Call Logs | voice-ai-dashboard.readonly | 2021-04-15 | locationId*, agentId, contactId, callType, startDate, endDate, actionType, sortBy, sort, page, pageSize |  |
| GET | `/voice-ai/dashboard/call-logs/{callId}` | Get Call Log | voice-ai-dashboard.readonly | 2021-04-15 | callId*, locationId* |  |
| POST | `/voice-ai/actions` | Create Agent Action | voice-ai-agent-goals.write | 2021-04-15 |  | agentId*, locationId*, actionType*, name*, actionParameters* |
| PUT | `/voice-ai/actions/{actionId}` | Update Agent Action | voice-ai-agent-goals.write | 2021-04-15 | actionId* | agentId*, locationId*, actionType*, name*, actionParameters* |
| GET | `/voice-ai/actions/{actionId}` | Get Agent Action | voice-ai-agent-goals.readonly | 2021-04-15 | actionId*, locationId* |  |
| DELETE | `/voice-ai/actions/{actionId}` | Delete Agent Action | voice-ai-agent-goals.write | 2021-04-15 | actionId*, locationId*, agentId* |  |

### workflows API (`apps/workflows.json`, 1 endpoints)

| Method | Path | What it does | Scope | Version | Params (*=required) | Body fields (*=required) |
|---|---|---|---|---|---|---|
| GET | `/workflows/` | Get Workflow | workflows.readonly | 2021-07-28 | locationId* |  |

### Webhook events (`docs/webhook events/`)

`AppInstall`, `AppUninstall`, `AppointmentCreate`, `AppointmentDelete`, `AppointmentUpdate`, `AssociationCreate`, `AssociationDelete`, `AssociationUpdate`, `CampaignStatusUpdate`, `ContactCreate`, `ContactDelete`, `ContactDndUpdate`, `ContactTagUpdate`, `ContactUpdate`, `ConversationUnreadWebhook`, `InboundMessage`, `InvoiceCreate`, `InvoiceDelete`, `InvoicePaid`, `InvoicePartiallyPaid`, `InvoiceSent`, `InvoiceUpdate`, `InvoiceVoid`, `LCEmailStats`, `LocationCreate`, `LocationUpdate`, `NoteCreate`, `NoteDelete`, `NoteUpdate`, `ObjectSchemaCreate`, `ObjectSchemaUpdate`, `OpportunityAssignedToUpdate`, `OpportunityCreate`, `OpportunityDelete`, `OpportunityMonetaryValueUpdate`, `OpportunityStageUpdate`, `OpportunityStatusUpdate`, `OpportunityUpdate`, `OrderCreate`, `OrderStatusUpdate`, `OutboundMessage`, `PlanChange`, `PriceCreate`, `PriceDelete`, `PriceUpdate`, `ProductCreate`, `ProductDelete`, `ProductUpdate`, `ProviderOutboundMessage`, `RecordCreate`, `RecordDelete`, `RecordUpdate`, `RelationCreate`, `RelationDelete`, `TaskComplete`, `TaskCreate`, `TaskDelete`, `UserCreate`

<!-- CATALOG:END -->
