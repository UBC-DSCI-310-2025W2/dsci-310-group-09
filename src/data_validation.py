import numpy as np
import pandas as pd

EXPECTED_RAW_COLUMNS = [
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "PageValues",
    "SpecialDay",
    "Month",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
    "VisitorType",
    "Weekend",
    "Revenue",
]

NUMERIC_RAW_COLUMNS = [
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "PageValues",
    "SpecialDay",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
]

CATEGORICAL_RAW_COLUMNS = ["Month", "VisitorType"]
BOOLEAN_LIKE_COLUMNS = ["Weekend", "Revenue"]

NON_NEGATIVE_COLUMNS = [
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "PageValues",
]

UNIT_INTERVAL_COLUMNS = ["BounceRates", "ExitRates", "SpecialDay"]

ALLOWED_MONTHS = {
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "June",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
}

ALLOWED_VISITOR_TYPES = {
    "Returning_Visitor",
    "New_Visitor",
    "Other",
}

BOOLEAN_VALUE_MAP = {
    True: 1,
    False: 0,
    1: 1,
    0: 0,
    "TRUE": 1,
    "FALSE": 0,
    "True": 1,
    "False": 0,
    "true": 1,
    "false": 0,
}

def _normalize_boolean_like_values(series: pd.Series, column_name: str) -> set:
    """
    Convert boolean-like values to {0, 1} for validation.
    Raises ValueError if unexpected values are present.
    """
    unique_values = set(series.dropna().unique())
    normalized_values = set()

    for value in unique_values:
        if value not in BOOLEAN_VALUE_MAP:
            raise ValueError(
                f"Column '{column_name}' contains invalid boolean-like values: {unique_values}"
            )
        normalized_values.add(BOOLEAN_VALUE_MAP[value])

    return normalized_values

def validate_raw_online_shoppers_data(
    df: pd.DataFrame,
    input_path: str,
    missing_threshold: float = 0.0,
) -> None:
    """
    Run validation checks on the raw online shoppers dataset.
    Stops the pipeline immediately if any check fails.
    """
    # 1. Correct file format
    if not input_path.lower().endswith(".csv"):
        raise ValueError("Input file must be a CSV file.")

    if df.empty:
        raise ValueError("Raw dataset is empty.")

    # Treat blank strings as missing
    validated_df = df.replace(r"^\s*$", pd.NA, regex=True)

    # 2. Correct column names
    missing_columns = [col for col in EXPECTED_RAW_COLUMNS if col not in validated_df.columns]
    extra_columns = [col for col in validated_df.columns if col not in EXPECTED_RAW_COLUMNS]

    if missing_columns or extra_columns:
        raise ValueError(
            f"Column validation failed. Missing columns: {missing_columns}. "
            f"Unexpected columns: {extra_columns}."
        )

    # 3. No empty observations
    if validated_df.isna().all(axis=1).any():
        raise ValueError("Dataset contains one or more completely empty observations.")

    # 4. Missingness not beyond expected threshold
    missing_fraction = validated_df.isna().mean()
    too_missing = missing_fraction[missing_fraction > missing_threshold]
    if not too_missing.empty:
        raise ValueError(
            "Missingness exceeds the allowed threshold. "
            f"Columns above threshold: {too_missing.to_dict()}"
        )

    # 5. Correct data types in each column
    for col in NUMERIC_RAW_COLUMNS:
        if not pd.api.types.is_numeric_dtype(validated_df[col]):
            raise TypeError(f"Column '{col}' must be numeric.")

    for col in CATEGORICAL_RAW_COLUMNS:
        if not (
            pd.api.types.is_object_dtype(validated_df[col])
            or str(validated_df[col].dtype) == "category"
        ):
            raise TypeError(f"Column '{col}' must be a string/category column.")

    for col in BOOLEAN_LIKE_COLUMNS:
        _normalize_boolean_like_values(validated_df[col], col)

        # 6. No duplicate observations
    duplicate_count = validated_df.duplicated().sum()
    if duplicate_count > 0:
        print(
            f"Validation warning: dataset contains {duplicate_count} duplicate "
            "observations. They will be removed during cleaning."
        )

    # 7. Correct category levels
    month_values = set(validated_df["Month"].dropna().astype(str).str.strip().unique())
    invalid_months = month_values - ALLOWED_MONTHS
    if invalid_months:
        raise ValueError(f"Invalid Month values found: {invalid_months}")

    visitor_values = set(validated_df["VisitorType"].dropna().astype(str).str.strip().unique())
    invalid_visitor_types = visitor_values - ALLOWED_VISITOR_TYPES
    if invalid_visitor_types:
        raise ValueError(f"Invalid VisitorType values found: {invalid_visitor_types}")

    # 8. No outlier or anomalous values
    for col in NON_NEGATIVE_COLUMNS:
        if (validated_df[col] < 0).any():
            raise ValueError(f"Column '{col}' contains negative values.")

    for col in UNIT_INTERVAL_COLUMNS:
        if ((validated_df[col] < 0) | (validated_df[col] > 1)).any():
            raise ValueError(f"Column '{col}' contains values outside [0, 1].")

    # 9. Target/response variable follows expected distribution
    revenue_values = _normalize_boolean_like_values(validated_df["Revenue"], "Revenue")
    if revenue_values != {0, 1}:
        raise ValueError(
            "Revenue must contain both classes so classification remains meaningful."
        )
