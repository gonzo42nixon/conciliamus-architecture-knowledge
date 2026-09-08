"""Browser-persisted chat timeline state for the Streamlit advisor."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, MutableMapping
from uuid import uuid4


STORE_VERSION = 1
UNTITLED_LABEL = "Neuer Chat"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _new_chat() -> dict[str, Any]:
    timestamp = _now()
    return {
        "id": uuid4().hex,
        "label": UNTITLED_LABEL,
        "created_at": timestamp,
        "updated_at": timestamp,
        "messages": [],
    }


def new_store() -> dict[str, Any]:
    chat = _new_chat()
    return {"version": STORE_VERSION, "active_id": chat["id"], "chats": [chat]}


def normalize_store(value: object) -> dict[str, Any]:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            return new_store()
    if not isinstance(value, dict):
        return new_store()

    chats = []
    for candidate in value.get("chats", []):
        if not isinstance(candidate, dict) or not isinstance(candidate.get("messages"), list):
            continue
        chat = _new_chat()
        chat.update({key: candidate[key] for key in chat if key in candidate})
        chat["messages"] = [
            message for message in candidate["messages"]
            if isinstance(message, dict) and message.get("role") in {"user", "assistant"}
            and isinstance(message.get("content"), str)
        ]
        chats.append(chat)

    if not chats:
        return new_store()
    active_id = value.get("active_id")
    if not any(chat["id"] == active_id for chat in chats):
        active_id = chats[0]["id"]
    return {"version": STORE_VERSION, "active_id": active_id, "chats": chats}


def active_chat(store: dict[str, Any]) -> dict[str, Any]:
    for chat in store["chats"]:
        if chat["id"] == store["active_id"]:
            return chat
    store["active_id"] = store["chats"][0]["id"]
    return store["chats"][0]


def start_new_chat(store: dict[str, Any]) -> dict[str, Any]:
    chat = _new_chat()
    store["chats"].insert(0, chat)
    store["active_id"] = chat["id"]
    return chat


def select_chat(store: dict[str, Any], chat_id: str) -> bool:
    if any(chat["id"] == chat_id for chat in store["chats"]):
        store["active_id"] = chat_id
        return True
    return False


def touch_active_chat(store: dict[str, Any], label_hint: str | None = None) -> None:
    chat = active_chat(store)
    if chat["label"] == UNTITLED_LABEL:
        first_prompt = label_hint or next(
            (msg["content"] for msg in chat["messages"] if msg["role"] == "user"),
            UNTITLED_LABEL,
        )
        compact = " ".join(first_prompt.split())
        chat["label"] = compact[:52] + ("…" if len(compact) > 52 else "")
    chat["updated_at"] = _now()


def bind_session(session: MutableMapping[str, Any], store: object | None = None) -> None:
    session["chat_store"] = normalize_store(store if store is not None else session.get("chat_store"))
    session["messages"] = active_chat(session["chat_store"])["messages"]


def serialize_store(store: dict[str, Any]) -> str:
    return json.dumps(store, ensure_ascii=False, separators=(",", ":"))
