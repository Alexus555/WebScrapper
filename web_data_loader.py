import requests


class WebLoader:
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        })

    def fetch_text_data(self, url: str) -> str:
        response = self._session.get(url)
        if response.status_code == 200:
            return response.text

        response.raise_for_status()

    def fetch_image_data(self, url: str):
        response = self._session.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            return response.raw

        response.raise_for_status()






