import requests

URL = 'https://filmix.co/filmy/'
FILE_FILMS = 'filmi.csv'

Headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'
}

def get_html(url, params=None):
    r = requests.get(url, headers=Headers, params=params)
    return r

def parser():
    html = get_html(URL)
    print(html.status_code)

parser()
