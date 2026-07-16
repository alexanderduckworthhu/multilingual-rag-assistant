"""Score retrieval with Precision@k and MRR on the golden query set."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import EVAL_DIR, PROCESSED_DIR, RETRIEVAL_TOP_K
from src.eval.metrics import QueryJudgement, evaluate_retrieval
from src.retrieve.search import retrieve

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Load golden queries, run retrieval, write eval_report.json."""
    golden_path = EVAL_DIR / "golden_queries.json"
    try:
        judgements_raw = json.loads(golden_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Failed reading golden set {golden_path}: {exc}") from exc

    judgements = [QueryJudgement(**row) for row in judgements_raw]

    def retrieve_fn(query: str, language: str | None) -> list[str]:
        passages, _ = retrieve(query=query, top_k=RETRIEVAL_TOP_K, language=language)
        return [passage.chunk_id for passage in passages]

    report = evaluate_retrieval(judgements, retrieve_fn, k=RETRIEVAL_TOP_K)
    out_path = PROCESSED_DIR / "eval_report.json"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    try:
        out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Failed writing {out_path}: {exc}") from exc

    logger.info("precision@%s: %s", RETRIEVAL_TOP_K, report[f"precision@{RETRIEVAL_TOP_K}"])
    logger.info("MRR: %s", report["mrr"])
    logger.info("n_queries: %s", report["n_queries"])
    logger.info("Wrote %s", out_path)


if __name__ == "__main__":
    main()
