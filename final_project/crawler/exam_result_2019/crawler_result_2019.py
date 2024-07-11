import requests
import aiohttp
from helper.logger_helper import LoggerSimple
from bs4 import BeautifulSoup
from config.directory_management import DirectoryManagement
from helper.multithread_helper import multithread_helper
from concurrent.futures import ThreadPoolExecutor

logger = LoggerSimple.get_logger(__name__)


def get_url_check(id_number):
    return f'https://diemthi.tuoitre.vn/kythi2019.html?FiledValue={id_number}&MaTruong={id_number[:2]}'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


def extract_data_result(id_number):
    url_api = f'https://d3ewbr0j99hudd.cloudfront.net/search-exam-result/2021/result/{id_number}.json'
    data_exam = None
    try:
        response = requests.get(url_api)
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


def create_array_url(start, end):
    array_url = []
    for i in range(start, end):
        array_url.append(get_url_check(i))

    return array_url


if __name__ == '__main__':
    dm = DirectoryManagement()
    executor = ThreadPoolExecutor()
    max_executor = executor._max_workers
    lst_provide = ['{0:02}'.format(num) for num in range(1, 65)]
    for provide_id in lst_provide:
        try:
            logger.info(f'prepare crawl provide: {provide_id}')
            max_id_number = get_min_max_by_code(provide_id)
            all_data = []
            group_name = None
            batch_size = 500

            for batch_start in range(1, 500, batch_size):
                batch_end = min(batch_start + batch_size, max_id_number)
                id_numbers = [build_id_number(provide_id, post_id) for post_id in range(batch_start, batch_end)]
                batch_data = multithread_helper(items=id_numbers, method=extract_data_result, max_workers=8)
                logger.debug(f'batch_data: {batch_data}')
                if batch_data:
                    all_data.extend(batch_data)
                    if not group_name and batch_data:
                        group_name = batch_data[0].get('groupName', f'provide_{provide_id}')

            logger.info(f'Total records fetched for provide_id {provide_id}: {len(all_data)}')
            if group_name:
                logger.info(f'Group name determined: {group_name}')

            if all_data and group_name:
                logger.info(f'Saving data for group {group_name}')
                dm.save_data_exam_result(all_data, f'{group_name}.csv')
                logger.info(f'Data saved for {group_name}.csv')
            else:
                logger.warning(f'No data to save for provide_id {provide_id}')

        except Exception as e:
            logger.error(e)
