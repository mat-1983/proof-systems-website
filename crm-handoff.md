# Minimum CRM Handoff

Use one lightweight lead register chosen by Mat. Do not use Linear as the lead database and do not create live automation before approval.

## Minimum fields

`lead_id`, `received_at`, `name`, `email`, `phone`, `company`, `role`, `sector`, `route_key`, `lead_state`, `workflow_summary`, `hours_per_week`, `consent_recorded`, `owner`, `stage`, `next_action`, `next_action_due`, `last_contacted_at`, `outcome`, `retention_delete_after`, `source_submission_id`.

Keep the original detailed submission in Netlify only as long as needed. Put a short, non-sensitive summary in the register rather than copying all free-text answers.

## Stages and rules

| Stage | Owner | Required next action |
| --- | --- | --- |
| New | Mat | Review by next working day |
| Needs clarification | Mat | Send the short qualification template |
| Fit confirmed | Mat | Send the appropriate next step |
| Call booked | Mat | Record booking date and intended route |
| Diagnostic proposed | Mat | Record proposal status; no payment activation |
| Training proposed | Mat | Record remote workshop fit and next decision |
| Nurture/deferred | Mat | Record an agreed review date or close |
| Closed | Mat | Record outcome and retention date |

Fail-safe: the register must have a saved view for open leads whose `next_action_due` is today or overdue. Review it each working day. A lead cannot remain open without an owner and dated next action.

## Test cases

Run one synthetic record through diagnostic, video/guide, call, training and no-fit outcomes. Each must retain a single owner, route, stage and next action without producing a duplicate Linear issue or parallel task list.
