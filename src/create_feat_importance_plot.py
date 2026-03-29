import matplotlib.pyplot as plt
import pandas as pd

def create_feat_importance_plot(model, X_train: pd.DataFrame, max_display: int) -> plt:
    """
    Returns a bar plot of feature importances of the input model.

    Parameters
    ----------
    model : Object
        A trained model that will be used to plot feature importances.
    X_train : pd.DataFrame
        Training data of X features. 
    max_display : int
        The number of features to show on the plot.

    Returns
    -------
    matplotlib.pyplot
        Bar plot of the feature importances in the model.

    Raises
    ------
    TypeError
        If the model is linear (contains no feature importance attribute).
        If X_train is not a dataframe.
        If max_display is not an integer.
    ValueError
        If X_train is empty or has less than one column.
        If max_display is less than one.
        If max_display is greater than the number of features available.
    """
    if hasattr(model, 'feature_importances_') == False:
        raise TypeError("Model must have the attribute feature_importances_")

    if not isinstance(X_train, pd.DataFrame):
        raise TypeError("X_train must be a pandas DataFrame.")

    if len(X_train.columns) < 1:
        raise ValueError("X_train must have at least one column.")

    if not isinstance(max_display, int):
        raise TypeError("Max_display must be an integer.")

    if max_display < 1:
        raise ValueError("Max_display must have a value greater than zero.")

    if max_display > len(X_train.columns):
        raise ValueError("Max_display is out of range of the features available.")

    # Create plot
    importances = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    ax = importances.head(max_display).plot(kind="barh")
    
    plt.gca().invert_yaxis()
    plt.title(f"Figure 2. Top {max_display} Important Features for Predicting Revenue")
    plt.xlabel("Importance")
    
    return ax