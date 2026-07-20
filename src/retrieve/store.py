"""Chroma persistence for the shared EN/FR WHO guidance collection."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import chromadb
from chromadb.config import Settings

from src.config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_UPSERT_BATCH_SIZE
from src.ingest.chunk import ChunkRecord
from src.ingest.embed import embed_passages

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
logging.getLogger("chromadb").setLevel(logging.ERROR)
logging.getLogger("posthog").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


def get_client(persist_dir: Path | None = None) -> chromadb.PersistentClient:
    """Return a persistent Chroma client rooted at `persist_dir`."""
    path = str(persist_dir or CHROMA_DIR)
    Path(path).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=path,
        settings=Settings(anonymized_telemetry=False),
    )


def get_or_create_collection(
    client: chromadb.PersistentClient | None = None,
) -> chromadb.Collection:
    """Return the WHO guidance collection, creating it if needed."""
    chroma_client = client or get_client()
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def reset_collection(client: chromadb.PersistentClient | None = None) -> None:
    """Delete and recreate the collection so rebuilds start clean."""
    chroma_client = client or get_client()
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except ValueError:
        # Collection missing, safe to create fresh.
        pass
    except Exception:
        logger.exception("Unexpected error deleting collection %s", COLLECTION_NAME)
        raise
    get_or_create_collection(chroma_client)


def upsert_chunks(
    chunks: list[ChunkRecord],
    batch_size: int = EMBEDDING_UPSERT_BATCH_SIZE,
    client: chromadb.PersistentClient | None = None,
) -> int:
    """Embed and upsert `chunks`; return the number of passages written."""
    collection = get_or_create_collection(client)
    total_upserted = 0
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        documents = [chunk.text for chunk in batch]
        try:
            embeddings = embed_passages(documents)
            collection.upsert(
                ids=[chunk.chunk_id for chunk in batch],
                documents=documents,
                metadatas=[chunk.to_metadata() for chunk in batch],
                embeddings=embeddings,
            )
        except Exception:
            logger.exception("Failed upserting batch starting at %s", start)
            raise
        total_upserted += len(batch)
    return total_upserted


def collection_count(client: chromadb.PersistentClient | None = None) -> int:
    """Return how many passages are currently indexed."""
    return int(get_or_create_collection(client).count())
