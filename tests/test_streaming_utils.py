from streaming_utils import iter_gemini_sse_lines, iter_openai_sse_lines


def test_iter_openai_sse_lines_yields_only_visible_content():
    lines = [
        b": keep-alive\n",
        b'data: {"choices":[{"delta":{"content":"Hallo"}}]}\n',
        b"data: malformed\n",
        b'data: {"choices":[{"delta":{"content":" Welt"}}]}\n',
        b"data: [DONE]\n",
    ]

    assert list(iter_openai_sse_lines(lines)) == ["Hallo", " Welt"]


def test_iter_gemini_sse_lines_yields_candidate_parts():
    lines = [
        b'data: {"candidates":[{"content":{"parts":[{"text":"Token"}]}}]}\n',
        b'data: {"candidates":[{"content":{"parts":[{"text":" Stream"}]}}]}\n',
        b'data: {"candidates":[]}\n',
    ]

    assert list(iter_gemini_sse_lines(lines)) == ["Token", " Stream"]
