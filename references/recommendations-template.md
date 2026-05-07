# Vetted Local Recommendations — Template

This file is the **single source of truth** for everything the concierge agent will recommend to guests: restaurants, beaches, chefs, drivers, tour operators, vendors. The agent is instructed to read this file first and **never invent** a recommendation that isn't in here.

> **This template ships empty on purpose.** The whole point of the concierge agent is that *you* curate which providers you trust. Fill in your own list as you visit / call / book each one. A short list of vetted contacts beats a long list of speculative ones.

You can split this single file into multiple files (e.g. `restaurant-recommendations.md`, `beach-recommendations.md`, `chef-contacts.md`) once it gets long. Update the agent and skill to point at the new filenames.

---

## How to use this file

- **Add a provider only after you've personally vetted them** (visited, called, or had a guest report back positively).
- **Always include a "Why we recommend" line** so the agent can pattern-match to guest needs.
- **Maintain a "Do Not Recommend" section** at the bottom — places you've ruled out. The agent will never suggest anything on that list.
- **Append to the call log** at the bottom whenever you call a provider. Date stamp every entry.
- **Treat caveats as binding** (e.g. "hotel-guests-only" beach clubs that won't reserve for non-residents — never offer those).

---

## Restaurants

### `<Restaurant Name>`

- **Location:** `<address or village>`
- **Style:** `<cuisine, e.g. classic regional, modern, casual, fine dining>`
- **Why we recommend:** `<one or two sentences — what makes this special, who it's right for>`
- **Food expectations to set:** `<anything a guest needs to know upfront, e.g. "menu hasn't changed in years — go for the experience, not innovation">`
- **Notes:** `<booking lead time, dress code, view, kid-friendliness, dietary flexibility>`
- **Booking guarantee:** `<does the restaurant require a CC guarantee form for groups? Where's the form template stored?>`
- **Lunch vs dinner — when to recommend which:**
  - **Peak summer:** `<lunch / dinner>` because `<reason — heat, atmosphere, lighting>`
  - **Shoulder months:** `<lunch / dinner>` because `<reason>`
  - **Low season:** `<lunch / dinner>` because `<reason>`
- **Default booking times:** lunch `<HH:MM>`, dinner `<HH:MM>`
- **Required for booking:** full name + phone + party size + time
- **Contact:** `<email or phone, plus name of the contact if you have one>`
- **Last visited / verified:** `YYYY-MM-DD`

### `<Restaurant Name 2>`

- **Location:** `<address or village>`
- **Style:** `<cuisine>`
- **Why we recommend:** `<one or two sentences>`
- **Notes:** `<dietary flexibility, walking vs driving, kid-friendliness>`
- **Contact:** `<email or phone>`
- **Last visited / verified:** `YYYY-MM-DD`

---

## Beaches / beach clubs

> Split into "couples / adults" and "families" if your area has both. Mark each entry with whether it's sandy, has sunbeds, requires a reservation, and any access caveats.

### `<Beach or Club Name>` — Couples / Adults

- **Location:** `<area, drive time from property>`
- **Sandy?** `<yes / no — pebble / mixed>`
- **Vibe:** `<one line — quiet, party, romantic, family-mixed>`
- **Restaurant on site:** `<name, style>`
- **Sunbed price:** `<approx range>`
- **Reservation:** `<yes / no, lead time>`
- **Season:** `<dates open>`
- **Access caveats:** `<e.g. "hotel-guests-only — won't reserve for non-residents", or "boat-only access from <harbour>">`
- **Why we recommend:** `<one or two sentences>`
- **Last verified:** `YYYY-MM-DD`

### `<Beach or Club Name 2>` — Families

- **Location:** `<area, drive time>`
- **Sandy?** `<yes / no>`
- **Vibe:** `<calm, kid-friendly, jellyfish nets, etc.>`
- **Why we recommend:** `<for families because ...>`
- **Reservation:** `<yes / no>`
- **Last verified:** `YYYY-MM-DD`

---

## Private chefs

> Use the same format for every chef. Track cost price (what they charge you) separately from retail price (what you quote the guest, including markup).

### Pricing model

- Cost price = what the chef charges you
- Retail price = cost + your markup (set your own, e.g. a fixed per-person amount)
- Always reconfirm the chef's rate annually — pricing drifts year to year

### `<Chef Name>`

- **Email:** `<chef@example.com>`
- **Status:** `<active repeat collaborator / new contact / one-off>`
- **Cost price:** `<e.g. EUR XX per person for a 3-course dinner — last confirmed YYYY-MM>`
- **Retail to guest:** `<cost + your markup>`
- **Cuisine:** `<style>`
- **Sourcing:** `<local, organic, etc.>`
- **Strength:** `<dietary flexibility, kid-friendly, plating, etc.>`
- **Booking flow:** `<how you typically engage them — see workflow notes below>`
- **Past engagements:** `<short list of guests they've cooked for, dates, outcome>`
- **Booking lead time:** `<weeks of notice they need for peak season>`
- **When to recommend:** `<group size, occasion, dietary mix>`
- **Last verified:** `YYYY-MM-DD`

### Booking workflow

1. Email the chef with guest dates, group size + composition (adults / children with ages), any dietary notes
2. Chef sends availability + menu options + cost
3. You pass numbers to guest with your markup applied
4. Once guest commits, make the introduction (email handover) — guest confirms dates and menu **directly with the chef**, including any specific menu adjustments
5. Track in concierge memory + tracker but stay out of the menu detail

---

## Drivers / transfers / tour operators

### `<Driver or Operator Name>`

- **Service type:** `<airport transfer / day-trip driver / minivan tours>`
- **Email:** `<contact@example.com>`
- **Phone:** `<+XX X XX XX XX XX>`
- **Vehicle:** `<sedan / minivan / bus, capacity>`
- **Pricing:** `<typical day rate or per-route prices>`
- **Languages:** `<which languages the driver speaks>`
- **Notes:** `<reliability, English level, child-seat availability, payment method>`
- **Past engagements:** `<short list of guests, dates, outcome>`
- **Last verified:** `YYYY-MM-DD`

---

## Tours and activities

> Vetted half-day and full-day options that work well from your property. Match to guest interests, fitness, and group size.

### `<Tour Name>`

- **Duration:** `<half-day 4h / full-day 8h>`
- **Route:** `<the actual stops>`
- **Best for:** `<couples / families / culture buffs / nature>`
- **Driver / operator:** `<which driver from above runs it>`
- **Approx cost:** `<van + extras>`
- **Seasonality:** `<year-round / seasonal>`
- **Notes:** `<anything that affects the experience — closures, mid-day heat, picnic option>`

---

## Do Not Recommend

> Append-only. Once you've ruled a place out, never offer it again. Date the entry so future-you remembers why.

| Place | Reason | Date ruled out |
|-------|--------|----------------|
| `<Place A>` | `<closed / poor experience / hotel-guests-only>` | `YYYY-MM-DD` |
| `<Place B>` | `<wrong vibe for our guests>` | `YYYY-MM-DD` |

---

## Notes from the operator (call log)

> Append notes here after calling or visiting. Format: date — provider — note.

- `YYYY-MM-DD` — `<Provider name>` — `<one-line note: what changed, what you confirmed, who you spoke to>`
- `YYYY-MM-DD` — `<Provider name>` — `<note>`
