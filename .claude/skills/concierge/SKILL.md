# Skill: Concierge Service

## Trigger

Use proactively when:

- A guest asks about restaurants, tours, transfers, activities, or local recommendations
- A guest mentions dining, dietary restrictions, or food preferences (this IS a concierge task — suggest restaurants)
- A guest asks for driving routes, day-trip ideas, or things to do
- A high-value booking is detected in the PMS (set your own threshold, e.g. above a given booking value)
- An email arrives from or about a guest already on the concierge tracker
- The operator asks to add a guest to the concierge tracker or organise a service
- During morning routine, when guest emails mention any activity / dining / logistics need

**IMPORTANT:** Any guest communication involving local recommendations (restaurants, activities, routes, sightseeing) MUST use this skill. Never draft restaurant or activity suggestions without consulting the vetted reference files first.

## Booking-date sanity check (MANDATORY before drafting)

Before drafting any concierge reply:

1. Note the sent date of the guest's email.
2. Pull the guest's booking (check-in / check-out) from the PMS.
3. Compare with **today's date** and classify the stay phase:
   - **Pre-arrival** (today < check-in): safe to send planning suggestions.
   - **In-house** (check-in <= today < check-out): acknowledge they have already arrived. Only offer help for time they have left. Do NOT send generic pre-arrival "let us help plan your stay" content.
   - **Post-stay** (today >= check-out): do NOT auto-draft. Flag to the operator — most likely you should apologise for the late reply and follow up only if useful.
4. If the email sat for several days and the guest has since arrived or departed, **flag to the operator before drafting** with: email date, check-in/out, today's date, and proposed framing. Ask for approval before sending anything.

## Email account routing (MANDATORY)

When sending **to a guest**, always use a guest-facing inbox:

- `{{INBOX_GUEST_HOTEL}}` — for hotel-room guests
- `{{INBOX_GUEST_RENTAL}}` — for whole-property renters

**Never send guest-facing emails from your supplier inbox.** The supplier inbox (`{{INBOX_PROVIDERS}}`) is B2B only — restaurants, drivers, chefs, tour operators, vendors, accountants.

If a previous thread with the guest happens to be on the wrong account (e.g. older pre-arrival emails sent from the supplier inbox), do NOT continue that thread. Start a fresh email from the correct account. Routing rule beats thread continuity.

When emailing **service providers** on behalf of a guest, use `{{INBOX_PROVIDERS}}` — these are B2B conversations.

## Whole-property concierge form (whole-property rentals only)

If you accept whole-property bookings, host a single typed-fields intake form so renters submit all concierge preferences (arrival time, transfers, tours, dining, dietary, activities) upfront. It is **ONLY** for whole-property renters, never for individual hotel-room guests.

**When to send:**

- Guest books the whole property (rental product, not individual rooms)
- Include the form link in the pre-arrival / welcome email
- If a whole-property renter emails you with concierge requests before completing the form, include the link so they can give you everything in one place

**How to identify a whole-property renter:**

- Booking covers the entire property
- Booking source / product code in the PMS marks it as a whole-property rental
- Project memory tracks active whole-property bookings — check there

**Never send this form to:**

- Individual hotel-room guests
- OTA bookings for individual rooms
- Inquiries that have not yet converted to a whole-property booking

## Concierge Tracker

Use a single source of truth for all concierge work. Reference setup is a Google Sheet (`SHEET_ID_CONCIERGE` in `.env`). Any tracker with two tabs (Guests + Services) works.

### Guests tab

| Column | Description |
|--------|-------------|
| First Name | Guest first name |
| Last Name | Guest last name |
| Email | Guest email address |
| Check-in | Arrival date |
| Check-out | Departure date |
| Booking Value | Total booking value |
| Booking Source | Direct, OTA name, etc. |
| Notes | Special requests, preferences, occasion |

### Services tab

| Column | Description |
|--------|-------------|
| Guest | Guest name (matches Guests tab) |
| Service Type | Restaurant, Tour, Transfer, Activity, Other |
| Date | Date of the service |
| Details | Specifics (restaurant name, tour route, pickup time, etc.) |
| Status | Requested, Confirmed, Pending Deposit, Cancelled |
| Cost | Cost if applicable |
| Notes | Confirmation numbers, contact details, special instructions |

## Service Types

- **Restaurant** -- Booking a table at a local restaurant
- **Tour** -- Guided or self-guided tours and excursions
- **Transfer** -- Airport pickup / drop-off, car service
- **Activity** -- Spa, cooking class, wine tasting, water sports, etc.
- **Other** -- Anything that does not fit the above

## Status Values

- **Requested** -- Guest has asked for this, not yet actioned
- **Confirmed** -- Booked and confirmed with the provider
- **Pending Deposit** -- Provider requires deposit before confirming
- **Cancelled** -- Service cancelled

## Workflow — Check & Update Sequence

When checking concierge status or processing concierge work, ALWAYS follow this order:

### Step 1: Load current state (sources of truth)

1. **Project memory** (`.claude/agent-memory/concierge/`) — read the list of active guests and open items
2. **PMS reservations** — for each active guest, look up the reservation and read the notes (`{{PMS_LOOKUP_TOOL}}`). The notes contain the day-by-day concierge plan with statuses.
3. **Concierge tracker** (Services tab) — read current service statuses

