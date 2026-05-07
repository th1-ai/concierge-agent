---
name: Pull guest contact details from the PMS, never ask the guest
description: When booking restaurants, tours, or transfers on a guest's behalf, use the guest's mobile and email from the PMS — not the property landline, not a fresh request to the guest
type: feedback
---

> **Example pattern.** This file shows the *shape* of a useful agent-memory note. Replace it with your own learnings as the agent runs.

When booking a service on a guest's behalf (restaurant, tour, driver), the provider needs a contact for the day-of: phone number to call if running late, email if the booking changes. The cheapest reliable pattern:

1. **Look up the reservation in the PMS first.** Get: guest full name, mobile, email, party size, dates.
2. **Use the guest's own mobile** as the day-of contact in the booking — not the property landline. Providers (restaurants in particular) call the customer directly when there's an issue, and routing through the property's main line adds a hop that fails on weekends and evenings.
3. **Pass through dietary notes and party composition** (adults / children with ages) to the provider. They can pre-set the table or pre-warn the chef.
4. **Never email the guest to ask for info already in the PMS.** It looks unprofessional and slows the booking. If something is genuinely missing (mobile not on file for an OTA booking), ask once, with context.

**Why:** Providers want a number that reaches the actual customer. The property landline often goes to voicemail and the message reaches the operator hours later — by which point the table has been given away.

**How to apply:** Before drafting any provider email, run a PMS lookup. If the lookup returns a mobile, use it. If it returns only an OTA-relay address, flag to the operator that the booking can be held but the day-of contact will be the property line until the guest provides a direct mobile.

**Anti-pattern to avoid:** Asking the guest "could you confirm your mobile and party size?" when both are already in the PMS. The guest filled this in at booking. Asking again signals you didn't read their record.
