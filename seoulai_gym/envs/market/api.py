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
        headers = {'content-type': 'application/json'}
        r = requests.post(url,
                          headers=headers,
                          data = json.dumps(data))
        return r.json()

    def api_get(
        self,
        cmd,
        data,
    ):
        url = BASE_URL + cmd
        print(url, json.dumps(data))
        headers = {'content-type': 'application/json'}
        r = requests.get(url,
                          headers=headers,
                         data = json.dumps(data))
        return r.json()
