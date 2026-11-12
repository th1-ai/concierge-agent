# Concierge Agent

A Claude Code sub-agent for hotel operators. It handles concierge requests from guests — restaurant bookings, tours, transfers, activities, local recommendations — using *only* the providers you've personally vetted, and it records everything in one tracker so nothing falls through the cracks.

This repo is a template: markdown instructions for Claude Code, with no scripts inside. It follows the **WAT** split (Workflows, Agents, Tools): the agent does the reasoning, and the command-line tools you already have for email, PMS, tracker and calendar do the execution.

---

## What it does

- **Recommends only your vetted providers** — never invents restaurants, beaches, or chefs. If your reference file doesn't have a fit, it tells you instead of guessing.
- **Drafts every outbound email for your approval** — never sends to guests or providers
- **Keeps guest mail and supplier mail on separate inboxes** — guest drafts come from a guest-facing inbox, provider drafts from your supplier inbox
- **Adds guest preferences to the PMS** — bedding, dietary, mobility, occasion, kids, pets — as reservation notes so check-in staff see them. Notes are the only thing it writes to the PMS without asking.
- **Tracks every service end-to-end** — Requested, Pending Deposit, Confirmed, Cancelled — in a tracker you control
- **Checks the booking dates before drafting** — pre-arrival, in-house, or post-stay framing, never a generic pre-arrival email to someone who's already left
- **Ends every run with the same short report** — drafts waiting for you, what it updated, what it needs you to decide, what it could not do

---

## What you need

