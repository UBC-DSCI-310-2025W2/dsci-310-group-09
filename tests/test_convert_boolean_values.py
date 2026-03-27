import pandas as pd
import pytest

from src.convert_boolean_values import convert_boolean_columns


# -------------------------
# Simple cases
# -------------------------

def test_convert_single_boolean_column():
    df = pd.DataFrame({
        "Weekend": [True, False, True]
    })

    result = convert_boolean_columns(df, ["Weekend"])

    assert result["Weekend"].tolist() == [1, 0, 1]


def test_convert_multiple_boolean_columns():
    df = pd.DataFrame({
        "Weekend": [True, False, True],
        "Revenue": [False, True, False]
    })

    result = convert_boolean_columns(df, ["Weekend", "Revenue"])

    assert result["Weekend"].tolist() == [1, 0, 1]
    assert result["Revenue"].tolist() == [0, 1, 0]


def test_non_target_columns_remain_unchanged():
    df = pd.DataFrame({
        "Weekend": [True, False],
        "Revenue": [False, True],
        "Month": ["Feb", "Mar"]
    })

    result = convert_boolean_columns(df, ["Weekend", "Revenue"])

    assert result["Month"].tolist() == ["Feb", "Mar"]


# -------------------------
# Edge cases
# -------------------------

def test_returns_copy_and_does_not_modify_original():
    df = pd.DataFrame({
        "Weekend": [True, False],
        "Revenue": [False, True]
    })

    result = convert_boolean_columns(df, ["Weekend"])

    assert df["Weekend"].dtype == bool
    assert result["Weekend"].tolist() == [1, 0]


def test_empty_column_list_returns_unchanged_copy():
    df = pd.DataFrame({
        "Weekend": [True, False],
        "Revenue": [False, True]
    })

    result = convert_boolean_columns(df, [])

    assert result.equals(df)
    assert result is not df


def test_empty_dataframe_with_boolean_columns():
    df = pd.DataFrame({
        "Weekend": pd.Series(dtype="bool"),
        "Revenue": pd.Series(dtype="bool")
    })

    result = convert_boolean_columns(df, ["Weekend", "Revenue"])

    assert result.empty
    assert str(result["Weekend"].dtype) in ["int64", "int32"]
    assert str(result["Revenue"].dtype) in ["int64", "int32"]


# -------------------------
# Error cases
# -------------------------

def test_raises_keyerror_for_missing_column():
    df = pd.DataFrame({
        "Weekend": [True, False]
    })

    with pytest.raises(KeyError, match="Columns not found"):
        convert_boolean_columns(df, ["Revenue"])


def test_raises_valueerror_for_non_boolean_column():
    df = pd.DataFrame({
        "Weekend": [1, 0, 1]
    })

    with pytest.raises(ValueError, match="not a boolean column"):
        convert_boolean_columns(df, ["Weekend"])


def test_raises_valueerror_when_one_of_multiple_columns_is_not_boolean():
    df = pd.DataFrame({
        "Weekend": [True, False],
        "Revenue": [1, 0]
    })

    with pytest.raises(ValueError, match="not a boolean column"):
        convert_boolean_columns(df, ["Weekend", "Revenue"])