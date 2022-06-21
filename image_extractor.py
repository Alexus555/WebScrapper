import logging
import os
import shutil
import json

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


def save_description(image_directory, image_data_list):
    description_file_name = os.path.join(image_directory, 'description.json')
    with open(description_file_name, 'w', encoding='utf-8') as f:
        json.dump(image_data_list,
                  f,
                  indent=4,
                  sort_keys=True,
                  ensure_ascii=False)
        logging.info(f'Description saved to file {description_file_name}')


def fetch_image_data_from_text(text: str) -> list:
    soup = BeautifulSoup(text, 'lxml')
    img_meta_list = soup.find_all('div', {'class': 'justifier__item'})

    image_data_list = [
        {
            'index': img_meta_list.index(i),
            'image_src': json.loads(i.attrs["data-bem"])["serp-item"]["img_href"],
            'image_desc': json.loads(i.attrs["data-bem"])["serp-item"]["snippet"]["title"],
            'processing_result': '',
        } for i in img_meta_list[:5]]

    logging.info(f'{len(image_data_list)} image(s) were found in content')

    return image_data_list


def get_description_from_content(text: str) -> str:
    soup = BeautifulSoup(text, 'lxml')
    meta_data = soup.find('meta', {'name': 'description'})

    description = ''
    if meta_data is not None:
        description = \
            str(
                meta_data.attrs['content']
            ).replace(
                'Результаты поиска по запросу "',
                ''
            ).replace(
                '" в Яндекс Картинках',
                '')

    return description


def get_files_for_processing(data_path: str) -> list:
    files = os.listdir(data_path)

    files = [
        os.path.join(data_path, fn) for fn in filter(lambda x: x.endswith('.html'), files)]

    logging.info(f'{len(files)} file(s) were found in directory {data_path}')

    return files


def read_file_and_extract_images(file_name: str, directory_for_save: str):
    logging.info(f'Reading file {file_name}...')

    name = str(os.path.basename(file_name)).replace('.html', '').lower()
    image_directory = os.path.join(directory_for_save, name)
    if os.path.exists(image_directory) and len(os.listdir(image_directory)) > 1:
        logging.info(f'The directory {image_directory} is not empty. Skipped...')
        return

    prepare_directory(image_directory)

    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()

    description = get_description_from_content(content)
    image_data_list = fetch_image_data_from_text(content)

    web_loader = WebLoader()
    for image_data in image_data_list:
        image_url = str(image_data['image_src'])
        if image_url.find('http') == -1:
            image_url = f'http:{image_url}'

        logging.info(f"Fetching image from {image_url}")

        image_data['processing_result'] = 'Success'

        try:
            raw_image = web_loader.fetch_image_data(image_url)
        except Exception as e:
            logging.error(e)
            image_data['processing_result'] = str(e)
            continue

        image_file_name = os.path.join(image_directory, f"{image_data['index']}.jpg")

        save_raw_image_to_file(raw_image, image_file_name)

    description_data = \
        {
            'description': description,
            'image_data': image_data_list,
        }

    save_description(image_directory, description_data)


def extract_images(source_directory: str, dest_directory):
    files_for_processing = get_files_for_processing(source_directory)

    for file in files_for_processing:
        read_file_and_extract_images(file, dest_directory)
