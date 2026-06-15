# Data safety and privacy

This skill is intended for CRM analysis. CRM data may include personal data, confidential commercial terms, internal notes, and sensitive communication history.

## Do not commit

- `.env` files;
- webhook URLs;
- API tokens;
- OAuth credentials;
- raw CRM exports;
- raw Open Lines message dumps;
- attachments;
- client lists;
- phone numbers;
- email addresses;
- client names;
- deal titles if they identify a client or project.

## Default redaction

Prefer:

- deal IDs;
- manager IDs when public, names only in internal safe reports;
- aggregate counts;
- stage/category labels;
- anonymized examples;
- short paraphrases instead of raw messages.

## Public examples

Examples in this repository are synthetic and anonymized. They are not real Bitrix24 records.

## Before sharing a report

Check:

- Does it contain a webhook URL or token?
- Does it identify a client?
- Does it quote private messages?
- Does it reveal internal prices or terms that should stay private?
- Is the audience allowed to see manager-level details?
- Is the report necessary, or would a shorter private answer be safer?
