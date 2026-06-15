# Open Lines dialog analysis

Analyze Open Lines conversations as sales-process evidence, not as isolated chat transcripts.

## What to review

- first response speed;
- whether the manager greeted and structured the conversation;
- whether the manager discovered the customer's real need;
- qualification depth;
- product/service fit;
- commercial clarity;
- follow-up and next step;
- CRM discipline after the dialog.

## Read-only sources

- `imopenlines.crm.chat.get` to locate linked chat;
- `im.dialog.messages.get` with small limits for recent messages;
- `imopenlines.session.history.get` if session history is available;
- CRM activities linked to the deal.

## Default privacy behavior

Do not quote raw message text by default. Summarize patterns:

- `client asked for price; manager requested specs; no follow-up after proposal`;
- `manager answered quickly but did not set next step`;
- `client's last question appears unanswered`.

## Review checklist

1. Was the first response timely?
2. Did the manager acknowledge the customer's request?
3. Were discovery questions asked before quoting?
4. Were key qualification points collected?
5. Did the manager explain fit/options in plain language?
6. Was price handled with context, options, and conditions?
7. Was a specific next step agreed?
8. Was the CRM updated with the correct stage/activity?

## Dialog report format

```text
Score: X/100
Strengths:
Problems:
Missing questions:
Next step:
Suggested reply:
```

## Suggested reply rules

Suggested replies should be:

- short enough to send to a client;
- specific to the missing information;
- not pushy unless the deal is already stale;
- privacy-safe;
- adapted to the user's language.
