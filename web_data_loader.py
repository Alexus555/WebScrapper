import time

import requests
import ssl_warning_suppressor
from selenium import webdriver


class WebLoader:
    def __init__(self, request_executor: str = 'request'):

        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        })

        self._request_executor = request_executor

        if self._request_executor == 'selenium':

            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument('--headless')
            firefox_options.headless = True

            self._driver = webdriver.Firefox(options=firefox_options)
            self._driver.implicitly_wait(3)

    def __del__(self):
        if self._request_executor == 'selenium':
            self._driver.quit()

    def fetch_text_data(self, url: str) -> str:
        if self._request_executor == 'selenium':
            self._driver.get(url)
            page_source = self._driver.page_source
            self._driver.close()
            return page_source

        else:
            with ssl_warning_suppressor.no_ssl_verification():
                response = self._session.get(url, timeout=20)
                if response.status_code == 200:
                    return response.text

            response.raise_for_status()

    def fetch_image_data(self, url: str):
        with ssl_warning_suppressor.no_ssl_verification():
            response = self._session.get(url, stream=True, timeout=20, verify=False)
            if response.status_code == 200:
                response.raw.decode_content = True
                return response.raw

            response.raise_for_status()






