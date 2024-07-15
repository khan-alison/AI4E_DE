import requests
from bs4 import BeautifulSoup
from config.directory_management import DirectoryManagement

def get_content_request(url='https://diemthi.tuyensinh247.com/diem-chuan.html'):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return requests.get(url).content
    except requests.exceptions.RequestException as e:
        print(f'Error fetching URL: {e}')
        return None


def extract_content(html):
    if html is None:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    universities_data = []

    for e_li in soup.select('#benchmarking > li'):
        a_tag = e_li.find('a')
        url = 'https://diemthi.tuyensinh247.com' + a_tag.get('href') if a_tag.get('href') != '' else None
        universities_code = a_tag.find('strong').get_text()
        universities_name = a_tag.get_text().split('-')[1].strip()
        universities_information = {
            'url': url,
            'university_code': universities_code,
            'university_name': universities_name
        }
        universities_data.append(universities_information)
    return universities_data


if __name__ == '__main__':
    url = 'https://diemthi.tuyensinh247.com/diem-chuan.html'
    content_html = get_content_request(url=url)
    universities_data = extract_content(html=content_html)
    dm = DirectoryManagement()

    dm.save_universities_data(universities_data, 'universities_data.csv')
