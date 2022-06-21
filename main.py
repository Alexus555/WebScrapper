import json
import config
import logging
import sys
from yandex import content_extractor, image_extractor


def extract_content():
    with open(config.PROCESSING_LIST, 'r', encoding='utf-8') as f:
        data_for_processing = json.load(f)

    for data in data_for_processing:
        result = content_extractor.fetch_raw_data(data, config.SEARCH_ENGINE_URL, config.RAW_DATA_PATH)
        if result == 'banned':
            return


def extract_images():
    image_extractor.extract_images(config.RAW_DATA_PATH, config.PREP_DATA_PATH)


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format=u"%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(".\\script.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("Start script")

    extract_content()

    extract_images()

    logging.info("Finish script")


