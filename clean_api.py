import json
import logging

import polars as pl


def trim_record(record):
    fields = [
        "id",
        "cif",
        "name",
        "address",
        "short_description",
        "description",
        "email",
        "hidden",
        "inactive",
    ] + [f for f in record.keys() if f.endswith("_link")]

    new_record = {key: record[key] for key in fields}

    return new_record


def main():
    with open("api.json") as fh:
        data = json.load(fh)
        df = pl.from_records([trim_record(record) for record in data])

    df = df.filter(~pl.col("hidden") & ~pl.col("inactive")).select(
        pl.all().exclude(["hidden", "inactive"])
    )

    df.write_parquet("api.parquet")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
