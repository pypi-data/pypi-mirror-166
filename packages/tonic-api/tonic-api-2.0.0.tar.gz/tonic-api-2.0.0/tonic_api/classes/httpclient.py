import requests


class HttpClient:
    """Client for handling requests to Tonic instance

    Parameters
    ----------
    base_url : str
        URL to Tonic instance
    api_key : str
        The API token associated with your workspace
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": api_key}

    def http_get(self, url: str, params: dict={}):
        """Make a get request.

        Parameters
        ----------
        url : str
            URL to make get request. Is appended to self.base_url.
        params: dict
            Passed as the params parameter of the requests.get request.
        
        """
        try:
            res = requests.get(self.base_url + url, params=params, headers=self.headers)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

    def http_post(self, url, params={}, data={}):
        """Make a post request.

        Parameters
        ----------
        url : str
            URL to make the post request. Is appended to self.base_url.
        params: dict
            Passed as the params parameter of the requests.post request.
        """
        try:
            res = requests.post(
                self.base_url + url, params=params, json=data, headers=self.headers
            )
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)
