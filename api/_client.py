import time

from requests import Session, Response
from slumber import API

import config
from libs.logger import get_log

log = get_log("AM-Vision API")


class _APISession(Session):
    def request(self, method: str, url: str, **kwargs) -> Response:
        start = time.perf_counter()
        resp = super().request(method, url, **kwargs)
        end = time.perf_counter()
        duration = int(1000 * (end - start))

        if 400 <= resp.status_code <= 499:
            log.warning(f"{method} {url} {resp.status_code}: {resp.json()}")
        else:
            log.info(f"{method} {url} {resp.status_code} {duration}ms")

        return resp


class APIClient(API):
    def __init__(self) -> None:
        super().__init__(config.API_URL, session=_APISession())
        self._store["session"].auth = None
        self._store["session"].headers["Authorization"] = f"Token {config.API_TOKEN}"


api = APIClient()
