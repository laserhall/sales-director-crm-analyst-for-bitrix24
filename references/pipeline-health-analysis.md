# Pipeline health analysis

Pipeline health means the CRM reflects sales reality closely enough for management decisions.

## Core checks

1. Stage aging: deals stay too long in one stage.
2. Stage exit criteria: stage names match objective evidence.
3. Next-step discipline: every live deal has a next action, owner, and timing.
4. Activity hygiene: recent activity exists for active deals.
5. Source quality: sources produce qualified opportunities, not only raw leads.
6. Forecast reality: expected revenue is not inflated by stale or unqualified deals.
7. Lost reason discipline: losses are classified consistently.
8. Duplicate/test/no-fit cleanup: non-sales records do not distort the pipeline.

## Risk buckets

- Critical: client is waiting, no response, hot deal stale, or deadline risk.
- Medium: proposal sent but no follow-up, missing decision-maker, stage aging.
- Low: minor CRM hygiene issue, weak source labeling, missing optional field.

## Stuck deal thresholds

Use default thresholds only as a starting point. Customize per business.

- New lead without response: same day or within configured first-response SLA.
- Proposal sent without follow-up: 1 business day.
- Active deal without planned next activity: 2 business days.
- Negotiation without customer response: 3-5 business days depending on deal size.
- Any open deal with no activity for 7+ days: review.

## Output

```text
Critical:
Medium risk:
Low risk:
Main causes:
What to do today:
```

## Forecast notes

Forecast should distinguish:

- committed / evidence-backed;
- likely / next step exists;
- possible / gaps remain;
- stale / should not be counted without recovery action.
