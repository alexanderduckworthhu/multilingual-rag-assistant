"""Build or rebuild the Chroma index from sample and raw documents."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.retrieve.ensure_index import build_index
from src.retrieve.store import collection_count

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Load corpus, chunk, embed, upsert into Chroma, write index metadata."""
    logger.info("Building multilingual WHO guidance index")
    try:
        upserted_count = build_index(prefer_raw=True)
    except FileNotFoundError as exc:
        raise SystemExit(str(exc)) from exc
    except OSError as exc:
        raise SystemExit(f"Failed writing index metadata: {exc}") from exc

    logger.info(
        "Upserted %s passages. Collection count=%s",
        upserted_count,
        collection_count(),
    )


if __name__ == "__main__":
    main()
