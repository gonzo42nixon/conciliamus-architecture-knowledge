from glossary_advisor import (
    GLOSSARY_SWEEP_QUESTION,
    build_glossary_analysis_prompt,
    parse_glossary_query,
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
    assert prompt.startswith(GLOSSARY_SWEEP_QUESTION)
    assert "- term: BTP" in prompt
    assert "- impact: 91" in prompt
    assert "Erfinde keine SAP-Quellen" in prompt
