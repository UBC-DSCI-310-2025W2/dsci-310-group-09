import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score


def evaluate_model(
    model,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> pd.DataFrame:
    """
    Evaluate a trained classification and return performance metrics.

    Parameters
    ----------
    model : object
        A trained model with predict and predict_proba methods.
    X_test : pd.DataFrame
        Test feature data.
    y_test : pd.Series
        True labels for the test data.

    Returns
    ----------
    pd.DataFrame
        DataFrame containing evaluation metrics.

    Raises
    ----------
    TypeError
        If inputs are not of expected types or model lacks required methods.
    ValueError
        If X_test and y_test have mismatched lengths.
    """

    if not isinstance(X_test, pd.DataFrame):
        raise TypeError("X_test must be a pandas DataFrame.")

    if not isinstance(y_test, (pd.Series, pd.DataFrame)):
        raise TypeError("y_test must be a pandas Series or DataFrame.")

    if not hasattr(model, "predict") or not hasattr(model, "predict_proba"):
        raise TypeError("model must have predict and predict_proba methods.")

    if len(X_test) != len(y_test):
        raise ValueError("X_test and y_test must have the same length.")

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    report_dict = classification_report(y_test, y_pred, output_dict=True)

    report_df = pd.DataFrame(report_dict).transpose()

    roc_auc = roc_auc_score(y_test, y_prob)

    roc_row = pd.DataFrame({
        "precision": [None],
        "recall": [None],
        "f1-score": [None],
        "support": [None],
        "roc_auc": [roc_auc]
    }, index=["roc_auc"])

    result = pd.concat([report_df, roc_row], axis=0)

    return result