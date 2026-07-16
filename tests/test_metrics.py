from src.eval.metrics import precision_at_k, reciprocal_rank


def test_precision_at_k():
    retrieved = ["a::c0000", "b::c0001", "c::c0002"]
    relevant = ["a"]
    assert precision_at_k(retrieved, relevant, k=3) == 1 / 3


def test_mrr_first_rank():
    assert reciprocal_rank(["hit::c0", "x"], ["hit"]) == 1.0
    assert reciprocal_rank(["x", "hit::c0"], ["hit"]) == 0.5
    assert reciprocal_rank(["x", "y"], ["hit"]) == 0.0
