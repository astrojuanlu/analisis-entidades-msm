import logging
import json

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://app.mercadosocial.net"
ENTITIES_URL = BASE_URL + "/api/v1/entities/"
CATEGORIES_URL = BASE_URL + "/api/v1/categories/"


def scrape_api(url, key, base_url=BASE_URL):
    while True:
        logger.info("Reading URL %s", url)

        resp = httpx.get(url)
        resp.raise_for_status()

        resp_json = resp.json()

        yield from resp_json[key]

        if resp_json["meta"]["next"]:
            url = base_url + resp_json["meta"]["next"]
        else:
            break


def main():
    entities = list(scrape_api(ENTITIES_URL, "entities"))

    with open("api.json", "w") as fh:
        json.dump(entities, fh)

    categories = list(scrape_api(CATEGORIES_URL, "categories"))

    with open("categories.json", "w") as fh:
        json.dump(categories, fh)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
