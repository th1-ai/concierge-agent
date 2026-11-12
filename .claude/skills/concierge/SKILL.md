---
name: concierge
description: Procedures for hotel concierge work - booking-date check, guest vs provider inbox routing, duplicate-proof email search, tracker layout, and the flows for organising restaurants, tours, transfers and activities from the operator's vetted provider list. Use when a guest asks about dining, dietary needs, day trips, things to do, routes, transfers or local tips, when a provider replies about a guest booking, or when the operator asks to add a guest to the concierge tracker or check concierge status.
---

# Skill: Concierge Service

These procedures apply to every concierge task, whether the `concierge` sub-agent runs it or the main session does.

Three rules sit above everything here:

- **Draft, never send.** Every email to a guest or provider is a draft for the operator to approve.
- **Vetted providers only.** Recommend only what is in `references/recommendations-template.md`. If nothing fits, tell the operator; never invent a place, a price or availability.
- **PMS writes are append-only notes.** Anything else on a reservation needs the operator's approval.

## 1. Booking-date check (before any draft)

A reply that ignores where the guest is in their stay reads as careless, so check first:

1. Note the sent date of the guest's email.
2. Pull the guest's check-in and check-out from the PMS.
3. Compare with today's date:
   - **Pre-arrival** (today < check-in): planning suggestions are fine.
   - **In-house** (check-in <= today < check-out): acknowledge that they have arrived and offer help only for the time they have left. No generic "let us help plan your stay" content.
   - **Post-stay** (today >= check-out): do not draft. Flag it to the operator, who decides whether a late apology or follow-up is useful.
4. If the email sat for several days and the guest has arrived or left since, flag it before drafting. Give the email date, the check-in and check-out dates, today's date and the framing you propose.

## 2. Inbox routing

| Recipient | Draft from |
|---|---|
| Hotel-room guest | `{{INBOX_GUEST_HOTEL}}` |
| Whole-property renter | `{{INBOX_GUEST_RENTAL}}` |
| Restaurant, driver, chef, tour operator, any vendor | `{{INBOX_PROVIDERS}}` |

Never draft a guest email from the provider inbox, or a provider email from a guest inbox. Guests then reply into a mailbox nobody watches for guest mail.

If an older thread with a guest sits on the wrong account, do not continue it. Start a fresh email from the correct account: the routing rule beats thread continuity.

## 3. Duplicate-proof email search (before any guest draft)

Search every configured inbox two ways:

- **By the email address on the reservation.** This finds threads even when the guest's display name differs.
- **By the guest's full name.** This finds mail sent from a personal address that is not on the booking.

If either search finds mail already sent to this guest on the same subject, do not draft a duplicate. Report what was sent and when, and whether it needs a follow-up.

Then search for provider replies on the guest's open items.

## 4. Commands

The operator supplies the command-line tools. The lines below show the shape this skill expects; the real flags depend on the operator's wrappers. If a command fails, run it with `--help` once and adapt. If the tool is missing, stop and report it.

```bash
# PMS: find a reservation
{{PMS_LOOKUP_TOOL}} --email "guest@example.com"
{{PMS_LOOKUP_TOOL}} --name "LastName"
{{PMS_LOOKUP_TOOL}} --booking-ref "<ota_ref>"

# PMS: append a note to a reservation
{{PMS_NOTES_TOOL}} --reservation-id "<RES_ID>" --note "<text>"

# Email: read a thread, create a draft, create a threaded reply draft
{{EMAIL_CLI}} thread-get --account guest --message-id "<MSG_ID>" --format text
{{EMAIL_CLI}} create-draft --account guest --to "guest@example.com" --subject "<subject>" --body "<html>" --html
{{EMAIL_CLI}} create-reply --account guest --message-id "<MSG_ID>" --body "<html>" --html
```

Use `{{TRACKER_CLI}}` to read and update the tracker (ID `{{SHEET_ID_CONCIERGE}}`) and `{{CALENDAR_CLI}}` to read and write calendar events.

Never use a send command, even if the email tool has one.

## 5. Concierge tracker

One tracker is the record of all concierge work. Any tool with two tabs works.

**Guests tab**

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

**Services tab**

