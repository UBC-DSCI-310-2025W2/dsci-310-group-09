import pandas as pd


def convert_boolean_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convert specified boolean columns in a dataframe to integers (0/1).

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    columns : list[str]
        Names of columns to convert.

    Returns
    -------
    pd.DataFrame
        Copy of dataframe with specified columns converted to integers.

    Raises
    ------
    KeyError
        If any specified columns are missing.
    ValueError
        If a specified column is not boolean dtype.
    """
    result = df.copy()

    missing_cols = [col for col in columns if col not in result.columns]
    if missing_cols:
        raise KeyError(f"Columns not found in dataframe: {missing_cols}")

    for col in columns:
        if not pd.api.types.is_bool_dtype(result[col]):
            raise ValueError(f"Column '{col}' is not a boolean column.")
        result[col] = result[col].astype(int)

    return result