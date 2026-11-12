# runs/

The concierge agent keeps its own record here. The files hold guest names and booking details, so the included `.gitignore` keeps everything in this folder out of git except this README and `.gitkeep`.

| File | Written by | What it is |
|---|---|---|
| `LOG.md` | The agent, one entry appended per run | The memory between runs. The agent reads the recent entries before it acts, so that it does not do the same work twice. The last entry is the summary of the latest run. |
| `handoff/concierge-agent.md` | The agent, replaced on every run | Open concierge items for [`morning-routine-agent`](https://github.com/th1-ai/morning-routine-agent). |
| `last-report.md` | Your scheduler (see the README) | The full text of the latest scheduled report. |

## Format of a `LOG.md` entry

The newest entry is at the bottom. The agent appends and never rewrites an earlier entry.

```
## 2026-01-15T08:02 · level 2 · scheduled
- Needs you: Service S-14 (transfer, 2026-01-17) still "Requested", provider silent since 2026-01-12.
- Checked: guest inboxes and provider inbox since 2026-01-14T15:01; tracker; calendar; PMS arrivals to 2026-01-29.
- Done: draft D-881 to guest <surname> [key msg-4471]; tracker Services row 14 added [key res-2207/restaurant/2026-01-18].
- Shadow: none.
- Proposed: add the price a provider confirmed to the provider file (see report).
- Errors: none.
```

- **Heading:** start time of the run, the level read from `AUTONOMY.md`, and `scheduled` or `on request`.
- **Needs you:** first, always present. `Nothing needs you` when empty.
- **Checked:** which systems were read and from which point in time. The next run starts from the start time of this entry.
- **Done:** each write, with the id the tool returned and a key in square brackets. The key is the message id for a reply, or `reservation id/service type/service date` for a service. A later run skips an item whose key is listed here.
- **Shadow:** actions the agent would have done under the "shadow first" rule in [`AUTONOMY.md`](../AUTONOMY.md).
- **Proposed:** what is left for you to decide or do.
- **Errors:** the failed command and its message. `none` when clean.

A run that stops at the kill switch writes one line with the reason, for example `## <time> · level PAUSED · scheduled · stopped: AUTONOMY.md says Level: PAUSED`, `stopped: AUTONOMY.md is missing` or `## <time> · level 0 · scheduled · stopped: Level 0`.

## Housekeeping

`LOG.md` grows. Once a month, move the old entries to another file such as `LOG-2026-01.md`. The agent reads only `LOG.md`.
