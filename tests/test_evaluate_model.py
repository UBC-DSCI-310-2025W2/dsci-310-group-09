import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from src.evaluate_model import evaluate_model

# -------------------------
# Simple cases
# -------------------------

def test_evaluate_model_returns_dataframe():
    X, y = make_classification(n_samples=100, n_features=5, random_state=42)
    X = pd.DataFrame(X)
    y = pd.Series(y)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    
    result = evaluate_model(model, X, y)
    
    assert isinstance(result, pd.DataFrame)

def test_evaluate_model_contains_expected_rows():
    X, y = make_classification(n_samples=100, n_features=5, random_state=42)
    X = pd.DataFrame(X)
    y = pd.Series(y)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    result = evaluate_model(model, X, y)
    
    assert "0" in result.index
    assert "1" in result.index
    assert "accuracy" in result.index
    assert "roc_auc" in result.index

def test_roc_auc_within_valid_range():
    X, y = make_classification(n_samples=100, n_features=5, random_state=42)
    X = pd.DataFrame(X)
    y = pd.Series(y)

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    result = evaluate_model(model, X, y)

    roc_auc = result.loc["roc_auc", "roc_auc"]

    assert 0.0 <= roc_auc <= 1.0


# -------------------------
# Edge cases
# -------------------------

def test_perfect_predictions_give_auc_1():
    df = pd.DataFrame({
        "feature": [0, 0, 1, 1]
    })
    y = pd.Series([0, 0, 1, 1])

    model = RandomForestClassifier(random_state=42)
    model.fit(df, y)

    result = evaluate_model(model, df, y)

    assert result.loc["roc_auc", "roc_auc"] == 1.0


def test_small_dataset_runs_successfully():
    df = pd.DataFrame({
        "feature": [0, 1]
    })
    y = pd.Series([0, 1])

    model = RandomForestClassifier(random_state=42)
    model.fit(df, y)

    result = evaluate_model(model, df, y)

    assert not result.empty


# -------------------------
# Error cases
# -------------------------

def test_raises_typeerror_for_non_dataframe_X():
    X = [[1, 2], [3, 4]]
    y = pd.Series([0, 1])

    model = RandomForestClassifier().fit(pd.DataFrame(X), y)

    with pytest.raises(TypeError, match="X_test must be a pandas DataFrame"):
        evaluate_model(model, X, y)


def test_raises_valueerror_for_mismatched_lengths():
    X = pd.DataFrame({"a": [1, 2, 3]})
    y = pd.Series([0, 1])  # mismatch

    model = RandomForestClassifier().fit(X, [0, 1, 0])

    with pytest.raises(ValueError, match="same length"):
        evaluate_model(model, X, y)


def test_raises_typeerror_for_invalid_model():
    X = pd.DataFrame({"a": [1, 2, 3]})
    y = pd.Series([0, 1, 0])

    with pytest.raises(TypeError, match="predict"):
        evaluate_model("not_a_model", X, y)

def test_output_is_not_modified_input():
    X, y = make_classification(n_samples=50, n_features=3, n_informative=2, n_redundant=0, random_state=42)
    X = pd.DataFrame(X)
    y = pd.Series(y)

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    X_copy = X.copy()

    evaluate_model(model, X, y)

    assert X.equals(X_copy)