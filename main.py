
import json
import config
import logging
import os
import sys
import shutil
from web_data_loader import WebLoader


def save_content_to_file(web_content, file_name):
    with open(file_name, 'w') as f:
        f.write(web_content)


def fetch_raw_data(data) -> None:
    barcode = data.barcode
    name = data.name

    data_directory = config.RAW_DATA_PATH

    url = config.SEARCH_ENGINE_URL % name
    web_loader = WebLoader()
    web_content = web_loader.fetch_web_data(url)

    page_file_name = os.path.join(data_directory, f'{barcode}.html')
    save_content_to_file(web_content, page_file_name)


def extract_data():
    with open(config.PROCESSING_LIST, 'r') as f:
        data_for_processing = json.load(f)

    for data in data_for_processing:
        fetch_raw_data(data)







if __name__ == 'main':

    logging.basicConfig(
        level=logging.INFO,
        format=u"%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(".\\script.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("Start script")

    extract_data()

    logging.info("Finish script")


