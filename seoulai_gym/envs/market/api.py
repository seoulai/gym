import requests
import json
from seoulai_gym.envs.market.config import BASE_URL


class BaseAPI():
    def __init__(
        self,
    ) -> None:
        """Initialize BaseAPI
        Args:
            None
        Returns:
            None
        """

    def api_post(
        self,
        cmd,
        data,
    ):
        url = BASE_URL + cmd
        print(url, json.dumps(data))
        headers = {"content-type": "application/json"}
        r = requests.post(url,
                          headers=headers,
                          data=json.dumps(data))
        if r.status_code == 200:
            return r.json()
        return None

    def api_get(
        self,
        cmd,
        data,
    ):
        url = BASE_URL + cmd
        conditions = [key+"="+value for key, value in data.items()]
        query = "?" + "&".join(conditions)
        url += query
        print(url, json.dumps(data))
        # headers = {"content-type": "application/json"}
        # print(url, json.dumps(data))
        r = requests.get(url)

        if r.status_code == 200:
            return r.json()
        return None
