"""Split WHO guidance documents into overlapping retrieval passages."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_OVERLAP_CHARS, CHUNK_SEPARATORS, CHUNK_SIZE_CHARS


@dataclass
class DocumentRecord:
    """A full source document before chunking."""

    doc_id: str
    title: str
    language: str  # en | fr
    source_url: str
    text: str
    organization: str = "WHO"


@dataclass
class ChunkRecord:
    """One retrieval passage with citation metadata."""

    chunk_id: str
    doc_id: str
    title: str
    language: str
    source_url: str
    organization: str
    text: str
    chunk_index: int

    def to_metadata(self) -> dict[str, Any]:
        """Return Chroma metadata without the passage text body."""
        metadata = asdict(self)
        metadata.pop("text")
        return metadata


def make_splitter(
    chunk_size: int = CHUNK_SIZE_CHARS,
    chunk_overlap: int = CHUNK_OVERLAP_CHARS,
) -> RecursiveCharacterTextSplitter:
    """Build the recursive character splitter used at ingest time."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=CHUNK_SEPARATORS,
        length_function=len,
    )


def chunk_documents(documents: list[DocumentRecord]) -> list[ChunkRecord]:
    """Split each document into overlapping ChunkRecord passages."""
    splitter = make_splitter()
    passages: list[ChunkRecord] = []
    for document in documents:
        pieces = splitter.split_text(document.text.strip())
        for chunk_index, piece in enumerate(pieces):
            if not piece.strip():
                continue
            passages.append(
                ChunkRecord(
                    chunk_id=f"{document.doc_id}::c{chunk_index:04d}",
                    doc_id=document.doc_id,
                    title=document.title,
                    language=document.language,
                    source_url=document.source_url,
                    organization=document.organization,
                    text=piece.strip(),
                    chunk_index=chunk_index,
                )
            )
    return passages
