import os
import click
import pandas as pd


@click.command()
@click.argument("input_path")
@click.argument("output_path")
def main(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.read_csv(input_path)
    df.to_csv(output_path, index=False)

    click.echo(f"Saved raw data to {output_path}")
    click.echo(f"Shape: {df.shape}")


if __name__ == "__main__":
    main()