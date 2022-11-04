import json
import polars as pl

with open("benefits.json") as fh:
    benefits = json.load(fh)

benefits_data = []
for category_name, entities in benefits.items():
    for entity_name, benefit_text in entities.items():
        benefits_data.append(
            {
                "name_in_benefits": entity_name,
                "category_in_benefits": category_name,
                "benefit_text": benefit_text,
            }
        )

# Verify that duplicated rows match duplicated names
df_benefits = pl.DataFrame(benefits_data)
whole_duplicates = df_benefits.select(
    pl.all().exclude("category_in_benefits")
).is_duplicated()
name_duplicates = df_benefits["name_in_benefits"].is_duplicated()

# This doesn't hold! There is one entity that has 2 different benefit texts
# assert (whole_duplicates == name_duplicates).all()
# Let's merge the two different benefits into one, for now
problematic_entities = df_benefits.filter(whole_duplicates != name_duplicates)
problematic_entities = (
    problematic_entities.groupby("name_in_benefits")
    .agg(
        [
            pl.col("category_in_benefits").list().alias("categories_in_benefits"),
            pl.col("benefit_text"),
        ]
    )
    .with_column(pl.col("benefit_text").arr.join(";"))
)

good_entities = df_benefits.filter(
    ~pl.col("name_in_benefits").is_in(problematic_entities["name_in_benefits"])
)
good_entities = good_entities.groupby("name_in_benefits").agg(
    [pl.col("category_in_benefits").list().alias("categories_in_benefits")]
)
df = (
    df_benefits.unique(subset="name_in_benefits")
    .select(pl.all().exclude("category_in_benefits"))
    .join(good_entities, on="name_in_benefits")
    .select(["name_in_benefits", "categories_in_benefits", "benefit_text"])
)
df = pl.concat([df, problematic_entities]).sort("name_in_benefits")

df.write_parquet("benefits.parquet")
