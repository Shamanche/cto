import requests
from save import save_to_html

API_URL = 'https://pk.platformaofd.ru/api/monitoring'

payload = {
    'badgeId': 1,
    'type': "client",
    'filterValues': [],
    'withArchive': 1}


r = requests.post(API_URL, data=payload)

print(r)
