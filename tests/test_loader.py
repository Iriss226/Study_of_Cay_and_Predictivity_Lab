"""Tests for data loader utilities."""

import numpy as np
import pandas as pd
import pytest

from cay_lab.data.loader import make_synthetic_dataset, log_transform, COL_C, COL_A, COL_Y


def test_synthetic_dataset_shape():
    df = make_synthetic_dataset(n_periods=100)
    assert df.shape == (100, 4)
    assert list(df.columns) == ["c", "a", "y", "er"]


def test_synthetic_dataset_no_nan():
    df = make_synthetic_dataset(n_periods=80)
    assert not df.isnull().any().any()


def test_synthetic_dataset_index_type():
    df = make_synthetic_dataset(n_periods=50)
    assert isinstance(df.index, pd.PeriodIndex)


def test_synthetic_dataset_seed_reproducibility():
    df1 = make_synthetic_dataset(seed=7)
    df2 = make_synthetic_dataset(seed=7)
    pd.testing.assert_frame_equal(df1, df2)


def test_log_transform_applies_log():
    df = make_synthetic_dataset(n_periods=40)
    # Shift to positive before log
    df["c"] = df["c"] - df["c"].min() + 1
    df["a"] = df["a"] - df["a"].min() + 1
    df["y"] = df["y"] - df["y"].min() + 1
    out = log_transform(df, cols=["c"])
    assert np.allclose(out["c"], np.log(df["c"]))
    # Other columns unchanged
    pd.testing.assert_series_equal(out["a"], df["a"])
