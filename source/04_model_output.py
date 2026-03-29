import os
import click
import shap
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

from src.evaluate_model import evaluate_model

@click.command()
@click.argument("input_path")
@click.argument("output_prefix")
def main(input_path, output_prefix):
    df = pd.read_csv(input_path)

    # Split predictors and target
    X = df.drop("Revenue", axis=1)
    y = df["Revenue"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train model
    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )
    rf.fit(X_train, y_train)

    # Predictions + evaluation using reusable function
    results = evaluate_model(rf, X_test, y_test)

    # Save classification report (remove roc_auc row)
    report_df = results.drop(index="roc_auc")
    report_df.to_csv(f"{output_prefix}_classification_report.csv", index=True)

    # Save ROC-AUC separately
    auc_value = results.loc["roc_auc", "roc_auc"]
    auc_df = pd.DataFrame({
    "metric": ["roc_auc"],
    "value": [auc_value]
})
    auc_df.to_csv(f"{output_prefix}_auc.csv", index=False)

    # Make sure output folder exists
    output_dir = os.path.dirname(output_prefix)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Save feature importance plot
    importances = pd.Series(
        rf.feature_importances_,
        index=X_train.columns
    ).sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    importances.head(10).plot(kind="barh")
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_feature_importance.png", bbox_inches="tight")
    plt.close()

    # Save SHAP summary plot
    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(X_test)

    if isinstance(shap_values, list):
        shap_values_class1 = shap_values[1]
    else:
        shap_values_class1 = shap_values[:, :, 1]

    plt.figure(figsize=(14, 9))
    shap.summary_plot(
        shap_values_class1,
        X_test,
        max_display=12,
        plot_size=(14, 9),
        show=False
    )
    plt.title("SHAP Summary Plot for Online Shopper Revenue Prediction", pad=15)
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_shap_summary.png", dpi=300, bbox_inches="tight")
    plt.close()

    click.echo(f"Saved report to {output_prefix}_classification_report.csv")
    click.echo(f"Saved AUC table to {output_prefix}_auc.csv")
    click.echo(f"Saved figure to {output_prefix}_feature_importance.png")
    click.echo(f"Saved figure to {output_prefix}_shap_summary.png")


if __name__ == "__main__":
    main()