from glossary_advisor import (
    GLOSSARY_SWEEP_QUESTION,
    build_glossary_analysis_prompt,
    build_glossary_visible_question,
    polish_glossary_answer,
    parse_glossary_query,
    should_dispatch_pending_glossary,
)


def test_parse_glossary_query_requires_source_and_term():
    assert parse_glossary_query({"term": "BTP"}) is None
    assert parse_glossary_query({"source": "glossary"}) is None


def test_glossary_prompt_keeps_fixed_question_and_card_context():
    context = parse_glossary_query({
        "source": "glossary",
        "request_id": "123-BTP",
        "term": "BTP",
        "impact": "91",
        "sap": "SAP Business Technology Platform",
    })
    assert context is not None
    prompt = build_glossary_analysis_prompt(context)
    assert prompt.startswith("Der Glossar Eintrag")
    assert GLOSSARY_SWEEP_QUESTION in prompt
    assert "- term: BTP" in prompt
    assert "- impact: 91" in prompt
    assert "Erfinde keine SAP-Quellen" in prompt


def test_visible_question_names_card_and_answer_style_is_compact():
    context = {"term": "CLAUDE", "title": "Claude (Frontier AI Model Family by Anthropic)"}
    visible = build_glossary_visible_question(context)
    assert "Claude (Frontier AI Model Family by Anthropic)" in visible
    assert visible.index("Claude") < visible.index(GLOSSARY_SWEEP_QUESTION)

    verbose = (
        "Sehr geehrter Markus Engelmann, liebes Conciliamus-Team,\n"
        "als Ihr Conciliamus AI Architecture Advisor beantworte ich die Anfrage auf Basis des OKF.\n\n"
        "## Zusammenfassung für das Team\nRelevant."
    )
    polished = polish_glossary_answer(verbose)
    assert polished == "## Zusammenfassung\nRelevant."


def test_query_launch_waits_for_chat_hydration_and_dispatches_once():
    context = {"request_id": "req-42", "term": "BTP"}

    assert not should_dispatch_pending_glossary(context, False, None)
    assert should_dispatch_pending_glossary(context, True, None)
    assert not should_dispatch_pending_glossary(context, True, "req-42")
