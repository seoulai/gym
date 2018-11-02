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
    def api(
        self,
        cmd,
        data,
    ):
        base_url = "https://"+SERVER_IP+"/api/"
        url = base_url + cmd

        r = requests.post(url, data)
        return r.json()
