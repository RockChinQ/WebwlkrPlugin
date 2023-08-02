import requests

import uuid
import json
import logging


endpoint = "https://webreader.webpilotai.com/api/visit-web"


def process(url: str, *args, **kwargs) -> str:
    """直接去调人家WebPilot的接口"""

    header = {
        "Content-Type": "application/json",
        "WebPilot-Friend-UID": str(uuid.uuid4()),
    }

    data = {
        "link": url,
        'user_has_request': False
    }

    resp = requests.post(endpoint, headers=header, json=data)

    logging.debug("webpilot resp: {}".format(resp.json()))

    return json.dumps(resp.json(), ensure_ascii=False)