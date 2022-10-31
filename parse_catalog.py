from dataclasses import dataclass, asdict
import json
import logging
import typing as t

import httpx
import lxml.html

CATALOG_URL = "https://gestionmadrid.mercadosocial.net/accounts/catalogo/"

logger = logging.getLogger(__name__)


@dataclass
class CatalogEntity:
    entity_name: str
    entity_description: str
    entity_address: str
    social_links: t.Dict[str, str]
    img_url: str
    report_url: str


class JSONCatalogEntityEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CatalogEntity):
            return asdict(obj)
        return super().default(self, obj)


def get_categories(element):
    options = element.xpath('//*[@id="id_categories"]/option')
    return {option.text: option.attrib["value"] for option in options}


def parse_entity(element):
    div_img, div_content, div_report = element.xpath("div/div")

    img_url = div_img.xpath(".//img")[0].attrib["src"]

    entity_name = div_content.xpath("h3")[0].text
    entity_description = div_content.xpath("p")[0].text
    entity_address = div_content.xpath("strong")[0].text
    social_links = {
        a.attrib["title"]: a.attrib["href"]
        for a in div_content.xpath("./div[contains(@class, 'social-links')]/a")
    }

    # TODO: Extract exemption status
    report_url = div_report.xpath(".//img")[0].attrib["src"]

    return CatalogEntity(
        entity_name=entity_name,
        entity_description=entity_description,
        entity_address=entity_address,
        social_links=social_links,
        img_url=img_url,
        report_url=report_url,
    )


def parse_entities(element):
    tds = element.xpath('//*[@id="results"]//td[@class="entity-td"]')
    return [parse_entity(td) for td in tds]


def main():
    resp = httpx.get(CATALOG_URL)
    resp.raise_for_status()

    page = lxml.html.fromstring(resp.text)

    categories = get_categories(page)

    entities = {}
    for name, cat_id in categories.items():
        logger.info("Reading category %s", name)

        resp = httpx.get(CATALOG_URL, params={"categories": cat_id})
        resp.raise_for_status()

        page = lxml.html.fromstring(resp.text)
        entities[name] = parse_entities(page)

    with open("catalog.json", "w") as fh:
        json.dump(entities, fh, cls=JSONEntityEncoder)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
