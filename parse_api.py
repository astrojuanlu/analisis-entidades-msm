import logging
import json

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://app.mercadosocial.net"
API_URL = BASE_URL + "/api/v1/entities/"


def main():
    data = []
    url = API_URL
    while True:
        logger.info("Reading URL %s", url)

        resp = httpx.get(url)
        resp.raise_for_status()

        resp_json = resp.json()

        data.extend(resp_json["entities"])

        if resp_json["meta"]["next"]:
            url = BASE_URL + resp_json["meta"]["next"]
        else:
            break

    with open("api.json", "w") as fh:
        json.dump(data, fh)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
