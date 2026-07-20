"""Vector retrieval with optional language filter and distance gating."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from src.config import MAX_COSINE_DISTANCE_TO_ANSWER, RETRIEVAL_TOP_K
from src.i18n import CORPUS_LANG_CODES
from src.ingest.embed import embed_query
from src.retrieve.store import get_or_create_collection

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    """One passage returned from the vector store for a user query."""

    chunk_id: str
    text: str
    distance: float
    metadata: dict[str, Any]

    @property
    def title(self) -> str:
        """Document title from metadata, falling back to chunk_id."""
        return str(self.metadata.get("title", self.chunk_id))

    @property
    def language(self) -> str:
        """ISO-ish language code stored at ingest time (`en` / `fr`)."""
        return str(self.metadata.get("language", ""))

    @property
    def source_url(self) -> str:
        """Provenance URL from the document sidecar metadata."""
        return str(self.metadata.get("source_url", ""))

    @property
    def doc_id(self) -> str:
        """Stable document identifier used in citations."""
        return str(self.metadata.get("doc_id", ""))


def _query_collection(
    query_embedding: list[float],
    top_k: int,
    passage_count: int,
    language: str | None,
) -> list[RetrievedChunk]:
    """Run one Chroma query and map rows to RetrievedChunk objects."""
    collection = get_or_create_collection()
    where_filter = (
        {"language": language} if language in CORPUS_LANG_CODES else None
    )
    query_result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, passage_count),
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )
    chunk_ids = query_result.get("ids", [[]])[0]
    documents = query_result.get("documents", [[]])[0]
    metadatas = query_result.get("metadatas", [[]])[0]
    distances = query_result.get("distances", [[]])[0]

    passages: list[RetrievedChunk] = []
    for chunk_id, text, metadata, distance in zip(
        chunk_ids, documents, metadatas, distances
    ):
        passages.append(
            RetrievedChunk(
                chunk_id=chunk_id,
                text=text or "",
                distance=float(distance),
                metadata=metadata or {},
            )
        )
    return passages


def _prefer_language_order(
    passages: list[RetrievedChunk],
    prefer_language: str | None,
) -> list[RetrievedChunk]:
    """Stable-sort so same-language passages appear first when preferred."""
    if not prefer_language or prefer_language not in CORPUS_LANG_CODES:
        return passages
    matching = [p for p in passages if p.language == prefer_language]
    others = [p for p in passages if p.language != prefer_language]
    return matching + others


def retrieve(
    query: str,
    top_k: int = RETRIEVAL_TOP_K,
    language: str | None = None,
    prefer_language: str | None = None,
    max_distance: float = MAX_COSINE_DISTANCE_TO_ANSWER,
) -> tuple[list[RetrievedChunk], bool]:
    """Return (ranked passages, is_grounded) for `query`.

    - `language`: hard filter (UI “retrieve from EN only / FR only”).
    - `prefer_language`: when the corpus has that language, try it first;
      fall back to the full index if the preferred hit is empty or too weak.
    """
    try:
        collection = get_or_create_collection()
        passage_count = collection.count()
    except Exception:
        logger.exception("Failed to open Chroma collection")
        return [], False

    if passage_count == 0:
        return [], False

    try:
        query_embedding = embed_query(query)
    except Exception:
        logger.exception("Query embedding failed for query=%r", query)
        return [], False

    # Hard language filter from the UI, no fallback.
    if language in CORPUS_LANG_CODES:
        try:
            passages = _query_collection(
                query_embedding, top_k, passage_count, language
            )
        except Exception:
            logger.exception("Chroma query failed for query=%r", query)
            return [], False
        if not passages:
            return [], False
        return passages, passages[0].distance <= max_distance

    preferred = prefer_language if prefer_language in CORPUS_LANG_CODES else None

    # Soft preference: use same-language docs when they ground well enough.
    if preferred is not None:
        try:
            preferred_passages = _query_collection(
                query_embedding, top_k, passage_count, preferred
            )
        except Exception:
            logger.exception("Preferred-language query failed for query=%r", query)
            preferred_passages = []

        if (
            preferred_passages
            and preferred_passages[0].distance <= max_distance
        ):
            return preferred_passages, True

    try:
        passages = _query_collection(
            query_embedding, top_k, passage_count, language=None
        )
    except Exception:
        logger.exception("Chroma query failed for query=%r", query)
        return [], False

    if not passages:
        return [], False

    passages = _prefer_language_order(passages, preferred)
    is_grounded = passages[0].distance <= max_distance
    return passages, is_grounded
