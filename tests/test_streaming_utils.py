from streaming_utils import iter_gemini_sse_lines, iter_openai_sse_lines, iter_text_chunks, smooth_stream


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


def test_iter_text_chunks_preserves_markdown_exactly():
    markdown = "## Titel\n\nEin kurzer **Fallback**."
    assert "".join(iter_text_chunks(markdown, delay_seconds=0)) == markdown


def test_smooth_stream_coalesces_tiny_tokens_without_changing_text():
    tokens = ["Ein", " ", "ruhiger", " ", "Token", "-", "Stream"]
    chunks = list(smooth_stream(tokens, target_chars=20))

    assert "".join(chunks) == "Ein ruhiger Token-Stream"
    assert len(chunks) < len(tokens)