- [Claude Code](https://code.claude.com/docs/en/overview) installed
- Command-line access to your email, with at least one guest-facing account and one supplier-facing account that can read mail and create drafts (the reference setup is Gmail through a Google Workspace CLI)
- A command-line way to look up a reservation in your PMS and append a note to it (the reference setup is two small scripts against Cloudbeds; any PMS with a lookup and a notes endpoint works)
- A tracker with two tabs (Google Sheet, Airtable, Notion) and a calendar, each reachable from the command line

The agent calls these tools; it does not include them. A tool you do not have is not a blocker: the agent reports what it could not reach and carries on with the rest.

---

## Quick start

1. **Clone the repo** and open Claude Code in it:

   ```bash
   git clone https://github.com/th1-ai/concierge-agent.git
   cd concierge-agent
   claude
   ```

2. **Let Claude Code set it up with you.** Paste this:

   > Read the README and set this agent up with me.

   Claude Code asks you for each value in [Customising](#customising) and writes it into the two files. To do it by hand instead, open [`.claude/agents/concierge.md`](.claude/agents/concierge.md) and [`.claude/skills/concierge/SKILL.md`](.claude/skills/concierge/SKILL.md) and replace each `{{PLACEHOLDER}}`.

3. **Build your vetted-providers list** in [`references/recommendations-template.md`](references/recommendations-template.md). See [below](#building-your-vetted-providers-list). The file ships empty on purpose.

4. **Check that it works** with the steps in [Verify it works](#verify-it-works).

5. **Use it:**

   > A guest just emailed asking for restaurant suggestions for two adults, no dietary restrictions, lunch on Friday. Use the concierge agent to draft a reply.

   Claude Code also hands concierge work to the agent on its own when a request matches the `description` line in the agent file.

If your command-line tools read credentials from a `.env` file, copy [`.env.example`](.env.example) to `.env` and add them. The agent itself reads nothing from `.env`.

---

## File structure

```
concierge-agent/
├── README.md                                        # This file
├── .env.example                                     # Only for credentials your own tools need
├── .gitignore
├── LICENSE
├── references/
│   └── recommendations-template.md                  # Empty template for YOUR vetted providers
└── .claude/
    ├── agents/
    │   └── concierge.md                             # The sub-agent: order of work, hard rules, report format
    ├── skills/
    │   └── concierge/
    │       └── SKILL.md                             # Procedures: date check, inbox routing, tracker, flows
    └── agent-memory/
        └── concierge/
            ├── MEMORY.md                            # Memory index, loaded on every run
            └── example-feedback-pattern.md          # Example memory note — replace with your own
```

The agent file lists the skill under `skills:`, so the skill's full text is loaded whenever the agent starts.

---

## Customising

The agent and skill files use placeholders so they fit any property, PMS and email stack. Replace every one before first use; the agent stops and reports if it finds one unreplaced.

| Placeholder | What to put | Example |
|---|---|---|
| `{{HOTEL_NAME}}` | Your property name | `Your Hotel` |
| `{{HOTEL_LOCATION}}` | Town or area | `<your town>` |
| `{{OPERATOR_NAME}}` | The person who approves drafts | `<your name>` |
| `{{INBOX_GUEST_HOTEL}}` | Guest-facing inbox for hotel-room guests | `stays@example.com` |
| `{{INBOX_GUEST_RENTAL}}` | Guest-facing inbox for whole-property renters | `rental@example.com` |
| `{{INBOX_PROVIDERS}}` | Supplier inbox for restaurants, drivers, chefs, vendors | `suppliers@example.com` |
| `{{EMAIL_CLI}}` | Command that reads mail and creates drafts | `gws gmail` |
| `{{PMS_LOOKUP_TOOL}}` | Command that looks up a reservation | `tools/lookup_guest.py` |
| `{{PMS_NOTES_TOOL}}` | Command that appends a note to a reservation | `tools/add_reservation_note.py` |
| `{{TRACKER_CLI}}` | Command that reads and updates the tracker | `gws sheets` |
| `{{SHEET_ID_CONCIERGE}}` | Tracker sheet or database ID | `<your sheet id>` |
| `{{CALENDAR_CLI}}` | Command that reads and writes calendar events | `gws calendar` |
| `{{CONCIERGE_FORM_URL}}` | Link to your intake form for whole-property renters | `https://example.com/concierge-form` |

Notes:

- **One guest inbox only?** Put the same address in `{{INBOX_GUEST_HOTEL}}` and `{{INBOX_GUEST_RENTAL}}`.
- **No whole-property rentals?** Delete the "Whole-property concierge form" section from the skill instead of filling in `{{CONCIERGE_FORM_URL}}`.
- **No calendar or tracker tool yet?** Write `none` in the placeholder. The agent reports that system under "Could not do" on each run.
- **Command examples.** The skill's "Commands" section shows example flags such as `--email` and `create-draft`. Your tools will differ. Change the examples to the real syntax so the agent does not have to work it out each time.

### Setup instructions for Claude Code

When the operator asks you to set this agent up:

1. Ask for the values in the table above, a few at a time, in plain language. Offer the notes above where they apply.
2. For each command the operator names, check that it exists (run it with `--help`). Do not run anything that sends mail or changes a reservation. If a command is missing, say so and carry on.
3. Replace the placeholders in `.claude/agents/concierge.md` and `.claude/skills/concierge/SKILL.md`. Do not edit this README.
4. Rewrite the command examples in the skill's "Commands" section to match the real syntax you saw in the `--help` output. Keep the rule that no send command is used.
5. Confirm that `grep -rn '{{' .claude/` returns nothing.
6. Do not create or fill a `.env` with secrets yourself. Tell the operator which credentials their tools need and let them add them.
7. Remind the operator that `references/recommendations-template.md` is theirs to fill, and do not add providers to it yourself.

---

## Verify it works

1. **Placeholders are gone.** `grep -rn '{{' .claude/` prints nothing.
2. **Claude Code sees the agent.** Run `/agents` inside Claude Code; `concierge` is in the list.
3. **It refuses to invent.** Before you add any providers, ask:

   > Use the concierge agent: a guest wants a dinner recommendation for tonight.

   The right answer is a report that says there is no vetted provider to recommend. If it names a restaurant, check that the reference file path in the agent file matches your file.
4. **It drafts and does not send.** Add one provider, repeat the request for a test reservation, and check that a draft appears in the guest-facing account and that nothing was sent.

---

## Building your vetted-providers list

This is the most important step, and the one only you can do.

The agent is told to **never invent** a recommendation. It suggests only places that appear in [`references/recommendations-template.md`](references/recommendations-template.md). That file ships **empty on purpose** — the value of the concierge agent comes from your curation, not from a generic list scraped from the web.

Suggested approach:

1. Start with the 5–10 providers you already trust (restaurants, drivers, a chef, a beach club).
2. Add each entry with: name, location, why you recommend it, contact details, any caveats, and the date you last verified it.
3. Keep a "Do Not Recommend" section at the bottom — places you've ruled out. The agent never suggests anything on that list.
4. Add a line to the call log every time you call or visit a provider. Date every entry.
5. Split the file (e.g. into `restaurant-recommendations.md`, `beach-recommendations.md`, `chef-contacts.md`) once it gets long, and update the file path in the agent and skill files.

The agent proposes additions in its report when it learns something new, such as a price a provider confirmed. It edits the file only when you tell it to.

---

## How memory works

The agent file sets `memory: project`, so Claude Code gives the agent a memory folder at `.claude/agent-memory/concierge/`. On every run, Claude Code loads the first 200 lines of [`MEMORY.md`](.claude/agent-memory/concierge/MEMORY.md) from that folder. The agent opens the other files only when `MEMORY.md` points to them.

The agent saves:

- **Active stays** — guests with open concierge items and what is pending
- **Guest preferences** — worth keeping for a return visit
- **Feedback** — corrections and confirmed approaches (e.g. "use the guest's mobile from the PMS — don't ask the guest")

[`example-feedback-pattern.md`](.claude/agent-memory/concierge/example-feedback-pattern.md) shows the format for a feedback note. Delete it, and its line in `MEMORY.md`, once you have your own.

> **Memory files contain guest data.** They hold real guest names, dates and preferences, and the included `.gitignore` does not exclude them. If your copy of this repo is pushed anywhere, add `.claude/agent-memory/` to `.gitignore` first.

---

## Troubleshooting

| Symptom | What to check |
|---|---|
| `concierge` is not in `/agents` | Start `claude` from the repo root. The file must be at `.claude/agents/concierge.md` and start with `---` on line 1. |
| The agent stops and lists placeholders | A `{{...}}` is still in the agent or skill file. Replace it or write `none`. |
| "Command not found" or wrong flags in the report | The command examples in the skill do not match your tools. Correct them in the skill's "Commands" section. |
| It says there is no vetted provider | The reference file is empty, or you renamed or split it and the agent and skill files still name the old path. |
| It stops partway with a partial result | The agent has a 30-turn limit (`maxTurns`). Ask Claude Code to continue the concierge agent, or raise the number. |
| Memory is not kept between runs | Auto memory is switched off in your Claude Code settings. Agent memory depends on it. |

---

## Related agents

This agent works well alongside:

- [`email-triage-agent`](https://github.com/th1-ai/email-triage-agent) — flags incoming guest emails that mention dining or activities so concierge is invoked promptly
- [`pre-arrival-outreach-agent`](https://github.com/th1-ai/pre-arrival-outreach-agent) — reaches out to upcoming bookings and hands the conversation to concierge once a guest engages
- [`booking-inquiry-agent`](https://github.com/th1-ai/booking-inquiry-agent) — drafts the reply that turns an inquiry into a booking, before concierge picks up
- [`morning-routine-agent`](https://github.com/th1-ai/morning-routine-agent) — its daily briefing includes concierge follow-ups
- [`web-research-agent`](https://github.com/th1-ai/web-research-agent) — useful when you're vetting a candidate provider before you add them to your list

The full set of 21 agents is at [th1.ai/agent-stack](https://th1.ai/agent-stack).

---

## License

MIT — see [LICENSE](LICENSE).
