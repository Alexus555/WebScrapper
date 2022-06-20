import requests


class WebLoader:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        })

    def fetch_web_data(self, url: str) -> str:
        request = self._session.get(url)
        return request.text


