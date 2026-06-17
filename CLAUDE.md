# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a runnable application**. It is a distributable **Hermes/Claude skill** that turns an
AI assistant into a read-only senior sales director and CRM analyst for **Bitrix24**. The deliverable
is `SKILL.md` plus its `references/`, `scripts/`, and `examples/`. Users install it with:

```bash
hermes skills install https://raw.githubusercontent.com/laserhall/sales-director-crm-analyst-for-bitrix24/main/SKILL.md
```

Most "development" here is editing prose (the skill instructions and reference playbooks), not code.
The two Python scripts are thin, dependency-free probes used to validate Bitrix24 connectivity.

## Architecture

The repository has three coordinated layers; understanding how they reference each other matters more
than any single file:

1. **`SKILL.md`** — the entry point and contract. Its YAML frontmatter (`name`, `description`,
   `version`, `tags`) is what the skill registry reads. The body defines the assistant's persona, the
   six analysis modes (single deal, Open Lines dialog, stuck deals, manager performance, pipeline
   health, win/loss), the fixed **output formats** for each mode, safety rules, and a closing
   verification checklist. The "workflow links" section points to every file in `references/`.

2. **`references/*.md`** — the knowledge base loaded on demand. `bitrix24-readonly-workflows.md` is the
   canonical source for *which Bitrix24 REST methods are allowed* and how to call/paginate them; the
   other files are scoring rubrics and playbooks (SLA, conversation-quality score, deal-analysis
   framework, follow-up playbooks, data-safety, etc.). When you change an allowed method or an output
   format in `SKILL.md`, keep these in sync.

3. **`scripts/*.py`** — executable, read-only Bitrix24 probes (standard library only, no deps). Both
   scripts enforce safety in code: they keep a hardcoded `READ_ONLY_METHODS` allowlist and the
   `endpoint()` helper *raises* on any method not in it, so write methods cannot be called even by
   mistake. Errors are passed through `safe_error()`, which redacts the webhook URL before printing.
   - `bitrix24_smoke_check.py` — checks connectivity and prints a capability summary (booleans for
     which read methods exist). Never prints the webhook URL.
   - `analyze_deal_readonly.py` — probes one deal: deal fields, activity count, linked Open Lines
     chat, and a small message page. Prints counts/IDs, never raw message text.

`examples/` holds **anonymized** sample inputs/outputs (a deal JSON, an Open Lines dialog JSON, two
sample reports). Use these as the format reference and never replace them with real CRM data.

## Core invariants (do not break these)

These rules are the entire point of the skill. Any edit must preserve them:

- **Read-only by default.** Only `get`/`list`/`search`/history methods. Never add `add`, `update`,
  `delete`, `set`, `send`, `message.add`, `notify`, `task.add`, or timeline-comment methods to a
  script allowlist or recommend them without explicit user confirmation.
- **Secret hygiene.** `BITRIX24_WEBHOOK_URL` is a secret. Never print, log, or commit it; always route
  errors through the redaction helper when touching script code.
- **Privacy.** Default to IDs, counts, stage names, and aggregates. Do not surface client names,
  phone/email, full deal titles, or raw dialog text. Keep examples anonymized.
- **Two-way consistency.** The allowed-method list and output formats appear in both `SKILL.md` and
  `references/bitrix24-readonly-workflows.md` — update both together.

## Commands

There is no build step, package manifest, or test suite. The scripts use only the Python standard
library (Python 3, `from __future__ import annotations`).

```bash
# One-time local config (the .env is gitignored; never commit it)
cp .env.example .env
# then edit .env and set BITRIX24_WEBHOOK_URL

# Load env and run the connectivity / capability check
set -a; source .env; set +a
python3 scripts/bitrix24_smoke_check.py

# Probe a single deal (read-only)
set -a; source .env; set +a
python3 scripts/analyze_deal_readonly.py --deal-id 12345
```

Exit codes: smoke check returns `0` on full success, `1` on partial failure, `2` if the webhook env
var is missing; the deal probe returns `0`/`1`/`2` similarly. There are no linters or CI configured.

## Conventions

- Documentation is **bilingual-aware**: respond in the user's language (English or Russian). The
  README carries a Russian section; keep parallel content in sync when editing user-facing docs.
- Bump `version:` in `SKILL.md` frontmatter for meaningful skill changes.
- Scripts must stay dependency-free and keep their `READ_ONLY_METHODS` allowlist + URL redaction.
- `.gitignore` deliberately excludes data formats that could leak CRM exports (`*.csv`, `*.xlsx`,
  `*.jsonl`, `exports/`, `dumps/`, `reports/private/`, `attachments/`, `*.pdf`) — keep it that way.
