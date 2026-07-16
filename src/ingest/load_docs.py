"""Load WHO guidance documents from sample/ and optional raw/ folders.

WHO topic guidance is the v1 corpus (Geneva-relevant, bilingual, dense).
UNGA resolutions are a deliberate v2 candidate once retrieval metrics are stable.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from src.config import MIN_DOCUMENT_TEXT_CHARS, RAW_DIR, SAMPLE_DIR
from src.ingest.chunk import DocumentRecord

logger = logging.getLogger(__name__)


def _read_txt(path: Path) -> str:
    """Read a UTF-8 text file and return its contents."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OSError(f"Failed reading text document {path}") from exc


def _read_pdf(path: Path) -> str:
    """Extract and normalize text from a PDF path."""
    try:
        reader = PdfReader(str(path))
        pages = [(page.extract_text() or "") for page in reader.pages]
    except (OSError, PdfReadError) as exc:
        raise OSError(f"Failed reading PDF document {path}") from exc

    text = "\n".join(pages)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _meta_from_sidecar(path: Path) -> dict[str, Any]:
    """Load sidecar metadata JSON, or infer defaults from the filename."""
    sidecar = path.with_suffix(path.suffix + ".meta.json")
    if not sidecar.exists():
        stem = path.stem
        language = "fr" if stem.endswith("_fr") or stem.endswith("-fr") else "en"
        return {
            "doc_id": stem,
            "title": stem.replace("_", " ").title(),
            "language": language,
            "source_url": "",
            "organization": "WHO",
        }
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid metadata sidecar for {path}") from exc


def load_documents_from_dir(directory: Path) -> list[DocumentRecord]:
    """Load `.txt` / `.pdf` documents (plus sidecars) from `directory`."""
    if not directory.exists():
        return []

    documents: list[DocumentRecord] = []
    for path in sorted(directory.iterdir()):
        if path.name.startswith("."):
            continue
        suffix = path.suffix.lower()
        try:
            if suffix == ".txt":
                text = _read_txt(path)
            elif suffix == ".pdf":
                text = _read_pdf(path)
            else:
                continue
        except OSError:
            logger.exception("Skipping unreadable document %s", path)
            continue

        if len(text.strip()) < MIN_DOCUMENT_TEXT_CHARS:
            logger.warning("Skipping short document %s (%s chars)", path, len(text))
            continue

        try:
            metadata = _meta_from_sidecar(path)
        except ValueError:
            logger.exception("Skipping document with bad sidecar %s", path)
            continue

        documents.append(
            DocumentRecord(
                doc_id=metadata["doc_id"],
                title=metadata["title"],
                language=metadata["language"],
                source_url=metadata.get("source_url", ""),
                text=text,
                organization=metadata.get("organization", "WHO"),
            )
        )
    return documents


def load_corpus(prefer_raw: bool = True) -> list[DocumentRecord]:
    """Load raw downloads when present, then fill gaps from sample documents."""
    documents: list[DocumentRecord] = []
    if prefer_raw:
        documents.extend(load_documents_from_dir(RAW_DIR))
    if not documents:
        documents.extend(load_documents_from_dir(SAMPLE_DIR))
        return documents

    existing_ids = {document.doc_id for document in documents}
    for sample_document in load_documents_from_dir(SAMPLE_DIR):
        if sample_document.doc_id not in existing_ids:
            documents.append(sample_document)
    return documents
