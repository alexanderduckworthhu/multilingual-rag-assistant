"""Sentence-transformer embeddings with multilingual-e5 query/passage prefixes."""

from __future__ import annotations

import logging
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from src.config import (
    EMBEDDING_MODEL,
    EMBEDDING_PASSAGE_PREFIX,
    EMBEDDING_QUERY_PREFIX,
)

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load and cache the embedding model (downloads on first use)."""
    try:
        return SentenceTransformer(EMBEDDING_MODEL)
    except Exception:
        logger.exception("Failed to load embedding model %s", EMBEDDING_MODEL)
        raise


def embed_passages(texts: list[str]) -> list[list[float]]:
    """Embed document passages with the E5 `passage:` prefix."""
    model = get_embedding_model()
    prefixed = [f"{EMBEDDING_PASSAGE_PREFIX}{text}" for text in texts]
    try:
        vectors = model.encode(
            prefixed, normalize_embeddings=True, show_progress_bar=False
        )
    except Exception:
        logger.exception("Passage embedding failed for %s texts", len(texts))
        raise
    return [vector.tolist() for vector in vectors]


def embed_query(text: str) -> list[float]:
    """Embed a user query with the E5 `query:` prefix."""
    model = get_embedding_model()
    try:
        vector = model.encode(
            f"{EMBEDDING_QUERY_PREFIX}{text}",
            normalize_embeddings=True,
            show_progress_bar=False,
        )
    except Exception:
        logger.exception("Query embedding failed")
        raise
    return vector.tolist()
