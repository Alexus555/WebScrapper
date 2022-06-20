import logging
import os
import shutil

from bs4 import BeautifulSoup
from web_data_loader import WebLoader


def prepare_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)


def save_raw_image_to_file(raw_image, file_name):
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(raw_image, f)
        logging.info(f'Image saved to file {file_name}')


def fetch_image_data_from_text(text: str) -> list:
    soup = BeautifulSoup(text)
    img_list = soup.find('img', {'class': 'serp-item__thumb'})

    image_data_list = [{'index': img_list.index(i), 'image_src': i.src, 'image_desc': i.alt} for i in img_list]

    logging.info(f'{len(image_data_list)} image(s) were found in directory')

    return image_data_list


def get_files_for_processing(data_path: str) -> list:
    files = os.listdir(data_path)

    files = [
        os.path.join(data_path, fn) for fn in filter(lambda x: x.endswith('.html'), files)]

    logging.info(f'{len(files)} file(s) were found in directory {data_path}')

    return files


def read_file_and_extract_images(file_name: str, directory_for_save: str):
    logging.info(f'Reading file {file_name}...')

    with open(file_name, 'r') as f:
        content = f.read()

    image_data_list = fetch_image_data_from_text(content)

    name = str(os.path.basename(file_name)).replace('.html', '').lower()
    image_directory = os.path.join(directory_for_save, name)
    prepare_directory(image_directory)

    web_loader = WebLoader()
    for image_data in image_data_list:
        logging.info(f"Fetching image from {image_data['image_src']}")
        raw_image = web_loader.fetch_image_data(image_data['image_src'])

        image_file_name = os.path.join(image_directory, f"{image_data['index']}.jpg")

        save_raw_image_to_file(raw_image, image_file_name)


def extract_images(source_directory: str, dest_directory):
    files_for_processing = get_files_for_processing(source_directory)

    for file in files_for_processing:
        read_file_and_extract_images(file, dest_directory)