| Column | Description |
|--------|-------------|
| Guest | Guest last name (matches the Guests tab) |
| Service Type | Restaurant, Tour, Transfer, Activity, Other |
| Date | Date of the service |
| Details | Restaurant name, tour route, pickup time, etc. |
| Status | Requested, Pending Deposit, Confirmed, Cancelled |
| Cost | Cost if applicable |
| Notes | Confirmation numbers, provider contact, special instructions |

**Status values**

- **Requested**: the guest has asked; not yet confirmed by the provider.
- **Pending Deposit**: the provider needs a deposit or card guarantee before confirming. This always needs the operator.
- **Confirmed**: the provider has confirmed in writing.
- **Cancelled**: the service is cancelled.

## 6. Flows

### Recommending a restaurant, beach, tour or activity

1. Read the reference file, including "Do Not Recommend" and the call log.
2. Match entries to the guest: dietary needs, occasion, style, party make-up (couple, family, children's ages), mobility, distance and season.
3. Treat every caveat in the file as binding. For example, do not offer a club the file marks as hotel-guests-only.
4. Offer two or three options at most, each with the reason it fits this guest, taken from the file's "Why we recommend" line.
5. Offer to make the booking for them.
6. If nothing fits, or the only fit was last verified long ago, report that instead of stretching a poor match.

### Organising a service

1. Confirm the guest's details and dates from the PMS and the tracker.
2. Pull the guest's name, mobile, party size and dates from the PMS. Never ask the guest for what the PMS already holds. Give the provider the guest's own mobile as the day-of contact, not the property landline, so the provider can reach them directly. If the PMS has no mobile, say so in the report.
3. Draft the request to the provider from `{{INBOX_PROVIDERS}}`. Pass on dietary needs and party make-up.
4. Add the service to the Services tab with status "Requested".
5. When the provider replies, update the status and draft the confirmation to the guest.

### Adding a guest to the tracker

1. The trigger is a whole-property booking, a booking above the operator's value threshold, or the operator asking.
2. Add the guest to the Guests tab.
3. Draft a welcome email offering concierge help, from the correct guest inbox, after the booking-date check and the duplicate search.

### Monitoring open items

- Compare incoming email with tracker statuses to find what changed.
- List any service whose date is within a few days and whose status is still "Requested" or "Pending Deposit".
- List provider requests that have had no reply, with the date they were sent.

### Whole-property concierge form

Whole-property renters get one intake form for all their requests (arrival time, transfers, tours, dining, dietary needs, activities): `{{CONCIERGE_FORM_URL}}`.

- Include the link in the pre-arrival or welcome draft for a whole-property booking.
- If a renter emails requests before completing the form, answer what they asked and include the link.
- Never send it to hotel-room guests, to OTA bookings for single rooms, or to an inquiry that has not yet become a whole-property booking.
- A booking is whole-property when it covers the entire property or the PMS booking source or product marks it as a rental.

## 7. Guest preferences to PMS note

When a guest mentions anything that staff on the day would want to know (bedding, cot or extra bed, dietary needs or allergies, mobility needs, arrival time, transfer needs, an occasion, children and their ages, pets), add it as a note on the reservation, even if no other concierge action follows.

1. Find the reservation with `{{PMS_LOOKUP_TOOL}}`.
2. If the notes tool supports `--dry-run`, run it that way first and check the reservation ID and text.
3. Append the note in this form: `<Type> request (<source> <YYYY-MM-DD>): <detail>.`

This needs no approval because it only adds information and changes nothing about the booking. It applies to notes only.

## 8. After every action, update all four

1. **Tracker**: status and notes columns.
2. **Calendar**: one event per service, with the guest name, phone, stay dates, booking reference, service details, provider contact, cost and status in the description.
3. **PMS reservation notes**: the day-by-day concierge plan with the status of each service.
4. **Memory**: the guest's open items.

A system you could not update goes in the report, so the operator knows which record is stale.

## 9. Keeping the reference file current

The operator owns the reference file. When the operator gives you a new provider, a visit report or a ruling ("stop recommending X"), update the file: name, location, style, why it is recommended, caveats, contact and a dated call-log line. Move ruled-out places to "Do Not Recommend" with the reason and date. Do not add a provider on your own initiative.
