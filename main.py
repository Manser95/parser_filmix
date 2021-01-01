import requests

URL = 'https://filmix.co'

req = requests.get(URL)

print(req.status_code)