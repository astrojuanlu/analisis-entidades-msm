import json
import logging

import polars as pl
from unidecode import unidecode


def clean_benefits(benefits_json):
    benefits_data = []
    for category_name, entities in benefits_json.items():
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

    good_entities = (
        df_benefits.filter(
            ~pl.col("name_in_benefits").is_in(problematic_entities["name_in_benefits"])
        )
        .groupby("name_in_benefits")
        .agg([pl.col("category_in_benefits").list().alias("categories_in_benefits")])
    )

    df_good = (
        df_benefits.unique(subset="name_in_benefits")
        .select(pl.all().exclude("category_in_benefits"))
        .join(good_entities, on="name_in_benefits")
        .select(["name_in_benefits", "categories_in_benefits", "benefit_text"])
    )

    df = (
        pl.concat([df_good, problematic_entities])
        .sort("name_in_benefits")
        .with_columns(
            [
                pl.col("benefit_text")
                .str.contains("registrada en la app")
                .alias("mentions_app"),
                pl.col("benefit_text")
                .str.contains(
                    "madrid@mercadosocial.net para indicarte el procedimiento"
                )
                .alias("manual_email_procedure"),
                pl.col("benefit_text")
                .str.contains(
                    "Esta ventaja no está disponible para "
                    "socios/as consumidores/as de intercooperación"
                )
                .alias("not_for_intercoop"),
            ]
        )
    )
    return df


def main():
    dfs = {}
    for audience in ("socias", "entidades"):
        with open(f"benefits_{audience}.json") as fh:
            benefits = json.load(fh)
            dfs[audience] = clean_benefits(benefits).select(
                [
                    pl.col("name_in_benefits"),
                    pl.all().exclude("name_in_benefits").suffix(f"_{audience}"),
                ]
            )

    df = (
        dfs["socias"]
        .join(
            dfs["entidades"],
            on="name_in_benefits",
            how="outer",
        )
        .sort(
            by=pl.col("name_in_benefits")
            .str.to_lowercase()
            .apply(lambda s: unidecode(s))
        )
    )
    df.write_parquet("benefits.parquet")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
