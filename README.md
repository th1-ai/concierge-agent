# Concierge Agent

A Claude Code sub-agent for hotel operators. It manages concierge services for guests — restaurant bookings, tours, transfers, activities, local recommendations — using *only* the providers you've personally vetted, and tracking everything in a single tracker so nothing falls through the cracks.

Built on the **WAT framework** (Workflows, Agents, Tools): probabilistic AI handles reasoning, deterministic scripts handle execution.

---

## What it does

- **Reads only your vetted providers** — never invents restaurants, beaches, or chefs. If your reference file doesn't have a fit, it flags you instead of guessing.
- **Routes guest emails vs supplier emails on separate inboxes** — the agent will refuse to send a guest-facing message from the supplier inbox, and vice versa
- **Drafts every outbound email for your approval** — never auto-sends to guests or providers
- **Pushes guest preferences to the PMS** — bedding, dietary, mobility, occasion, kids, pets — appended as reservation notes so check-in staff see them
- **Tracks every service end-to-end** — Requested, Pending Deposit, Confirmed, Cancelled — in a single sheet you control
- **Sanity-checks the booking date before drafting** — pre-arrival, in-house, or post-stay framing, never a generic pre-arrival email to someone who's already left

---

## What you need

- [Claude Code](https://claude.ai/code) installed
- Two or more email accounts you can read and draft from programmatically (one guest-facing, one supplier-facing — Gmail via the Google Workspace CLI is the reference setup)
- A PMS with API access for reservation lookup and notes (the reference setup is Cloudbeds, but any PMS with `lookup` + `append-note` endpoints works)
- A tracker (Google Sheet, Airtable, Notion — anything with two tabs)

---

## Quick start

1. **Clone the repo** into a Claude Code project:

   ```bash
   git clone https://github.com/th1-ai/concierge-agent.git
   cd concierge-agent
   ```

2. **Copy the env template** and fill it in:

   ```bash
   cp .env.example .env
   ```

3. **Edit [`.claude/agents/concierge.md`](.claude/agents/concierge.md)** and [`.claude/skills/concierge/SKILL.md`](.claude/skills/concierge/SKILL.md) — replace the placeholders described in [Customising](#customising) with the wrappers your setup uses.

4. **Build your vetted-providers list** in [`references/recommendations-template.md`](references/recommendations-template.md). The file ships empty on purpose — it's the single source of truth for everything the agent will recommend, so it has to come from your own visits and calls. Rename or split it as it grows.

5. **Open in Claude Code** from the project root:

   ```bash
   claude
   ```

6. **Invoke the agent**:

   > "A guest just emailed asking for restaurant suggestions for two adults, no dietary restrictions, lunch on Friday. Draft a reply."

   Claude Code will pick up the `concierge` sub-agent automatically because of the front-matter `description` line.

---

## File structure

```
concierge-agent/
├── README.md                                        # This file
├── .env.example                                     # Inboxes, PMS auth, tracker ID
├── .gitignore
├── LICENSE
├── references/
│   └── recommendations-template.md                  # Empty template for YOUR vetted providers
└── .claude/
    ├── agents/
    │   └── concierge.md                             # The sub-agent definition
    ├── skills/
    │   └── concierge/
    │       └── SKILL.md                             # Booking flows, tracker structure, rules
    └── agent-memory/
        └── concierge/
            └── example-feedback-pattern.md          # Example "memory note" — replace with your own
```

---

## Customising

The agent and skill files use placeholders so they can be adapted to any property + PMS + email stack. Replace the following before first run:

| Placeholder | What to put | Example |
|---|---|---|
| `{{HOTEL_NAME}}` | Your property name | `The Olive Tree Inn` |
| `{{HOTEL_LOCATION}}` | Town / village (only if you want it baked into the prompt) | `<your town>` |
| `{{OPERATOR_NAME}}` | Operator's first name (used in some draft templates) | `<your name>` |
| `{{INBOX_GUEST_HOTEL}}` | Guest-facing inbox for hotel-room guests | `stays@yourhotel.com` |
| `{{INBOX_GUEST_RENTAL}}` | Guest-facing inbox for whole-property renters | `rental@yourhotel.com` |
| `{{INBOX_PROVIDERS}}` | B2B inbox for restaurants, drivers, chefs, vendors | `suppliers@yourhotel.com` |
| `{{EMAIL_CLI}}` | Command-line wrapper to your email provider | `gws gmail` |
| `{{PMS_LOOKUP_TOOL}}` | Script that looks up reservations | `tools/lookup_guest.py` |
| `{{PMS_NOTES_TOOL}}` | Script that appends a note to a reservation | `tools/cloudbeds_notes.py` |
| `{{SHEET_ID_CONCIERGE}}` | Tracker sheet / database ID | `<your sheet id>` |

You can do this with any text editor or with one `sed` pass over the two files:

```bash
for f in .claude/agents/concierge.md .claude/skills/concierge/SKILL.md; do
  sed -i '' \
    -e 's|{{HOTEL_NAME}}|The Olive Tree Inn|g' \
    -e 's|{{OPERATOR_NAME}}|<your name>|g' \
    -e 's|{{INBOX_GUEST_HOTEL}}|stays@yourhotel.com|g' \
    -e 's|{{INBOX_GUEST_RENTAL}}|rental@yourhotel.com|g' \
    -e 's|{{INBOX_PROVIDERS}}|suppliers@yourhotel.com|g' \
    -e 's|{{EMAIL_CLI}}|gws gmail|g' \
    -e 's|{{PMS_LOOKUP_TOOL}}|tools/lookup_guest.py|g' \
    -e 's|{{PMS_NOTES_TOOL}}|tools/cloudbeds_notes.py|g' \
    "$f"
done
```

---

## Building your vetted-providers list

This is the most important step, and the one only you can do.

The agent is explicitly instructed to **never invent** a recommendation. It will only suggest places that appear in [`references/recommendations-template.md`](references/recommendations-template.md). That file ships **empty on purpose** — the value of the concierge agent comes from your curation, not from a generic list scraped from the web.

Suggested approach:

1. Start with the 5–10 providers you already trust (restaurants, drivers, a chef, a beach club).
2. Add each entry with: name, location, why you recommend it, contact details, any caveats.
3. Maintain a "Do Not Recommend" section at the bottom — places you've personally ruled out. The agent will never suggest anything on that list.
4. Append to the call log every time you call or visit a provider. Date stamp every entry.
5. Split the file (e.g. into `restaurant-recommendations.md`, `beach-recommendations.md`, `chef-contacts.md`) once it gets long. Update the agent and skill to point at the new filenames.

---

## How memory works

The agent uses Claude Code's per-agent memory at `.claude/agent-memory/concierge/`. After each session, it saves:

- **Project notes** — active guests, open items, pending services
- **Feedback** — patterns to repeat or avoid (e.g. "always pull guest mobile from the PMS — don't ask the guest")
- **Pricing confirmed with providers** — so the next quote uses fresh numbers

[`example-feedback-pattern.md`](.claude/agent-memory/concierge/example-feedback-pattern.md) shows the recommended format. Delete it once you have your own.

> **Heads-up on committing memory files:** project memory often contains real guest names, dates, and contact details. The included `.gitignore` keeps `.env` out of git, but does not exclude `.claude/agent-memory/`. If you want to keep memory private, add `.claude/agent-memory/` (or just `.claude/agent-memory/concierge/project_*.md`) to your local `.gitignore`.

---

## Related agents

This agent works well alongside:

- [`pre-arrival-outreach-agent`](https://github.com/th1-ai/pre-arrival-outreach-agent) — proactively reaches out to upcoming bookings and hands the conversation to concierge once a guest engages
- [`booking-inquiry-agent`](https://github.com/th1-ai/booking-inquiry-agent) — drafts the warm reply that converts an inquiry into a booking, before concierge picks up
- [`email-triage-agent`](https://github.com/th1-ai/email-triage-agent) — flags incoming guest emails that mention dining / activities so concierge gets invoked promptly
- [`web-research-agent`](https://github.com/th1-ai/web-research-agent) — useful when you're vetting a new candidate provider before adding them to your list

---

## License

MIT — see [LICENSE](LICENSE).
