"""Tests for CayBuilder (DOLS cointegration)."""

import numpy as np
import pytest

from cay_lab.data.loader import make_synthetic_dataset
from cay_lab.analysis.cay_builder import CayBuilder


@pytest.fixture
def df():
    return make_synthetic_dataset(n_periods=120, seed=0)


def test_fit_returns_self(df):
    builder = CayBuilder(df, lags=0)
    assert builder.fit() is builder


def test_cay_is_series(df):
    builder = CayBuilder(df, lags=0).fit()
    import pandas as pd
    assert isinstance(builder.cay, pd.Series)


def test_cay_length(df):
    builder = CayBuilder(df, lags=0).fit()
    # cay should cover the full df length
    assert len(builder.cay) == len(df)


def test_coef_keys(df):
    builder = CayBuilder(df, lags=1).fit()
    assert set(builder.coef_.keys()) == {"const", "beta_a", "beta_y"}


def test_cay_is_stationary_mean_near_zero(df):
    """The cay residual should have mean close to zero (it's a de-meaned residual)."""
    builder = CayBuilder(df, lags=0).fit()
    assert abs(builder.cay.mean()) < 0.5


def test_missing_columns_raises():
    import pandas as pd
    bad_df = pd.DataFrame({"c": [1, 2], "a": [1, 2]})  # missing 'y'
    with pytest.raises(ValueError, match="missing columns"):
        CayBuilder(bad_df)


def test_summary_string(df):
    builder = CayBuilder(df, lags=0).fit()
    s = builder.summary()
    assert "beta_a" in s
    assert "beta_y" in s


def test_dols_lags(df):
    builder = CayBuilder(df, lags=2).fit()
    assert builder.coef_ is not None
