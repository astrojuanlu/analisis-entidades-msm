import logging
import json
import unicodedata

import lxml.html
import httpx

logger = logging.getLogger(__name__)

BENEFITS_URLS = {
    "socias": "https://madrid.mercadosocial.net/ventajas-socias/",
    "entidades": "https://madrid.mercadosocial.net/ventajas-entidades/",
}


def get_categories(element):
    links = element.xpath(
        "//div[@class='post-content']//div[@class='fusion-gallery-image']/a"
    )
    return {link.xpath("img")[0].attrib["title"]: link.attrib["href"] for link in links}


def parse_benefits(element):
    entities_divs = element.xpath("//div[@class='awsm-content-scrollbar']")
    benefits = {}
    for entity_div in entities_divs:
        entity_name = entity_div.xpath("h2")[0].text
        ps = entity_div.xpath(".//p")
        benefit_text = unicodedata.normalize(
            "NFKC", " ".join(p.text_content() for p in ps)
        )
        benefits[entity_name] = benefit_text

    return benefits


def scrape_benefits_page(benefits_url):
    resp = httpx.get(benefits_url)
    resp.raise_for_status()

    page = lxml.html.fromstring(resp.text)

    categories = get_categories(page)

    benefits = {}
    for name, cat_url in categories.items():
        logger.info("Reading category %s", name)

        resp = httpx.get(cat_url, follow_redirects=True)
        resp.raise_for_status()

        page = lxml.html.fromstring(resp.text)
        benefits[name] = parse_benefits(page)

    return benefits


def main():
    for audience, url in BENEFITS_URLS.items():
        benefits = scrape_benefits_page(url)

        with open(f"benefits_{audience}.json", "w") as fh:
            json.dump(benefits, fh, ensure_ascii=False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
