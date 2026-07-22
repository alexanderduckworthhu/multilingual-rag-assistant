"""Build the Chroma index from the local corpus when it is missing."""

from __future__ import annotations

import json
import logging

from src.config import PROCESSED_DIR
from src.ingest.chunk import chunk_documents
from src.ingest.load_docs import load_corpus
from src.retrieve.store import collection_count, reset_collection, upsert_chunks

logger = logging.getLogger(__name__)


def build_index(*, prefer_raw: bool = True) -> int:
    """Rebuild the vector index from sample/raw docs; return passage count."""
    documents = load_corpus(prefer_raw=prefer_raw)
    if not documents:
        raise FileNotFoundError("No documents found in data/sample or data/raw.")

    passages = chunk_documents(documents)
    reset_collection()
    upserted_count = upsert_chunks(passages)

    metadata = {
        "n_documents": len(documents),
        "n_chunks": upserted_count,
        "languages": sorted({document.language for document in documents}),
        "doc_ids": [document.doc_id for document in documents],
    }
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    metadata_path = PROCESSED_DIR / "index_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    logger.info("Built index with %s passages (%s)", upserted_count, metadata_path)
    return upserted_count


def ensure_index() -> int:
    """Return indexed passage count, building the index first if it is empty."""
    try:
        count = collection_count()
    except Exception:
        logger.exception("Could not read collection count; rebuilding index")
        count = 0

    if count > 0:
        return count

    logger.info("Index empty — building from bundled sample corpus")
    return build_index(prefer_raw=True)
