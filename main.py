from bs4 import BeautifulSoup
import json
import config
import logging
import os
import sys
import shutil
from web_data_loader import WebLoader


def prepare_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)


def fetch_images_from_text(text):
    soup = BeautifulSoup(text)
    film_list = soup.find('div', {'class': 'profileFilmsList'})


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


def get_files_for_processing(data_path: str) -> list:
    files = os.listdir(data_path)

    files = [
        os.path.join(data_path, fn) for fn in filter(lambda x: x.endswith('.html'), files)]

    logging.info(f'{len(files)} file(s) were found in directory {data_path}')

    return files


def read_file_and_extract_images(file_name):

    with open(file_name, 'r') as f:
        content = f.read()

    fetch_images_from_text(content)



def extract_images():
    files_for_processing = get_files_for_processing(config.RAW_DATA_PATH)

    for file in files_for_processing:
        read_file_and_extract_images(file)




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


