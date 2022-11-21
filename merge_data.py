import json
import polars as pl

import recordlinkage
from recordlinkage.preprocessing import clean

df_catalog = pl.read_parquet("catalog.parquet")
df_benefits = pl.read_parquet("benefits.parquet")

catalog_cols = df_catalog.columns

df_catalog = df_catalog.with_columns(
    [
        pl.from_pandas(
            clean(df_catalog["entity_name"].to_pandas(), strip_accents="ascii")
        ).alias("entity_name_clean")
    ]
)
df_benefits = df_benefits.with_columns(
    [
        pl.from_pandas(
            clean(df_benefits["name_in_benefits"].to_pandas(), strip_accents="ascii")
        ).alias("entity_name_clean")
    ]
)

indexer = recordlinkage.Index()
# The DataFrames are small, so we can afford creating a Full indexer
indexer.full()
pairs_pd = indexer.index(df_catalog.to_pandas(), df_benefits.to_pandas())

comparer = recordlinkage.Compare()
comparer.string("entity_name_clean", "entity_name_clean")
features_pd = comparer.compute(
    pairs_pd, df_catalog.to_pandas(), df_benefits.to_pandas()
)

features = pl.from_pandas(features_pd.reset_index()).select(
    [
        pl.col("level_0").alias("catalog_idx"),
        pl.col("level_1").alias("benefits_idx"),
        pl.col("0").alias("score"),
    ]
)

matches = (
    features.filter(pl.col("score") > 0.5)  # Only keep likely matches
    .groupby("catalog_idx")
    .agg([pl.col("benefits_idx").sort_by("score", reverse=True).first()])
    .sort("catalog_idx")
)

df_catalog = df_catalog.with_column(pl.arange(0, len(df_catalog)).alias("catalog_idx"))
df_benefits = df_benefits.with_column(
    pl.arange(0, len(df_benefits)).alias("benefits_idx")
)

df = df_catalog.join(matches, on="catalog_idx", how="left").join(
    df_benefits, on="benefits_idx", how="left"
)[catalog_cols + ["categories_in_benefits", "benefit_text"]]

df.drop(["categories_in_catalog", "categories_in_benefits"]).sort(
    "entity_name"
).write_csv("entities_full.csv")

df.filter(pl.col("benefit_text").is_null()).select(pl.col("entity_name")).sort(
    "entity_name"
).write_csv("no_benefits.csv")
