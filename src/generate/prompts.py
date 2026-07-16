"""Closed-context citation prompts for grounded generation."""

from __future__ import annotations

from typing import Sequence

from src.i18n import llm_language_name
from src.retrieve.search import RetrievedChunk

SYSTEM_PROMPT = """You are a careful research assistant for WHO public guidance.
Answer ONLY using the CONTEXT passages below.
If the context is insufficient, say you cannot find the answer in the indexed documents.
Do not use outside knowledge. Do not invent statistics, dates, or policy positions.
Every factual sentence must end with a citation like [doc_id::c0001].

Language rules:
- Write the entire answer in {answer_language}.
- Prefer CONTEXT passages whose lang= matches the answer language when they exist.
- If CONTEXT is only in another language, translate faithfully into {answer_language}
  without adding facts that are not in CONTEXT. Keep the same citations.
"""

USER_PROMPT = """QUESTION:
{question}

CONTEXT:
{context}

Write a short answer in {answer_language} with citations. Prefer same-language sources when available. If you cannot answer from CONTEXT, say so clearly in {answer_language}.
"""


def format_context(chunks: Sequence[RetrievedChunk]) -> str:
    """Serialize retrieved passages into the LLM context block (order preserved)."""
    blocks = [
        f"[{chunk.chunk_id}] (lang={chunk.language}, title={chunk.title})\n{chunk.text}"
        for chunk in chunks
    ]
    return "\n\n---\n\n".join(blocks)


def build_messages(
    question: str,
    chunks: Sequence[RetrievedChunk],
    answer_language: str = "en",
) -> list[dict[str, str]]:
    """Build chat messages that constrain the model to retrieved context."""
    language_name = llm_language_name(answer_language)
    preferred = [c for c in chunks if c.language == answer_language]
    other = [c for c in chunks if c.language != answer_language]
    ordered_chunks = preferred + other
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.format(answer_language=language_name),
        },
        {
            "role": "user",
            "content": USER_PROMPT.format(
                question=question,
                context=format_context(ordered_chunks),
                answer_language=language_name,
            ),
        },
    ]
