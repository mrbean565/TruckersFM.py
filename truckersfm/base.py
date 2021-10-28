from typing import Union
import urllib3
import json
from .baseExceptions import ConnectionError, NotFoundError, RateLimitError

http = urllib3.PoolManager()


class TruckersMP:
    def __init__(self):
        self._root_url = "https://api.simulatorhits.com/v2/"

    def __checkError(self, errorCode) -> Union[bool, Exception]:
        if errorCode in [400, 401, 403, 502, 503, 504]:
            raise ConnectionError()
        elif errorCode == 404:
            raise NotFoundError()
        elif errorCode == 429:
            raise RateLimitError()

    def __decode_data(self, req) -> dict:
        return json.loads(req.data.decode("utf-8"))



    def get_servers(self) -> dict:
        """
        Fetches now-playing info
        """
        req = http.request("GET", f"{self._root_url}/now-playing")
        self.__checkError(req.status)

        return self.__decode_data(req)
