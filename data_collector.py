import json
import shutil

import config
import logging
import sys
import os
import csv


def get_directories_list() -> list:
    directories_list = [entry.path for entry in list(os.scandir(config.DIRETORY_FOR_PROCESSING))]
    return directories_list


def get_list_of_files(directory, extension) -> list:
    files = os.listdir(directory)

    filtered_files = list(filter(lambda x: x.endswith(f'.{extension}'), files))

    return filtered_files


def collect_data() -> list:
    directories_for_processing = get_directories_list()

    collected_data = []

    for directory in directories_for_processing:
        data_file_name = os.path.join(directory, 'category.json')
        if not os.path.exists(data_file_name):
            continue

        with open(data_file_name, encoding='utf-8') as f:
            data = json.load(f)

        barcode = os.path.basename(directory)

        row = {
            'category': data['category'],
            'name': data['description'],
            'barcode': barcode,
            'price': 0,
            'code': '',
            'description': '',
        }

        collected_data.append(row)

        jpg_files = get_list_of_files(directory, 'jpg')

        if len(jpg_files) > 0:
            src_file_name = jpg_files[0]
            dst_file_name = f'{barcode}.jpg'

            shutil.copy2(
                os.path.join(directory, src_file_name),
                os.path.join(config.COLLECTED_DATA_PATH, dst_file_name))

    return collected_data


def save_data_to_csv(file_name, field_names, data):
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


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

    data = collect_data()

    field_names = ['category', 'name', 'description', 'price', 'barcode', 'code']

    file_name = os.path.join(config.COLLECTED_DATA_PATH, 'data.csv')

    save_data_to_csv(file_name, field_names, data)

    logging.info("Finish script")


