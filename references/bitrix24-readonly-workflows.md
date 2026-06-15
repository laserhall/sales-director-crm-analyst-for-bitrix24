# Bitrix24 read-only workflows

This reference describes safe read-only workflows for Bitrix24 CRM and Open Lines analysis.

## Principles

- Prefer `get`, `list`, `search`, and safe history methods.
- Do not use `add`, `update`, `delete`, `set`, `send`, `message.add`, `notify`, `task.add`, `crm.timeline.comment.add`, or automation execution methods unless the user explicitly asks and confirms.
- Select only fields required for the current analysis.
- Do not print personal data by default.
- Keep raw exports local and out of public repositories.

## Webhook handling

Scripts read `BITRIX24_WEBHOOK_URL` from the environment. The URL is a secret. Never print it, log it, or commit it.

Common local setup:

```bash
set -a; source .env; set +a
python3 scripts/bitrix24_smoke_check.py
```

## Safe field selection

For broad lists, start with IDs and operational fields:

- `ID`
- `TITLE` only if explicitly needed and safe to show; otherwise omit
- `STAGE_ID`
- `CATEGORY_ID`
- `ASSIGNED_BY_ID`
- `SOURCE_ID`
- `DATE_CREATE`
- `DATE_MODIFY`
- `CLOSEDATE`
- `OPPORTUNITY`
- `CURRENCY_ID`

Avoid by default:

- phone and email fields;
- full contact names;
- comments;
- full message text;
- attachments;
- raw custom fields that may contain personal data.

## Deal workflow

### Single deal

1. `crm.deal.get`
   - parameter: `id=<deal_id>`
   - use to confirm existence and read safe operational fields.
2. `crm.activity.list`
   - filter: `OWNER_TYPE_ID=2`, `OWNER_ID=<deal_id>`
   - select safe activity metadata.
3. `imopenlines.crm.chat.get`
   - parameters: `CRM_ENTITY_TYPE=DEAL`, `CRM_ENTITY=<deal_id>`
   - use to find linked Open Lines chat IDs.
4. `im.dialog.messages.get`
   - parameter: `DIALOG_ID=chat<CHAT_ID>`
   - use a small `LIMIT`; do not print raw text by default.

### Deal list / stuck review

Use `crm.deal.list` with period, stage, category, assigned manager, or modification filters.

Useful filters:

- `filter[>=DATE_CREATE]`
- `filter[<DATE_CREATE]`
- `filter[>=DATE_MODIFY]`
- `filter[ASSIGNED_BY_ID]`
- `filter[STAGE_ID]`
- `filter[CATEGORY_ID]`
- `filter[CLOSED]=N`

## Contacts workflow

1. `crm.deal.contact.items.get`
   - parameter: `id=<deal_id>`
   - returns contact bindings.
2. `crm.contact.get`
   - parameter: `id=<contact_id>`
   - use only when role/context is required.
   - do not print phone/email/name by default.

## Activities workflow

- `crm.activity.list` for activity metadata and counts.
- `crm.activity.get` for a specific activity when detailed analysis is required.

Safe metadata:

- `ID`
- `TYPE_ID`
- `PROVIDER_ID`
- `PROVIDER_TYPE_ID`
- `CREATED`
- `LAST_UPDATED`
- `DEADLINE`
- `COMPLETED`
- `RESPONSIBLE_ID`
- `ASSOCIATED_ENTITY_ID`

## Open Lines workflow

Read-only methods:

- `imopenlines.crm.chat.get`
- `im.dialog.messages.get`
- `imopenlines.session.history.get`
- `imopenlines.config.list.get`
- `imopenlines.config.get`

Notes:

- For group/open-line chats, `DIALOG_ID` often must be `chat<CHAT_ID>`, not just the numeric ID.
- Keep message limits small for analysis samples.
- Do not quote full dialog text in public reports.
- `imopenlines.session.history.get` may require a session ID obtained from CRM activity metadata.

## Dictionaries

Use dictionaries to make reports readable:

- `crm.status.list` for stage/status labels;
- `crm.dealcategory.list` for pipelines/categories.

Do not assume stage IDs mean the same thing across portals.

## Users/managers

Read-only methods:

- `user.search`
- `user.get`

Use manager IDs in public or semi-public outputs. Show names only when the report is internal and safe.

## Pagination

Bitrix24 list methods usually return up to 50 records per page and may include `next` and `total`.

Workflow:

1. call with `start=0`;
2. if response includes `next`, call again with `start=<next>`;
3. stop when no `next` is returned;
4. cap pages for interactive analysis if the user did not request a full audit.

## Rate limits

Bitrix24 commonly enforces request limits. Use conservative pacing:

- avoid unnecessary fields;
- batch only when safe and understood;
- retry only transient errors;
- prefer narrow filters;
- for large reports, state the sampled period and limits.

## Error handling

Common errors:

- `ACCESS_DENIED`: missing permission or method unavailable to the current webhook/app.
- `QUERY_LIMIT_EXCEEDED`: rate limit hit; wait and retry later.
- `NOT_FOUND`: entity does not exist or is not visible to the credential.

When reporting errors, sanitize secrets and avoid printing full request URLs.
