"""Retrieval metrics for portfolio reporting: Precision@k and MRR."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class QueryJudgement:
    """One labeled query used to score retrieval quality."""

    query_id: str
    query: str
    relevant_ids: list[str]
    language_filter: str | None = None


def _is_hit(retrieved_id: str, relevant_ids: list[str]) -> bool:
    """Return True if `retrieved_id` matches a relevant id or doc prefix."""
    for relevant_id in relevant_ids:
        if retrieved_id == relevant_id or retrieved_id.startswith(relevant_id):
            return True
    return False


def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int,
) -> float:
    """Fraction of the top-k retrieved ids that are relevant."""
    top_ids = retrieved_ids[:k]
    if not top_ids:
        return 0.0
    hit_count = sum(1 for retrieved_id in top_ids if _is_hit(retrieved_id, relevant_ids))
    return hit_count / k


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    """Reciprocal rank of the first relevant hit (0 if none)."""
    for rank, retrieved_id in enumerate(retrieved_ids, start=1):
        if _is_hit(retrieved_id, relevant_ids):
            return 1.0 / rank
    return 0.0


def evaluate_retrieval(
    judgements: list[QueryJudgement],
    retrieve_fn: Callable[[str, str | None], list[str]],
    k: int = 5,
) -> dict:
    """Aggregate Precision@k and MRR across a golden query set."""
    precision_scores: list[float] = []
    reciprocal_ranks: list[float] = []
    per_query_rows: list[dict] = []

    for judgement in judgements:
        retrieved_ids = retrieve_fn(judgement.query, judgement.language_filter)
        precision = precision_at_k(retrieved_ids, judgement.relevant_ids, k)
        rr = reciprocal_rank(retrieved_ids, judgement.relevant_ids)
        precision_scores.append(precision)
        reciprocal_ranks.append(rr)
        per_query_rows.append(
            {
                "query_id": judgement.query_id,
                "query": judgement.query,
                f"precision@{k}": round(precision, 3),
                "reciprocal_rank": round(rr, 3),
                "retrieved": retrieved_ids[:k],
            }
        )

    query_count = max(len(judgements), 1)
    return {
        f"precision@{k}": round(sum(precision_scores) / query_count, 3),
        "mrr": round(sum(reciprocal_ranks) / query_count, 3),
        "n_queries": len(judgements),
        "per_query": per_query_rows,
    }
