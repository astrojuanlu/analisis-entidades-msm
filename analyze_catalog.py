import polars as pl

df_catalog = pl.read_parquet("catalog.parquet")

percentages_social = (
    df_catalog.select(
        ~pl.col(["facebook", "twitter", "web", "instagram", "telegram"]).is_null()
    ).sum()
    * 100.0
    / len(df_catalog)
)
print(percentages_social)

stats_per_category = (
    df_catalog.explode("categories_in_catalog")
    .groupby("categories_in_catalog")
    .agg(
        [
            pl.col(["facebook", "twitter", "web", "instagram", "telegram"])
            .is_not_null()
            .sum()
            * 100.0
            / pl.count(),
            pl.count(),
        ]
    )
).sort("categories_in_catalog")
print(stats_per_category)
