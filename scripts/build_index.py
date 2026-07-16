"""Build or rebuild the Chroma index from sample and raw documents."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import PROCESSED_DIR
from src.ingest.chunk import chunk_documents
from src.ingest.load_docs import load_corpus
from src.retrieve.store import collection_count, reset_collection, upsert_chunks

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Load corpus, chunk, embed, upsert into Chroma, write index metadata."""
    logger.info("Building multilingual WHO guidance index")
    documents = load_corpus(prefer_raw=True)
    if not documents:
        raise SystemExit("No documents found in data/sample or data/raw.")

    logger.info("Loaded %s documents", len(documents))
    for document in documents:
        logger.info("  %s [%s] %s", document.doc_id, document.language, document.title)

    passages = chunk_documents(documents)
    logger.info("Created %s passages", len(passages))

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
    try:
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Failed writing {metadata_path}: {exc}") from exc

    logger.info(
        "Upserted %s passages. Collection count=%s. Wrote %s",
        upserted_count,
        collection_count(),
        metadata_path,
    )


if __name__ == "__main__":
    main()
