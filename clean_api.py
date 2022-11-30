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
        "categories",
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

    with open("categories.json") as fh:
        data = json.load(fh)
        df_categories = pl.from_records(data)

    df = df.filter(~pl.col("hidden") & ~pl.col("inactive")).select(
        pl.all().exclude(["hidden", "inactive"])
    )
    category_pairings = (
        df.explode("categories")
        .select([pl.col("id"), pl.col("categories")])
        .join(
            df_categories.select(
                [pl.col("id").alias("category_id"), pl.col("name").alias("category")]
            ),
            left_on="categories",
            right_on="category_id",
            how="left",
        )
        .groupby("id")
        .agg(pl.col("category").list().alias("categories"))
    )
    df = df.select(pl.all().exclude("categories")).join(category_pairings, on="id")

    df.write_parquet("api.parquet")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
