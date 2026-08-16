"""Data loading and pre-processing utilities.

Provides helpers to:
- Load raw quarterly series (consumption, asset wealth, labour income,
  excess stock returns) from CSV or pandas DataFrames.
- Apply standard log-transformations and de-trending.
- Generate a synthetic dataset for testing / demonstration.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Column name constants (used across the whole package)
# ---------------------------------------------------------------------------
COL_C = "c"       # log real consumption per capita
COL_A = "a"       # log real household net worth per capita
COL_Y = "y"       # log real labour income per capita
COL_ER = "er"     # excess log stock return (e.g., annual or quarterly)


def load_from_csv(path: str, date_col: str = "date", **kwargs) -> pd.DataFrame:
    """Load a CSV file and return a DataFrame indexed by a DatetimeIndex.

    Parameters
    ----------
    path:
        Path to the CSV file.
    date_col:
        Name of the column containing dates.
    **kwargs:
        Additional keyword arguments forwarded to :func:`pandas.read_csv`.

    Returns
    -------
    pd.DataFrame
        DataFrame with a :class:`pandas.DatetimeIndex`.
    """
    df = pd.read_csv(path, **kwargs)
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).sort_index()
    return df


def log_transform(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    """Return a copy of *df* with the specified columns log-transformed.

    Parameters
    ----------
    df:
        Input DataFrame.
    cols:
        Columns to transform.  If *None*, transforms ``[COL_C, COL_A, COL_Y]``.

    Returns
    -------
    pd.DataFrame
    """
    if cols is None:
        cols = [COL_C, COL_A, COL_Y]
    out = df.copy()
    for col in cols:
        if col in out.columns:
            out[col] = np.log(out[col])
    return out


def make_synthetic_dataset(
    n_periods: int = 200,
    seed: int = 42,
    start: str = "1970Q1",
) -> pd.DataFrame:
    """Generate a synthetic quarterly dataset suitable for testing.

    The series are constructed so that (c, a, y) share a cointegrating
    vector (i.e. cay is stationary) and excess returns are partly
    predictable by the true cay.

    Parameters
    ----------
    n_periods:
        Number of quarterly observations.
    seed:
        Random seed for reproducibility.
    start:
        Start period label (Pandas period string).

    Returns
    -------
    pd.DataFrame
        Columns: ``c``, ``a``, ``y``, ``er``.
        Index: :class:`pandas.PeriodIndex` with quarterly frequency.
    """
    rng = np.random.default_rng(seed)
    index = pd.period_range(start=start, periods=n_periods, freq="Q")

    # Common stochastic trend
    trend = np.cumsum(rng.normal(0, 1, n_periods))

    # Cointegrated levels: c ≈ 0.3*a + 0.6*y + small_noise
    a = trend + np.cumsum(rng.normal(0, 0.5, n_periods))
    y = trend + np.cumsum(rng.normal(0, 0.5, n_periods))
    cay_true = rng.normal(0, 0.5, n_periods)  # stationary cay
    c = 0.3 * a + 0.6 * y + cay_true

    # Excess returns: partially predicted by cay
    noise = rng.normal(0, 2, n_periods)
    er = 1.5 * cay_true + noise

    df = pd.DataFrame(
        {"c": c, "a": a, "y": y, "er": er},
        index=index,
    )
    return df
