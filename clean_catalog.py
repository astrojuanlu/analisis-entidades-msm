import json
import polars as pl

SOCIAL_MAPPING = {
    "Página de Facebook": "facebook",
    "Perfil de Twitter": "twitter",
    "Perfil de Instagram": "instagram",
    "Canal de Telegram": "telegram",
    "Página web": "web",
}


with open("catalog.json") as fh:
    catalog = json.load(fh)

catalog_data = []
for category_name, entities in catalog.items():
    for entity_data in entities:
        entity_data["category_in_catalog"] = category_name
        for social_name, social_url in entity_data.pop("social_links").items():
            entity_data[SOCIAL_MAPPING[social_name]] = social_url
        catalog_data.append(entity_data)

df_catalog = pl.from_records(catalog_data)

# Verify that duplicated rows match duplicated names
whole_duplicates = df_catalog.select(
    pl.all().exclude("category_in_catalog")
).is_duplicated()
name_duplicates = df_catalog["entity_name"].is_duplicated()
assert (whole_duplicates == name_duplicates).all()

categories_in_catalog = df_catalog.groupby("entity_name").agg(
    [pl.col("category_in_catalog").list().alias("categories_in_catalog")]
)

df = (
    df_catalog.unique(subset="entity_name")
    .select(pl.all().exclude("category_in_catalog"))
    .join(categories_in_catalog, on="entity_name")
)
df.write_parquet("catalog.parquet")
