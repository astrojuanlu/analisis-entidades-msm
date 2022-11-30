import os

import polars as pl

from recordlinkage.preprocessing import clean

df_catalog = pl.read_parquet("api.parquet")
df_benefits = pl.read_parquet("benefits.parquet")

# If the file exists, just use it
# This allows operators to edit it manually
if not os.path.isfile("entity_pairs.csv"):
    df_benefits.select(
        [
            pl.col("name_in_benefits"),
            pl.from_pandas(
                clean(
                    df_benefits["name_in_benefits"].to_pandas(), strip_accents="ascii"
                )
            ).alias("entity_name_clean"),
        ]
    ).join(
        df_catalog.select(
            [
                pl.col("name").alias("name_in_catalog"),
                pl.from_pandas(
                    clean(df_catalog["name"].to_pandas(), strip_accents="ascii")
                ).alias("entity_name_clean"),
            ]
        ),
        on="entity_name_clean",
        how="left",
    ).write_csv(
        "entity_pairs.csv"
    )

entity_pairs = pl.read_csv("entity_pairs.csv")

df = df_catalog.join(
    entity_pairs.select(pl.all().exclude("entity_name_clean")),
    left_on="name",
    right_on="name_in_catalog",
    how="left",
).join(df_benefits, on="name_in_benefits", how="left")

df.select(pl.all().exclude(pl.List(pl.Utf8))).sort("name").write_csv(
    "entities_full.csv"
)

df.filter(
    pl.col("benefit_text_socias").is_null() & pl.col("benefit_text_entidades").is_null()
).select(pl.col("name")).sort("name").write_csv("no_benefits.csv")

with_benefits = df.select(
    pl.all().exclude(
        [
            "address",
            "short_description",
            "description",
            "facebook_link",
            "instagram_link",
            "twitter_link",
            "webpage_link",
            "categories",
            "categories_in_benefits_socias",
            "categories_in_benefits_entidades",
        ]
    )
).to_pandas()
benefits_columns = with_benefits.loc[:, "benefit_text_socias":].columns
with_benefits.dropna(how="all", subset=benefits_columns).to_csv("with_benefits.csv")
