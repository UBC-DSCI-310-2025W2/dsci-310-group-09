import pandas as pd

def calculate_class_balance(
    df: pd.DataFrame,
    target_col: str = "Revenue"
) -> pd.DataFrame:
    """
    Calculate class proportions and counts for a target column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    target_col : str, default="Revenue"
        Name of the target column.

    Returns
    -------
    pd.DataFrame
        Dataframe containing the target class, proportion, and count,
        sorted by target class value.

    Raises
    ------
    TypeError
        If df is not a pandas DataFrame or target_col is not a string.
    KeyError
        If target_col is not in the dataframe.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

    if not isinstance(target_col, str):
        raise TypeError("target_col must be a string.")

    if target_col not in df.columns:
        raise KeyError(f"Column '{target_col}' not found in dataframe.")

    counts = df[target_col].value_counts().sort_index()
    proportions = df[target_col].value_counts(normalize=True).sort_index()

    class_balance = pd.DataFrame({
        target_col: counts.index,
        "proportion": proportions.values,
        "count": counts.values
    })

    return class_balance