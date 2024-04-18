import json
from fake_useragent import UserAgent
import requests

ua = UserAgent()
headers_for_stratz = {
    'User-Agent': f'{ua.random}',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiNzVmODYxYzktMWFlZi00NmRmLTliZDYtYzY0NWFiOGE5NDQwIiwiU3RlYW1JZCI6IjExNTEwNjcxODYiLCJuYmYiOjE3MTAwNTkxMTIsImV4cCI6MTc0MTU5NTExMiwiaWF0IjoxNzEwMDU5MTEyLCJpc3MiOiJodHRwczovL2FwaS5zdHJhdHouY29tIn0.84meNwXgF6YuVOIVKLo7v3GhlK4uvmnZqYM7zfNa_s4'
}
headers_for_opendota = {
    'User-Agent': f'{ua.random}'
}
heroes = requests.get(url=f'https://api.opendota.com/api/heroes', headers=headers_for_opendota).json()
with open('heroes.json', 'w') as file:
    json.dump(heroes, file, indent=4)

items = requests.get(url='https://docs.stratz.com/api/v1/Item', headers=headers_for_stratz).json()
with open('items.json', 'w') as file:
    json.dump(items, file, indent=4)

