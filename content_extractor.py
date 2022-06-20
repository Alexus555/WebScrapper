import logging
import os

from web_data_loader import WebLoader


def save_content_to_file(web_content, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(web_content)
        logging.info(f'Content saved to file {file_name}')


def fetch_raw_data(data, source_url, data_directory) -> None:
    barcode = data['barcode']
    name = data['name']

    logging.info(f'Processing barcode {barcode}, name {name}...')
    url = source_url % name

    logging.info(f'Fetching data from {url}')
    web_loader = WebLoader()
    web_content = web_loader.fetch_text_data(url)

    page_file_name = os.path.join(data_directory, f'{barcode}.html')
    save_content_to_file(web_content, page_file_name)
