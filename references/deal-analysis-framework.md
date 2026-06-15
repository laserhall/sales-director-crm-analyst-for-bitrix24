# Deal analysis framework

Use this framework for one-deal Bitrix24 analysis.

## Goal

Turn CRM facts into a practical sales-director conclusion:

- what the customer needs;
- whether the deal is in the right stage;
- what is missing;
- what creates risk;
- what the manager should do next.

## Read-only evidence

Use:

- deal fields and stage;
- activity count and last activity date;
- Open Lines chat presence and safe metadata;
- selected recent messages only if needed and private;
- contact/company role only if relevant and safe;
- stage dictionaries.

## Core questions

1. What does the customer want to buy?
2. Is the request technically complete enough for an offer?
3. Was a proposal or calculation sent?
4. Did the customer respond after the proposal?
5. Is there a decision date or next step?
6. Is the current stage justified by evidence?
7. Is the deal stale compared with normal SLA?
8. What is the most likely reason it will be won or lost?

## Deal score dimensions

Score qualitatively or numerically depending on the task.

| Dimension | What to check |
|---|---|
| Need clarity | Product/service, quantity, deadline, use case |
| Qualification | budget, authority, timing, fit, repeat potential |
| Technical completeness | specs, files, variants, constraints |
| Commercial handling | price sent, options, objection handling |
| Stage reality | stage matches evidence, no optimistic staging |
| Next-step discipline | owner, action, date, communication channel |
| Stalling risk | unanswered client, no follow-up, missing data, no decision |
| CRM hygiene | required fields, activities, notes, source, stage dates |

## Output

```text
Deal: {ID}
Summary:
Current status:
Known customer need:
Missing information:
Risks:
Recommended manager action:
Close probability:
Sales director comment:
```

## Close probability guidance

Use evidence, not optimism.

- High: clear need, clear decision process, recent positive response, next step scheduled, stage is justified.
- Medium: real need exists but one or more gaps remain: budget, timing, decision-maker, proposal follow-up.
- Low: stale deal, no response, unclear fit, no next step, or stage unsupported by evidence.

## Stage exit criteria

Every pipeline stage should have objective exit criteria. Examples:

- New lead: customer contacted or first response attempted.
- Qualification: need, timing, fit, and next step clarified.
- Proposal: offer sent and follow-up scheduled.
- Negotiation: objection/decision process documented.
- Won: payment/order/contract confirmed according to business rules.
- Lost: reason classified and no active next step remains.
