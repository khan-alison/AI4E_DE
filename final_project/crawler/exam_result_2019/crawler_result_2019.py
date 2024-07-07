import requests

from helper.logger_helper import LoggerSimple
from bs4 import BeautifulSoup
from config.directory_management import DirectoryManagement

logger = LoggerSimple.get_logger(__name__)


def get_url_check(id_number):
    return f'https://diemthi.tuoitre.vn/kythi2019.html?FiledValue={id_number}&MaTruong={id_number[:2]}'


def extract_data_result(id_number):
    url_api = f'https://d3ewbr0j99hudd.cloudfront.net/search-exam-result/2021/result/{id_number}.json'
    data_exam = None

    try:
        response = requests.get(url=url_api)
        if response.status_code == 200:
            data = response.json()

            print(data)
            if data.get('studentCode') is not None:
                data_exam = data
    except Exception as e:
        logger.error(e)
        logger.error(f'ERROR: sbd={id_number}')

    return data_exam


def build_id_number(provide_id, post_id):
    prefix = ''.join(['0' for i in range(6 - len(str(post_id)))])
    # logger.info(prefix)
    return f'{provide_id}{prefix}{post_id}'


def get_min_max_by_code(provide_id='64'):
    min = 1
    max = 999999

    should_find = True
    min = int((max - min) / 2) + min
    while (should_find):
        if ((min - max) ** 2) == 1:
            break
        mid = int((max - min) / 2) + min
        id_number = build_id_number(provide_id=provide_id, post_id=mid)
        if extract_data_result(id_number) is None:
            max = mid
            continue
        else:
            min = mid
            continue
    return mid


if __name__ == '__main__':
    dm = DirectoryManagement()
    lst_provide = ['{0:02}'.format(num) for num in range(1, 2)]
    for provide_id in lst_provide:
        try:
            logger.info(f'prepare crawl provide: {provide_id}')
            batch_id_number = 5000

            max_id_number = get_min_max_by_code(provide_id)

            all_data = []
            group_name = None

            for pos in range(1, 200):
                id_number = build_id_number(provide_id=provide_id, post_id=pos)
                data = extract_data_result(id_number=id_number)
                if data:
                    all_data.append(data)
                    if not group_name:
                        group_name = data.get('groupName', f'provide_{provide_id}')

            if all_data and group_name:
                dm.save_data_exam_result(all_data, f'{group_name}.csv')

        except Exception as e:
            logger.error(e)