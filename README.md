# Sales Director & CRM Analyst for Bitrix24

Open-source Hermes skill for read-only Bitrix24 CRM analysis: deals, Open Lines conversations, stuck opportunities, manager performance, pipeline health, and win/loss patterns.

The skill is designed for owners, heads of sales, RevOps teams, and CRM analysts who need practical management conclusions from Bitrix24 data without changing production CRM records by default.

## What it does

- Reviews a single deal using Bitrix24 deal fields, activities, contacts, and Open Lines chat metadata.
- Evaluates Open Lines dialog quality: response speed, discovery, qualification, commercial handling, next-step clarity, and CRM discipline.
- Finds stuck deals and pipeline risks.
- Reviews manager performance by period, stage, source, activity, and communication quality.
- Checks pipeline health: stage aging, hygiene, stage exit criteria, next-step discipline, and forecast realism.
- Classifies win/loss reasons using CRM evidence instead of guesses.
- Produces concise recommendations for sales leadership.

## What it does not do

- It does not modify Bitrix24 records unless the user explicitly asks for a write operation and confirms the scope.
- It does not expose webhook URLs, tokens, phone numbers, emails, client names, deal titles, or raw dialog text by default.
- It does not replace a human sales leader; it gives structured evidence-based recommendations.
- It does not provide universal SLA or scoring values that fit every business without customization.

## Installation

Install the skill from the public raw URL:

```bash
hermes skills install https://raw.githubusercontent.com/laserhall/sales-director-crm-analyst-for-bitrix24/main/SKILL.md
```

## Configuration

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Set your Bitrix24 incoming webhook URL locally:

```bash
BITRIX24_WEBHOOK_URL="https://example.bitrix24.com/rest/1/REPLACE_WITH_WEBHOOK_CODE/"
```

Do not commit `.env`. The `.gitignore` excludes it.

## Smoke check

Run a safe read-only connection check:

```bash
set -a; source .env; set +a
python3 scripts/bitrix24_smoke_check.py
```

The script checks only read methods and prints safe capability flags. It never prints the webhook URL.

## Usage examples

In Hermes, ask for tasks such as:

- `Analyze deal 12345`
- `Find stuck deals for the last 7 days`
- `Review manager performance for this week`
- `Analyze open-line dialog for deal 12345`
- `Explain why we lost deals last month without exposing client data`

You can also run a single safe deal probe:

```bash
set -a; source .env; set +a
python3 scripts/analyze_deal_readonly.py --deal-id 12345
```

## Privacy warning

Bitrix24 CRM may contain personal data, client messages, commercial terms, and internal notes. Treat all raw data as confidential.

Default behavior:

- use IDs and aggregate counts;
- redact personal data;
- do not quote full Open Lines messages;
- do not print webhook URLs or tokens;
- do not commit `.env`, exports, dumps, or raw CRM files.

## Русское описание

Этот skill превращает Hermes в read-only РОПа и CRM-аналитика для Bitrix24: разбор сделок, открытых линий, зависших сделок, качества работы менеджеров, здоровья воронки и причин выигрышей/проигрышей.

По умолчанию skill ничего не меняет в CRM. Он анализирует факты, показывает риски и предлагает управленческие действия. Персональные данные клиентов, телефоны, email, webhook URL и полные тексты диалогов не выводятся без явной необходимости и безопасного контекста.

## Repository layout

```text
sales-director-crm-analyst-for-bitrix24/
  README.md
  LICENSE
  .gitignore
  .env.example
  SKILL.md
  references/
  scripts/
  examples/
```

## License

MIT. See [LICENSE](LICENSE).
