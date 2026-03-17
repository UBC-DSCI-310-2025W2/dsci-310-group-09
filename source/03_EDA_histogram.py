import os
import click
import pandas as pd
import matplotlib.pyplot as plt


@click.command()
@click.argument("input_path")
@click.argument("output_path")
def main(input_path, output_path):
    df = pd.read_csv(input_path)

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df.hist(figsize=(12, 10))
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    click.echo(f"Saved figure to {output_path}")


if __name__ == "__main__":
    main()