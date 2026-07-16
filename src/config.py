"""Locked architectural choices for the multilingual WHO guidance QA demo.

Change one knob at a time, rebuild the index, and re-run eval to see impact.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EVAL_DIR = DATA_DIR / "eval"
CHROMA_DIR = PROCESSED_DIR / "chroma"

COLLECTION_NAME = "who_guidance_en_fr"

# multilingual-e5-small: shared EN/FR vector space, laptop-friendly, free.
# Alternative considered: OpenAI text-embedding-3-small (stronger jargon, paid, online).
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
EMBEDDING_QUERY_PREFIX = "query: "
EMBEDDING_PASSAGE_PREFIX = "passage: "

# Recursive character split with overlap reduces answers cut at chunk boundaries.
# Alternative considered: semantic/LLM chunking (cleaner cuts, harder to debug).
CHUNK_SIZE_CHARS = 800
CHUNK_OVERLAP_CHARS = 120
CHUNK_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

# Chroma local persist: metadata filters, no Docker. Alternatives: FAISS, Pinecone.
RETRIEVAL_TOP_K = 5
# Cosine distance in Chroma (lower = closer). Above this → refuse generation.
MAX_COSINE_DISTANCE_TO_ANSWER = 0.55

# gpt-4o-mini: cheap citation following. Fallback: extractive passages if no API key.
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.0
EXTRACTIVE_PASSAGE_COUNT = 3

QUESTION_MIN_CHARS = 3
QUESTION_TEXT_AREA_HEIGHT_PX = 120
MIN_DOCUMENT_TEXT_CHARS = 40
EMBEDDING_UPSERT_BATCH_SIZE = 32
