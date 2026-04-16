"""Small helpers for tabulating exact QET energy ledgers."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from qet_bench.exact import qet_ledger

BenchmarkPoint = tuple[float, float]

BENCHMARK_POINTS: tuple[BenchmarkPoint, ...] = ((1.0, 0.5), (1.0, 1.0))


def ledger_row(h: float, k: float) -> dict[str, float]:
    """Return a single benchmark row with parameters and ledger entries."""
    row = {"h": float(h), "k": float(k)}
    row.update(qet_ledger(h=h, k=k))
    return row


def benchmark_ledgers(points: Iterable[BenchmarkPoint] = BENCHMARK_POINTS) -> pd.DataFrame:
    """Return exact ledgers for a sequence of ``(h, k)`` benchmark points."""
    return pd.DataFrame([ledger_row(h, k) for h, k in points])

