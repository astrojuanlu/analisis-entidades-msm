import polars as pl

df_hg = pl.read_parquet("catalog.parquet")
df_ha = pl.read_parquet("api.parquet")

print("Entities in the HG but not in HA have not created their profile yet: ")
print(set(df_hg["entity_name"]) - set(df_ha["name"]))

print(
    "Entities in the HA but not in the HG "
    "are either inactive, invalid, or have a name discrepancy: "
)
print(set(df_ha["name"]) - set(df_hg["entity_name"]))
