import logging
from config.directory_management import DirectoryManagement
import requests
from bs4 import BeautifulSoup
from helper.logger_helper import LoggerSimple

logger = LoggerSimple.get_logger(__name__)


def get_infor(url_benchmark, year):
    benchmark_datas = []
    try:
        url_with_year = f'{url_benchmark}?y={year}'
        response = requests.get(url_with_year)
        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            e_table = soup.select_one('table')
            for e_tr in e_table.select('.bg_white'):
                e_tds = e_tr.select('td')
                major_code = e_tds[1].get_text()
                major_name = e_tds[2].get_text()
                subjects_group = [subject_group.strip() for subject_group in e_tds[3].get_text().split(';')]
                point = e_tds[4].get_text()
                note = e_tds[5].get_text()
                for subject_group in subjects_group:
                    benchmark_obj = {
                        'major_code': major_code,
                        'major_name': major_name,
                        'subject_group': subject_group,
                        'point': point,
                        'note': note,
                        'year': year
                    }
                    logger.info(benchmark_obj)
                    benchmark_datas.append(benchmark_obj)
            return benchmark_datas
        else:
            logger.warning(f'{response.status_code} - {url_with_year}')
    except Exception as e:
        logger.error(f'Error fetching data from {url_with_year}: {e}')


def extract_data_benchmark(url_benchmark, university_meta, year=None):
    benchmark_datas = get_infor(url_benchmark, year)
    logger.info(benchmark_datas)
    return {'benchmark_datas': benchmark_datas, 'university_meta': university_meta}


if __name__ == "__main__":
    dm = DirectoryManagement()
    try:
        universities_data = dm.load_universities_data('universities_data.csv')
        logger.info(f'Loaded data for {len(universities_data)} universities')
    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
        universities_data = []

    for year in [2019, 2020, 2021, 2022, 2023]:
        for university_data in universities_data:
            url = university_data.get('url')
            data = extract_data_benchmark(url_benchmark=url, university_meta=university_data, year=year)
            benchmark_data = data.get('benchmark_datas')
            if benchmark_data:
                year = data.get('benchmark_datas')[0].get('year')
                file_name = f'benchmark_{year}/{university_data["university_code"]}_{year}.csv'
                dm.save_data_benchmark(benchmark_data, file_name)
                logger.info(f'Benchmark data saved to {file_name}')
