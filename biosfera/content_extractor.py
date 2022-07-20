import json
import logging
import os

from bs4 import BeautifulSoup
from web_data_loader import WebLoader


def save_content_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data,
                  f,
                  indent=4,
                  sort_keys=True,
                  ensure_ascii=False)
        logging.info(f'Content saved to file {file_name}')


def get_url_from_content(text: str) -> str:
    soup = BeautifulSoup(text, 'lxml')
    meta_data = soup.find('div', {'class': 'lotImage'})

    url = ''
    if meta_data is not None:
        url = meta_data.find('a').attrs['href']

    return url


def get_category_name_from_content(text: str) -> str:
    soup = BeautifulSoup(text, 'lxml')
    categories_list = soup.find('div', {'class': 'breadCrumps'})

    category_name = ''
    if categories_list is not None:
        url = categories_list.find_all('a')[1]

    return category_name


def fetch_raw_data(data, source_url, data_directory) -> str:

    url = source_url

    category_file_name = os.path.join(data_directory, 'category.json')

    if os.path.exists(category_file_name):
        logging.info(f'File {category_file_name} already exists. Skipped')
        result = 'exists'
        return result

    web_loader = WebLoader(request_executor='selenium')

    names = [i['image_desc'] for i in data['image_data']]
    names.insert(0, data['description'])

    product_url = ''
    for name in names:
        logging.info(f'Processing name {name}...')
        str_to_search = ' '.join(name.split(' ', maxsplit=2)[:2])

        web_content = web_loader.find_and_fetch_text_data(url, str_to_search, 'searchSend', 'button-search')

        if str(web_content).find('Поиск товаров') == -1:
            logging.warning(f'Scrapper are banned by search engine. Skipped...')
            result = 'banned'
            return result

        if str(web_content).find('ничего не найдено') == -1:
            continue

        product_url = get_url_from_content(web_content)

        break

    product_info_page = web_loader.fetch_text_data(product_url)

    category_name = get_category_name_from_content(product_info_page)

    category_data = {
        'description': data['description'],
        'category': category_name
    }

    save_content_to_file(category_data, category_file_name)

    result = 'success'
    return result
