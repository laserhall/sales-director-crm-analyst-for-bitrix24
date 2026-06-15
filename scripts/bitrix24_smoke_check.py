#!/usr/bin/env python3
"""Safe read-only Bitrix24 capability smoke check.

Reads BITRIX24_WEBHOOK_URL from the environment and prints a safe JSON summary.
The webhook URL is never printed.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, Optional

READ_ONLY_METHODS = {
    "profile",
    "user.current",
    "methods",
    "crm.deal.list",
    "imopenlines.config.list.get",
}


def _safe_error(exc: BaseException, webhook_url: str) -> str:
    text = str(exc)
    if webhook_url:
        text = text.replace(webhook_url, "[REDACTED_WEBHOOK_URL]")
    return text[:500]


def _endpoint(webhook_url: str, method: str) -> str:
    if method not in READ_ONLY_METHODS:
        raise ValueError(f"Refusing non-read-only method: {method}")
    return webhook_url.rstrip("/") + "/" + method + ".json"


def call_bitrix(method: str, params: Optional[Dict[str, Any]] = None, timeout: int = 20) -> Dict[str, Any]:
    webhook_url = os.environ.get("BITRIX24_WEBHOOK_URL", "").strip()
    if not webhook_url:
        raise RuntimeError("BITRIX24_WEBHOOK_URL is not set")
    data = urllib.parse.urlencode(params or {}, doseq=True).encode("utf-8")
    request = urllib.request.Request(_endpoint(webhook_url, method), data=data, method="POST")
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


def result_ok(method: str, params: Optional[Dict[str, Any]], timeout: int) -> Dict[str, Any]:
    webhook_url = os.environ.get("BITRIX24_WEBHOOK_URL", "").strip()
    started = time.time()
    try:
        response = call_bitrix(method, params, timeout=timeout)
        return {"ok": True, "elapsed_ms": int((time.time() - started) * 1000), "response": response}
    except Exception as exc:  # noqa: BLE001 - safe CLI summary
        return {"ok": False, "elapsed_ms": int((time.time() - started) * 1000), "error": _safe_error(exc, webhook_url)}


def normalize_methods(result: Any) -> Iterable[str]:
    if isinstance(result, list):
        return [str(x) for x in result]
    if isinstance(result, dict):
        values = []
        for value in result.values():
            if isinstance(value, list):
                values.extend(str(x) for x in value)
        return values
    return []


def main() -> int:
    webhook_url = os.environ.get("BITRIX24_WEBHOOK_URL", "").strip()
    timeout = int(os.environ.get("BITRIX24_TIMEOUT_SECONDS", "20"))
    summary: Dict[str, Any] = {
        "ok": False,
        "checks": {},
        "capabilities": {},
        "errors": [],
    }

    if not webhook_url:
        summary["errors"].append("BITRIX24_WEBHOOK_URL is not set")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 2

    profile = result_ok("profile", {}, timeout)
    user_current = result_ok("user.current", {}, timeout)
    methods_response = result_ok("methods", {}, timeout)
    deal_list = result_ok(
        "crm.deal.list",
        {"select[0]": "ID", "order[ID]": "DESC", "start": 0},
        timeout,
    )

    for name, check in [
        ("profile", profile),
        ("user.current", user_current),
        ("methods", methods_response),
        ("crm.deal.list.select_id", deal_list),
    ]:
        summary["checks"][name] = {k: v for k, v in check.items() if k != "response"}
        if not check["ok"]:
            summary["errors"].append(f"{name}: {check.get('error')}")

    methods = []
    if methods_response["ok"]:
        methods = list(normalize_methods(methods_response.get("response", {}).get("result")))

    method_set = set(methods)
    summary["capabilities"] = {
        "has_methods_list": bool(methods),
        "crm_deal_list": "crm.deal.list" in method_set,
        "crm_deal_get": "crm.deal.get" in method_set,
        "crm_activity_list": "crm.activity.list" in method_set,
        "crm_contact_get": "crm.contact.get" in method_set,
        "has_imopenlines_methods": any(m.startswith("imopenlines.") for m in method_set),
        "imopenlines_crm_chat_get": "imopenlines.crm.chat.get" in method_set,
        "imopenlines_session_history_get": "imopenlines.session.history.get" in method_set,
        "imopenlines_config_list_get": "imopenlines.config.list.get" in method_set,
        "im_dialog_messages_get": "im.dialog.messages.get" in method_set,
    }

    if summary["capabilities"].get("imopenlines_config_list_get"):
        config_check = result_ok("imopenlines.config.list.get", {}, timeout)
        summary["checks"]["imopenlines.config.list.get"] = {k: v for k, v in config_check.items() if k != "response"}
        summary["capabilities"]["can_call_imopenlines_config_list_get"] = bool(config_check["ok"])
        if not config_check["ok"]:
            summary["errors"].append(f"imopenlines.config.list.get: {config_check.get('error')}")
    else:
        summary["capabilities"]["can_call_imopenlines_config_list_get"] = False

    summary["ok"] = profile["ok"] and user_current["ok"] and methods_response["ok"] and deal_list["ok"]
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
