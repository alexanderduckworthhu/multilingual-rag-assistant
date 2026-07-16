"""Orchestrate retrieve → distance gate → LLM or extractive answer."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import APIConnectionError, APIError, AuthenticationError, OpenAI, RateLimitError

from src.config import EXTRACTIVE_PASSAGE_COUNT, LLM_MODEL, LLM_TEMPERATURE, RETRIEVAL_TOP_K
from src.generate.prompts import build_messages
from src.generate.translate import DisplayPassage, prepare_display_passages
from src.i18n import CORPUS_LANG_CODES, t
from src.retrieve.search import RetrievedChunk, retrieve

load_dotenv()
logger = logging.getLogger(__name__)


@dataclass
class RagResponse:
    """Grounded QA result returned to the Streamlit UI."""

    answer: str
    chunks: list[RetrievedChunk]
    display_passages: list[DisplayPassage]
    grounded: bool
    mode: str  # llm | extractive | refused | empty_index | llm_error
    answer_language: str


def _passages_for_display(
    chunks: list[RetrievedChunk],
    answer_language: str,
) -> list[RetrievedChunk]:
    """Prefer same-language passages when the corpus has that language."""
    if answer_language not in CORPUS_LANG_CODES:
        return chunks
    matching = [chunk for chunk in chunks if chunk.language == answer_language]
    if matching:
        others = [chunk for chunk in chunks if chunk.language != answer_language]
        return matching + others
    return chunks


def _extractive_answer(
    display_passages: list[DisplayPassage],
    answer_language: str,
) -> str:
    """Build a passage-based answer in the selected language (translated if needed)."""
    selected = display_passages[:EXTRACTIVE_PASSAGE_COUNT]
    lines = [str(t(answer_language, "msg_extractive_header")), ""]

    if any(passage.was_translated for passage in selected):
        lines.append(str(t(answer_language, "msg_passages_translated")))
        lines.append("")
    elif answer_language in CORPUS_LANG_CODES and selected:
        lines.append(str(t(answer_language, "msg_extractive_same_lang")))
        lines.append("")

    for rank, passage in enumerate(selected, start=1):
        lines.append(f"{rank}. [{passage.chunk_id}] {passage.title}")
        lines.append(passage.display_text)
        lines.append("")
    return "\n".join(lines).strip()


def _call_llm(messages: list[dict[str, str]]) -> tuple[str | None, str | None]:
    """Call the chat model; return (answer_text, error_message)."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, None
    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            messages=messages,
        )
        return (completion.choices[0].message.content or "").strip(), None
    except (AuthenticationError, RateLimitError, APIConnectionError, APIError) as exc:
        logger.warning("LLM call failed: %s", exc)
        return None, str(exc)
    except Exception as exc:  # unexpected SDK failures still fall back extractively
        logger.exception("Unexpected LLM failure")
        return None, str(exc)


def answer_question(
    question: str,
    answer_language: str = "en",
    retrieve_language: str | None = None,
    top_k: int = RETRIEVAL_TOP_K,
) -> RagResponse:
    """Return a grounded answer (or refusal) for `question`.

    Retrieval prefers EN/FR corpus matches when the answer language is EN/FR.
    Display passages (and extractive answers) are translated into the selected
    answer language when the source text is in another language.
    """
    prefer_language = (
        answer_language if answer_language in CORPUS_LANG_CODES else None
    )
    chunks, is_grounded = retrieve(
        query=question,
        top_k=top_k,
        language=retrieve_language,
        prefer_language=prefer_language,
    )
    if not chunks:
        return RagResponse(
            answer=str(t(answer_language, "msg_empty_index")),
            chunks=[],
            display_passages=[],
            grounded=False,
            mode="empty_index",
            answer_language=answer_language,
        )

    if not is_grounded:
        return RagResponse(
            answer=str(t(answer_language, "msg_refusal")),
            chunks=chunks,
            display_passages=prepare_display_passages(chunks, answer_language),
            grounded=False,
            mode="refused",
            answer_language=answer_language,
        )

    chunks = _passages_for_display(chunks, answer_language)
    display_passages = prepare_display_passages(chunks, answer_language)

    # LLM still sees original corpus wording for faithful grounding.
    messages = build_messages(question, chunks, answer_language=answer_language)
    llm_text, llm_error = _call_llm(messages)
    if llm_text is None:
        return RagResponse(
            answer=_extractive_answer(display_passages, answer_language),
            chunks=chunks,
            display_passages=display_passages,
            grounded=True,
            mode="llm_error" if llm_error else "extractive",
            answer_language=answer_language,
        )

    return RagResponse(
        answer=llm_text,
        chunks=chunks,
        display_passages=display_passages,
        grounded=True,
        mode="llm",
        answer_language=answer_language,
    )
