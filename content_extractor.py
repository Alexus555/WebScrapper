import os

from web_data_loader import WebLoader


def save_content_to_file(web_content, file_name):
    with open(file_name, 'w') as f:
        f.write(web_content)


def fetch_raw_data(data, source_url, data_directory) -> None:
    barcode = data.barcode
    name = data.name

    url = source_url % name
    web_loader = WebLoader()
    web_content = web_loader.fetch_text_data(url)

    page_file_name = os.path.join(data_directory, f'{barcode}.html')
    save_content_to_file(web_content, page_file_name)