### Step 2: Check for existing threads and updates

4. **Calendar** — check upcoming concierge events for any that need attention
5. **Emails — duplicate-proof search** — before drafting ANY email to a guest, search all configured inboxes using BOTH methods:
   - **Method A (PMS email):** Look up the guest's reservation in the PMS, get the email address on file, and search all inboxes for that email address. This catches threads even if the guest's display name differs.
   - **Method B (Full name):** Search all inboxes for the guest's full name. This catches emails sent from a personal address not linked to the booking.
   - If EITHER search returns existing sent messages or threads with this guest, **do not draft a duplicate**. Instead, note what was already sent and flag any that need a follow-up.
6. **Provider emails** — search for replies from restaurants, tour operators, transfer providers related to open items.

### Step 3: Act on what's changed

7. **Draft replies** — for any emails that need a response, draft them for the operator to review
8. **Update all systems** — after every action, update PMS notes, tracker, calendar, and memory (see Rules below)

### Adding a New Guest

1. Identify a high-value or whole-property booking in the PMS or from email
2. Add to the Guests tab with all details
3. Draft a warm, personal welcome email offering concierge services
4. Show the draft to the operator for approval

### Organising a Service

1. Confirm guest details and dates from the PMS + tracker
2. Contact the service provider (draft email for the operator to review)
3. Add the service to the Services tab with status "Requested"
4. Update all systems as confirmations come in
5. Inform the guest of confirmations (draft for the operator's review)

## Local Recommendations — Reference Files

**CRITICAL: Always consult your reference file(s) before recommending anything to a guest. Never invent or guess recommendations.**

| File | Contents |
|------|----------|
| `references/recommendations-template.md` | Vetted list of restaurants, beaches, chefs, drivers, and other providers — fill in your own |

**Restaurant workflow:**

1. Read your vetted-restaurants file
2. Match restaurants to the guest's needs (dietary restrictions, occasion, style, proximity)
3. Only recommend restaurants from the approved list
4. If no suitable restaurant exists in the list, **tell the operator** rather than inventing one
5. Offer to make the reservation on the guest's behalf — never tell the guest to call themselves

**Beach / activity workflow:**

1. Read your vetted-beaches / vetted-activities file
2. Match to the guest profile — couples vs family, mobility, interests — and read any access caveats (e.g. hotel-guest-only clubs)
3. Only recommend places from the approved list; never invent
4. Offer to call ahead and reserve on the guest's behalf
5. After any new call / visit feedback from the operator, append to the call-log section of the file

**Building the reference files:**

- When the operator adds a new restaurant or activity recommendation, update the relevant reference file
- Include: name, location, style, why you recommend it, any caveats (dietary, price, booking needed)
- Track a "Do Not Recommend" section for places you've ruled out

## Guest preferences -> PMS note (ALWAYS)

Whenever a guest mentions any stay-relevant preference or detail in an email — bedding setup (king vs twin, single bed, cot, extra bed), dietary needs / allergies, mobility needs, arrival time, transfer requirements, occasion (anniversary, birthday), kids / ages, pet info, anything an operator on the day would want to know — **immediately add it as a note to the PMS reservation** so it shows up at check-in. Do this even if no other concierge action is required.

```bash
# 1. Resolve the reservation (OTA confirmation # is in the body)
{{PMS_LOOKUP_TOOL}} --booking-ref <ota_ref>
# 2. Append note (no approval needed for notes — append-only, no risk)
{{PMS_NOTES_TOOL}} --reservation-id <RES_ID> \
  --note "{Type} request ({source} {YYYY-MM-DD}): {detail}." --dry-run
# then re-run without --dry-run
```

Look up the reservation first via `{{PMS_LOOKUP_TOOL}} --booking-ref <ota_ref>` or `--name`. Don't ask the operator for approval to add a note — it's append-only metadata, no risk. (Modifying reservation dates / rooms / charges still requires approval per the main rules.)

## Rules

- **Always check the PMS** for booking details before quoting or organising anything.
- **Pull guest contact details (phone, email, party size, dates) from the PMS before drafting** any email — to a guest, a restaurant, a tour operator, a transfer, anyone. The data is already in the PMS.
  - Never ask the guest for info we already have in the PMS (phone, dates, party size). It looks unprofessional.
  - Never substitute the property landline as the contact when booking restaurants / tours on a guest's behalf — use the guest's mobile from the PMS so the provider can reach them directly.
- **Always draft emails for the operator to review** before sending to guests or service providers.
- **Never modify PMS reservations** without the operator's explicit approval.
- **Log services in the tracker** as soon as they are requested; update status as it changes.
- **After EVERY concierge action** (email sent, response received, status change, booking confirmed), immediately update ALL of:
  1. **Concierge tracker** — status and notes columns
  2. **Project memory** (`.claude/agent-memory/concierge/`)
  3. **Calendar** — create / update events with full details in description: guest name, email, phone, check-in / check-out dates, booking ref, room details, service details, provider contact, cost, status
  4. **PMS reservation notes** — add / update a day-by-day concierge plan on the reservation via `{{PMS_NOTES_TOOL}}`, with status of each service (CONFIRMED, REQUESTED, etc.)
