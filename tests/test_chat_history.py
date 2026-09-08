from chat_history import (
    UNTITLED_LABEL,
    active_chat,
    bind_session,
    new_store,
    normalize_store,
    select_chat,
    start_new_chat,
    touch_active_chat,
)


def test_chat_lifecycle_and_labels():
    store = new_store()
    first = active_chat(store)
    first["messages"].append({"role": "user", "content": "Wie funktioniert ADR-001 im Detail?"})
    touch_active_chat(store)
    assert first["label"] == "Wie funktioniert ADR-001 im Detail?"

    second = start_new_chat(store)
    assert second["label"] == UNTITLED_LABEL
    assert select_chat(store, first["id"])
    assert active_chat(store)["id"] == first["id"]


def test_normalization_rejects_invalid_messages_and_binds_active_list():
    raw = {
        "active_id": "one",
        "chats": [{
            "id": "one",
            "label": "Test",
            "created_at": "2026-09-08T07:00:00+00:00",
            "updated_at": "2026-09-08T07:00:00+00:00",
            "messages": [
                {"role": "user", "content": "Hallo"},
                {"role": "system", "content": "nicht übernehmen"},
            ],
        }],
    }
    session = {}
    bind_session(session, raw)
    assert session["messages"] == [{"role": "user", "content": "Hallo"}]
    assert normalize_store("not json")["chats"]
