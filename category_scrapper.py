import json
import config
import logging
import sys
import os
from biosfera import content_extractor


def get_directories_list():
    directories_list = [entry.path for entry in list(os.scandir(config.DIRETORY_FOR_PROCESSING))]
    return directories_list


def extract_content():
    directories_for_processing = get_directories_list()

    for directory in directories_for_processing:
        data_file_name = os.path.join(directory, 'description.json')
        if not os.path.exists(data_file_name):
            continue

        with open(data_file_name, encoding='utf-8') as f:
            data = json.load(f)

        result = content_extractor.fetch_raw_data(data, config.SEARCH_CATEGORY_URL, directory)
        if result == 'banned':
            return


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

    logging.info("Finish script")


