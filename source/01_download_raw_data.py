import io
import zipfile
import requests
import pandas as pd


def main():
    url = "https://cdn.uci-ics-mlr-prod.aws.uci.edu/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset.zip"

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        print("Files in zip:", z.namelist())

        with z.open("online_shoppers_intention.csv") as f:
            df = pd.read_csv(f)

    df.to_csv("data/raw_online_shoppers.csv", index=False)
    print("Saved to data/raw_online_shoppers.csv")


if __name__ == "__main__":
    main()