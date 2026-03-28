import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.calculate_class_balance import calculate_class_balance


# -------------------------
# Simple cases
# -------------------------

def test_calculate_class_balance_balanced_classes():
    df = pd.DataFrame({
        "Revenue": [0, 1, 0, 1]
    })

    result = calculate_class_balance(df)

    expected = pd.DataFrame({
        "Revenue": [0, 1],
        "proportion": [0.5, 0.5],
        "count": [2, 2]
    })

    assert_frame_equal(result.reset_index(drop=True), expected)


def test_calculate_class_balance_unbalanced_classes():
    df = pd.DataFrame({
        "Revenue": [0, 0, 0, 1]
    })

    result = calculate_class_balance(df)

    expected = pd.DataFrame({
        "Revenue": [0, 1],
        "proportion": [0.75, 0.25],
        "count": [3, 1]
    })

    assert_frame_equal(result.reset_index(drop=True), expected)


# -------------------------
# Edge case
# -------------------------

def test_calculate_class_balance_single_class_only():
    df = pd.DataFrame({
        "Revenue": [1, 1, 1]
    })

    result = calculate_class_balance(df)

    expected = pd.DataFrame({
        "Revenue": [1],
        "proportion": [1.0],
        "count": [3]
    })

    assert_frame_equal(result.reset_index(drop=True), expected)


# -------------------------
# Error cases
# -------------------------

def test_calculate_class_balance_raises_keyerror_for_missing_column():
    df = pd.DataFrame({
        "Weekend": [0, 1, 0]
    })

    with pytest.raises(KeyError, match="not found in dataframe"):
        calculate_class_balance(df)


def test_calculate_class_balance_raises_typeerror_for_non_dataframe():
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        calculate_class_balance([0, 1, 0])