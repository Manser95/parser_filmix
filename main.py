import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = 'https://filmix.co/filmy/'
URL_PAGE = 'https://filmix.co/filmy/page/'
FILE_FILMS = 'filmi.csv'

Headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'
}


def get_html(url, params=None):
    r = requests.get(url, headers=Headers, params=params)
    return r


def get_page_count(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    navigation_div = soup.find('div', class_='navigation')
    pages_count = navigation_div.find_all_next('a')[3].text
    return pages_count


def get_links(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    items = soup.find_all('article', class_='shortstory line')
    links = []
    for item in items:
        links.append(item.find('h2', class_='name').a.get('href'))
    return links


# def get_content(html):
#     soup = BeautifulSoup(html.content, 'html.parser')
#     items = soup.find_all('article', class_='shortstory line')
#     # print(items[1])
#     films = []
#     for item in items:
#         films.append({
#             'name': item.find('h2', class_='name').a.get('title'),
#             'link': item.find('h2', class_='name').a.get('href'),
#             'genre': item.find('div', class_='item category').a.text,
#             'year': item.find('div', class_='item year').a.text,
#             # ''

#             # item.find('', class_='')
#         })
#     return films

def get_content(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    item = soup.find('div', class_='full min')
    # print(items[1])
    films = []
    films.append({
        'name': item.find('h1', class_='name').text,
        'original_name': item.find('div', class_='origin-name').text,
        'genre': item.find('div', class_='item category').find('span', class_='item-content').get_text(strip=True),
        'country': item.find('div', class_='item contry').a.text,
        'year': item.find('div', class_='item year').a.text,
        'directors': item.find('div', class_='item directors').find('span', class_='item-content').get_text(strip=True),
        'actors': item.find('div', class_='item actors').find('span', class_='item-content').get_text(strip=True),
        'duration': item.find('div', class_='item durarion').find('span', class_='item-content').text,
        'translation': item.find('div', class_='item translate').find('span', class_='item-content').get_text(strip=True),
        'description': item.find('div', class_='full-story').text,

        # item.find('', class_='')
    })
    return films


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for item in items:
            writer.writerow([item['name'], item['original_name'],
                             item['genre'], item['country'], item['year'], item['directors'], item['actors'], item['duration'], item['translation'], item['description']])


def parser():
    base_html = get_html(BASE_URL)
    if base_html.status_code == 200:
        # print(get_content(
        #     get_html('https://filmix.co/drama/147988-ana-lyubit-2019.html')))

        pages_count = int(get_page_count(base_html))
        for page in range(pages_count+1):
            links = get_links(get_html(URL_PAGE + f'{page}'))
            films = []
            for link in links:
                films.extend(get_content(get_html(link)))
            save_file(films, 'films.csv')
    else:
        print('Error')


parser()
