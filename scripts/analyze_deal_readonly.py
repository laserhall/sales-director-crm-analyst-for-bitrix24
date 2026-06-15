#!/usr/bin/env python3
"""Safe read-only Bitrix24 single-deal probe.

The script reads a deal, activity metadata, linked Open Lines chat, and a limited
message page. It does not print raw message text by default.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

READ_ONLY_METHODS = {
    "crm.deal.get",
    "crm.activity.list",
    "imopenlines.crm.chat.get",
    "im.dialog.messages.get",
}


def safe_error(exc: BaseException, webhook_url: str) -> str:
    text = str(exc)
    if webhook_url:
        text = text.replace(webhook_url, "[REDACTED_WEBHOOK_URL]")
    return text[:500]


def endpoint(webhook_url: str, method: str) -> str:
    if method not in READ_ONLY_METHODS:
        raise ValueError(f"Refusing non-read-only method: {method}")
    return webhook_url.rstrip("/") + "/" + method + ".json"


def call_bitrix(webhook_url: str, method: str, params: Optional[Dict[str, Any]] = None, timeout: int = 20) -> Dict[str, Any]:
    data = urllib.parse.urlencode(params or {}, doseq=True).encode("utf-8")
    request = urllib.request.Request(endpoint(webhook_url, method), data=data, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    parsed = json.loads(payload)
    if "error" in parsed:
        raise RuntimeError(f"{parsed.get('error')}: {parsed.get('error_description', '')}")
    return parsed


def list_activities(webhook_url: str, deal_id: str, timeout: int) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    start: Any = 0
    while True:
        params = {
            "filter[OWNER_TYPE_ID]": 2,
            "filter[OWNER_ID]": deal_id,
            "order[ID]": "DESC",
            "select[0]": "ID",
            "select[1]": "TYPE_ID",
            "select[2]": "PROVIDER_ID",
            "select[3]": "PROVIDER_TYPE_ID",
            "select[4]": "CREATED",
            "select[5]": "LAST_UPDATED",
            "select[6]": "DEADLINE",
            "select[7]": "COMPLETED",
            "select[8]": "RESPONSIBLE_ID",
            "select[9]": "ASSOCIATED_ENTITY_ID",
            "start": start,
        }
        response = call_bitrix(webhook_url, "crm.activity.list", params, timeout)
        page = response.get("result") or []
        if isinstance(page, list):
            items.extend(page)
        next_start = response.get("next")
        if next_start is None:
            break
        start = next_start
        if len(items) >= 500:
            break
    return items


def normalize_chat_result(result: Any) -> List[Dict[str, Any]]:
    if isinstance(result, list):
        return [x for x in result if isinstance(x, dict)]
    if isinstance(result, dict):
        if "CHAT_ID" in result:
            return [result]
        if "chats" in result and isinstance(result["chats"], list):
            return [x for x in result["chats"] if isinstance(x, dict)]
        return [x for x in result.values() if isinstance(x, dict) and "CHAT_ID" in x]
    return []


def extract_messages(result: Any) -> List[Dict[str, Any]]:
    if isinstance(result, list):
        return [x for x in result if isinstance(x, dict)]
    if isinstance(result, dict):
        for key in ("messages", "MESSAGE", "result"):
            value = result.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
        if "MESSAGES" in result and isinstance(result["MESSAGES"], list):
            return [x for x in result["MESSAGES"] if isinstance(x, dict)]
    return []


def infer_last_message_side(message: Dict[str, Any]) -> str:
    # Without portal-specific user/contact mapping, do not guess personal identity.
    if not message:
        return "unknown"
    if message.get("SYSTEM") in ("Y", True):
        return "system"
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Bitrix24 deal summary")
    parser.add_argument("--deal-id", required=True, help="Bitrix24 deal ID")
    parser.add_argument("--message-limit", type=int, default=int(os.environ.get("BITRIX24_MESSAGE_LIMIT", "20")))
    args = parser.parse_args()

    webhook_url = os.environ.get("BITRIX24_WEBHOOK_URL", "").strip()
    timeout = int(os.environ.get("BITRIX24_TIMEOUT_SECONDS", "20"))
    message_limit = max(1, min(args.message_limit, 50))

    summary: Dict[str, Any] = {
        "deal_id": str(args.deal_id),
        "has_deal": False,
        "stage_id": None,
        "activity_count": 0,
        "has_openline_chat": False,
        "message_count": 0,
        "last_message_side": "unknown",
        "warnings": [],
    }

    if not webhook_url:
        summary["warnings"].append("BITRIX24_WEBHOOK_URL is not set")
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    try:
        deal_response = call_bitrix(webhook_url, "crm.deal.get", {"id": args.deal_id}, timeout)
        deal = deal_response.get("result")
        if isinstance(deal, dict) and deal:
            summary["has_deal"] = True
            summary["stage_id"] = deal.get("STAGE_ID")
        else:
            summary["warnings"].append("Deal not found or empty result")
    except Exception as exc:  # noqa: BLE001
        summary["warnings"].append("crm.deal.get failed: " + safe_error(exc, webhook_url))
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 1

    try:
        activities = list_activities(webhook_url, str(args.deal_id), timeout)
        summary["activity_count"] = len(activities)
    except Exception as exc:  # noqa: BLE001
        summary["warnings"].append("crm.activity.list failed: " + safe_error(exc, webhook_url))

    try:
        chat_response = call_bitrix(
            webhook_url,
            "imopenlines.crm.chat.get",
            {"CRM_ENTITY_TYPE": "DEAL", "CRM_ENTITY": args.deal_id},
            timeout,
        )
        chats = normalize_chat_result(chat_response.get("result"))
        summary["has_openline_chat"] = bool(chats)
        if chats:
            chat_id = chats[0].get("CHAT_ID") or chats[0].get("ID")
            if chat_id:
                messages_response = call_bitrix(
                    webhook_url,
                    "im.dialog.messages.get",
                    {"DIALOG_ID": f"chat{chat_id}", "LIMIT": message_limit},
                    timeout,
                )
                messages = extract_messages(messages_response.get("result"))
                summary["message_count"] = len(messages)
                if messages:
                    summary["last_message_side"] = infer_last_message_side(messages[0])
        else:
            summary["warnings"].append("No linked Open Lines chat found")
    except Exception as exc:  # noqa: BLE001
        summary["warnings"].append("Open Lines read failed: " + safe_error(exc, webhook_url))

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
