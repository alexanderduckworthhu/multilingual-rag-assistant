"""Translate corpus passages into the selected answer language for display."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

from src.i18n import CORPUS_LANG_CODES
from src.retrieve.search import RetrievedChunk

logger = logging.getLogger(__name__)

# deep-translator / Google Translate language codes
_GOOGLE_LANG_CODES: dict[str, str] = {
    "en": "en",
    "fr": "fr",
    "de": "de",
    "it": "it",
    "pt": "pt",
    "zh": "zh-CN",
    "ru": "ru",
}

# Google free endpoint soft limit — keep chunks under this.
_MAX_CHARS_PER_REQUEST = 4500


@dataclass
class DisplayPassage:
    """A retrieved passage prepared for UI display (possibly translated)."""

    chunk_id: str
    title: str
    source_language: str
    source_url: str
    distance: float
    original_text: str
    display_text: str
    was_translated: bool

    @property
    def language(self) -> str:
        """Source corpus language code (`en` / `fr`)."""
        return self.source_language


def _split_for_translation(text: str) -> list[str]:
    """Split long text into pieces under the translator size limit."""
    text = text.strip()
    if len(text) <= _MAX_CHARS_PER_REQUEST:
        return [text]

    paragraphs = re.split(r"\n\s*\n", text)
    pieces: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= _MAX_CHARS_PER_REQUEST:
            current = candidate
            continue
        if current:
            pieces.append(current)
        if len(paragraph) <= _MAX_CHARS_PER_REQUEST:
            current = paragraph
        else:
            # Hard split oversized paragraphs.
            for start in range(0, len(paragraph), _MAX_CHARS_PER_REQUEST):
                pieces.append(paragraph[start : start + _MAX_CHARS_PER_REQUEST])
            current = ""
    if current:
        pieces.append(current)
    return pieces or [text[:_MAX_CHARS_PER_REQUEST]]


def translate_text(
    text: str,
    target_language: str,
    source_language: str | None = None,
) -> str:
    """Translate `text` into `target_language`; return original text on failure."""
    if not text.strip():
        return text
    if target_language == source_language:
        return text

    target_code = _GOOGLE_LANG_CODES.get(target_language)
    if not target_code:
        return text

    source_code = "auto"
    if source_language in _GOOGLE_LANG_CODES:
        source_code = _GOOGLE_LANG_CODES[source_language]

    try:
        from deep_translator import GoogleTranslator

        translator = GoogleTranslator(source=source_code, target=target_code)
        translated_parts: list[str] = []
        for part in _split_for_translation(text):
            translated_parts.append(translator.translate(part))
        return "\n\n".join(translated_parts).strip()
    except Exception:
        logger.exception(
            "Translation failed target=%s source=%s",
            target_language,
            source_language,
        )
        return text


def prepare_display_passages(
    chunks: list[RetrievedChunk],
    target_language: str,
) -> list[DisplayPassage]:
    """Return passages with `display_text` in `target_language` when needed."""
    prepared: list[DisplayPassage] = []
    for chunk in chunks:
        needs_translation = chunk.language != target_language
        # Same-language corpus hit — no translation.
        if not needs_translation:
            display_text = chunk.text
            was_translated = False
        elif (
            target_language in CORPUS_LANG_CODES
            and chunk.language == target_language
        ):
            display_text = chunk.text
            was_translated = False
        else:
            display_text = translate_text(
                chunk.text,
                target_language=target_language,
                source_language=chunk.language or None,
            )
            was_translated = display_text.strip() != chunk.text.strip()

        prepared.append(
            DisplayPassage(
                chunk_id=chunk.chunk_id,
                title=chunk.title,
                source_language=chunk.language,
                source_url=chunk.source_url,
                distance=chunk.distance,
                original_text=chunk.text,
                display_text=display_text,
                was_translated=was_translated,
            )
        )
    return prepared
