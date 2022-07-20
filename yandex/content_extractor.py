import logging
import os

from web_data_loader import WebLoader


def save_content_to_file(web_content, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(web_content)
        logging.info(f'Content saved to file {file_name}')


def fetch_raw_data(data, source_url, data_directory) -> str:

    barcode = data['barcode']
    name = data['name']

    logging.info(f'Processing barcode {barcode}, name {name}...')

    page_file_name = os.path.join(data_directory, f'{barcode}.html')

    if os.path.exists(page_file_name):
        logging.info(f'File {page_file_name} already exists. Skipped')
        result = 'exists'
        return result

    #url = source_url % name
    url = source_url

    logging.info(f'Fetching data from {url}')
    web_loader = WebLoader(request_executor='selenium')
    #web_content = web_loader.fetch_text_data(url)
    web_content = web_loader.find_and_fetch_text_data(url, name, 'input__control', 'websearch-button')

    if str(web_content).find('Яндекс Картинки') == -1:
        logging.warning(f'Scrapper are banned by search engine. Skipped...')
        result = 'banned'
        return result

    save_content_to_file(web_content, page_file_name)

    result = 'success'
    return result
