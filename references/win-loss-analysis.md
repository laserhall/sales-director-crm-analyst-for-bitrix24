# Win/loss analysis

Win/loss analysis classifies outcomes using CRM evidence rather than anecdotes.

## Inputs

- period and basis: creation date or close date;
- won/lost deal list;
- stage and loss reason dictionaries;
- activities and Open Lines evidence;
- manager/source/category filters when requested.

## Generic win reasons

- fast response;
- clear fit to product/service;
- complete discovery and qualification;
- strong commercial proposal;
- realistic deadline;
- good follow-up;
- existing relationship;
- decision-maker engaged;
- source produced high-intent demand.

## Generic loss reasons

- price too high;
- deadline not possible;
- weak fit or unavailable service;
- customer only compared prices;
- no response after proposal;
- slow first response;
- missing follow-up;
- no budget;
- decision-maker not reached;
- duplicate/test/non-target lead;
- competitor selected;
- internal CRM data insufficient to classify.

## Classification rules

- Prefer evidence from dialog/activity history.
- If no evidence exists, classify as `unknown / insufficient CRM evidence`.
- Separate customer-caused and process-caused losses.
- Track repeated patterns by manager, source, product/service, and stage.

## Output

```text
Period:
Deals analyzed:
Why we win:
Why we lose:
Recurring patterns:
What to change:
```

## Management actions

- Update stage exit criteria.
- Improve follow-up automation or reminders.
- Coach managers on discovery/qualification.
- Adjust source investment if sources produce low-fit leads.
- Fix offer templates if losses cluster around unclear commercial terms.
