# Concierge Agent Memory Index

Claude Code loads the first 200 lines of this file into the concierge agent's context on every run. Other files in this folder are read only if they are listed here, so give each one a one-line entry.

## Feedback

- [example-feedback-pattern.md](example-feedback-pattern.md): example note. Use the guest's mobile and email from the PMS for provider bookings; never ask the guest again. Delete this entry and the file once you have your own.

## Active stays

> One file per stay with open concierge items. Remove the entry when the stay is closed.
>
> Format: `- [stay_<surname>_<YYYY-MM>.md](stay_<surname>_<YYYY-MM>.md): <dates>, <open items>`

## Guest preferences

> Notes worth keeping for a return visit.
>
> Format: `- [guest_<surname>.md](guest_<surname>.md): <one-line summary>`
