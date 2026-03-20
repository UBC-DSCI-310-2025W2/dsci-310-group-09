import os
import click
import pandas as pd


@click.command()
@click.argument("input_path")
@click.argument("output_path")
def main(input_path, output_path):
    df = pd.read_csv(input_path)

    online = df.copy()

    # Convert boolean columns to integers
    online["Weekend"] = online["Weekend"].astype(int)
    online["Revenue"] = online["Revenue"].astype(int)

    # One-hot encode categorical variables
    online = pd.get_dummies(
        online,
        columns=["Month", "VisitorType"],
        drop_first=True
    )

    # Make sure output folders exist
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    os.makedirs("results", exist_ok=True)

    # Save processed data
    online.to_csv(output_path, index=False)

    # Save class imbalance table to results/
    class_balance = (
        online["Revenue"]
        .value_counts(normalize=True)
        .sort_index()
        .rename("proportion")
        .reset_index()
        .rename(columns={"index": "Revenue"})
    )

    class_counts = (
        online["Revenue"]
        .value_counts()
        .sort_index()
        .rename("count")
        .reset_index(drop=True)
    )

    class_balance["count"] = class_counts

    class_balance_path = "results/online_shoppers_class_balance.csv"
    class_balance.to_csv(class_balance_path, index=False)

    click.echo(f"Saved processed data to {output_path}")
    click.echo(f"Saved class balance table to {class_balance_path}")
    click.echo(f"Processed shape: {online.shape}")


if __name__ == "__main__":
    main()