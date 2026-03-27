import os
import click
import pandas as pd

from src.convert_boolean_values import convert_boolean_columns
from src.calculate_class_balance import calculate_class_balance


@click.command()
@click.argument("input_path")
@click.argument("output_path")
def main(input_path, output_path):
    df = pd.read_csv(input_path)

    online = df.copy()

    # Convert boolean columns to integers
    online = convert_boolean_columns(online, ["Weekend", "Revenue"])

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

    # Save class balance table to results/
    class_balance = calculate_class_balance(online, "Revenue")
    class_balance_path = "results/online_shoppers_class_balance.csv"
    class_balance.to_csv(class_balance_path, index=False)

    click.echo(f"Saved processed data to {output_path}")
    click.echo(f"Saved class balance table to {class_balance_path}")
    click.echo(f"Processed shape: {online.shape}")


if __name__ == "__main__":
    main()