def validate_processed_online_shoppers_data(
    df: pd.DataFrame,
    input_path: str,
) -> None:
    """
    Validate the processed dataset before modelling.
    """
    if not input_path.lower().endswith(".csv"):
        raise ValueError("Processed input file must be a CSV file.")

    if df.empty:
        raise ValueError("Processed dataset is empty.")

    if "Revenue" not in df.columns:
        raise ValueError("Processed dataset must contain the target column 'Revenue'.")

    if df.isna().any().any():
        missing_summary = df.isna().sum()
        missing_cols = missing_summary[missing_summary > 0]
        raise ValueError(
            f"Processed dataset contains missing values: {missing_cols.to_dict()}"
        )

    non_numeric_predictors = [
        col for col in df.columns
        if col != "Revenue" and not pd.api.types.is_numeric_dtype(df[col])
    ]
    if non_numeric_predictors:
        raise TypeError(
            "All processed predictor columns must be numeric. "
            f"Non-numeric columns found: {non_numeric_predictors}"
        )

    revenue_values = set(df["Revenue"].dropna().unique())
    if not revenue_values.issubset({0, 1}):
        raise ValueError(
            f"Processed Revenue column must contain only 0/1 values. Found: {revenue_values}"
        )
    if revenue_values != {0, 1}:
        raise ValueError("Processed Revenue column must contain both classes 0 and 1.")

def validate_train_test_split(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> None:
    """
    Validate the train/test split without introducing leakage.
    """
    if X_train.empty or X_test.empty:
        raise ValueError("Train/test split failed because one split is empty.")

    if list(X_train.columns) != list(X_test.columns):
        raise ValueError("X_train and X_test do not have the same predictor columns.")

    overlap = set(X_train.index).intersection(set(X_test.index))
    if overlap:
        raise ValueError(
            f"Train/test leakage detected: {len(overlap)} overlapping observations found."
        )

    if X_train.isna().any().any() or X_test.isna().any().any():
        raise ValueError("Missing values found in X_train or X_test after splitting.")

    if y_train.isna().any() or y_test.isna().any():
        raise ValueError("Missing values found in y_train or y_test after splitting.")

    numeric_train = X_train.select_dtypes(include=[np.number, "bool"]).astype(float)
    numeric_test = X_test.select_dtypes(include=[np.number, "bool"]).astype(float)

    if np.isinf(numeric_train.to_numpy()).any() or np.isinf(numeric_test.to_numpy()).any():
        raise ValueError("Infinite values found in X_train or X_test.")

    train_classes = set(pd.Series(y_train).unique())
    test_classes = set(pd.Series(y_test).unique())

    if train_classes != {0, 1}:
        raise ValueError(f"y_train must contain both classes 0 and 1. Found: {train_classes}")

    if test_classes != {0, 1}:
        raise ValueError(f"y_test must contain both classes 0 and 1. Found: {test_classes}")
