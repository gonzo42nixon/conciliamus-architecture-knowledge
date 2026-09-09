"""Small, provider-neutral helpers for streamed advisor responses."""

from __future__ import annotations

import json
import re
import time
from collections.abc import Iterable, Iterator


def iter_openai_sse_lines(lines: Iterable[bytes]) -> Iterator[str]:
    """Yield visible text tokens from an OpenAI-compatible SSE response."""
    for raw_line in lines:
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if not payload or payload == "[DONE]":
            continue
        try:
            event = json.loads(payload)
            content = event.get("choices", [{}])[0].get("delta", {}).get("content")
        except (TypeError, ValueError, IndexError):
            continue
        if content:
            yield content


def iter_gemini_sse_lines(lines: Iterable[bytes]) -> Iterator[str]:
    """Yield text tokens from Gemini's streamGenerateContent SSE format."""
    for raw_line in lines:
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if not payload:
            continue
        try:
            event = json.loads(payload)
            parts = event.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        except (TypeError, ValueError, IndexError):
            continue
        for part in parts:
            text = part.get("text") if isinstance(part, dict) else None
            if text:
                yield text


def iter_text_chunks(text: str, delay_seconds: float = 0.012) -> Iterator[str]:
    """Stream a local Markdown fallback in readable word-sized chunks."""
    for chunk in re.findall(r"\S+\s*|\s+", text):
        yield chunk
        if delay_seconds:
            time.sleep(delay_seconds)
