from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import pytest

from src.create_feat_importance_plot import create_feat_importance_plot


# -------------------------
# Simple cases
# -------------------------

def test_create_plot_success():
    X, y = make_classification(n_samples=100, n_features = 10, random_state=42)
    X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
    y = pd.Series(y)

    model = RandomForestClassifier(random_state=42).fit(X, y)

    ax = create_feat_importance_plot(model, X, max_display=5)

    assert ax is not None


def test_create_plot_max_features_success():
    X, y = make_classification(n_samples=100, n_features = 10, random_state=42)
    X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
    y = pd.Series(y)

    model = RandomForestClassifier(random_state=42).fit(X, y)

    ax = create_feat_importance_plot(model, X, max_display=10)

    assert ax is not None


# -------------------------
# Edge cases
# -------------------------

def test_plot_wrong_model():
    X = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    model = LogisticRegression().fit(X, [0, 1]) # Has .coef_, not .feature_importances_
    
    with pytest.raises(TypeError, match="Model must have the attribute feature_importances_"):
        create_feat_importance_plot(model, X, max_display=2)


def test_max_display_greater_than_features():
    X = pd.DataFrame({
        'feat1': [10, 20, 30, 40],
        'feat2': [1, 2, 1, 3],
        'feat3': [0, 0.1, 0, 0.2]
    })
    
    y = pd.Series([0, 1, 0, 1])

    model = RandomForestClassifier(random_state=42).fit(X, y)

    with pytest.raises(ValueError, match="Max_display is out of range"):
        create_feat_importance_plot(model, X, max_display=4)


# -------------------------
# Error cases
# -------------------------

def test_insufficient_max_display():
    X = pd.DataFrame({
        'feat1': [10, 20, 30, 40],
        'feat2': [1, 2, 1, 3],
        'feat3': [0, 0.1, 0, 0.2]
    })
    
    y = pd.Series([0, 1, 0, 1])

    model = RandomForestClassifier(random_state=42).fit(X, y)

    with pytest.raises(ValueError, match="Max_display must have a value greater than zero"):
        create_feat_importance_plot(model, X, max_display=0)


def test_insufficient_features():
    X = pd.DataFrame({
        'feat1': [10, 20, 30, 40],
        'feat2': [1, 2, 1, 3],
        'feat3': [0, 0.1, 0, 0.2]
    })
    
    X_no_cols = pd.DataFrame(index=range(10)) 

    y = pd.Series([0, 1, 0, 1])

    model = RandomForestClassifier(random_state=42).fit(X, y)
    
    with pytest.raises(ValueError, match="X_train must have at least one column."):
        create_feat_importance_plot(model, X_no_cols, max_display=1)


def test_non_pandas_X_train():
    X = pd.DataFrame({
        'feat1': [10, 20, 30, 40],
        'feat2': [1, 2, 1, 3],
        'feat3': [0, 0.1, 0, 0.2]
    })
    
    X_np = np.random.rand(10, 2)
    y = pd.Series([0, 1, 0, 1])

    model = RandomForestClassifier(random_state=42).fit(X, y)
    
    with pytest.raises(TypeError, match="X_train must be a pandas DataFrame."):
        create_feat_importance_plot(model, X_np, max_display=1)

        
def test_non_integer_max_display():
    X = pd.DataFrame({
        'feat1': [10, 20, 30, 40],
        'feat2': [1, 2, 1, 3],
        'feat3': [0, 0.1, 0, 0.2]
    })
    
    y = pd.Series([0, 1, 0, 1])

    model = RandomForestClassifier(random_state=42).fit(X, y)

    with pytest.raises(TypeError, match="Max_display must be an integer."):
        create_feat_importance_plot(model, X, max_display="5")