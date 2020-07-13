import requests
from pprint import pprint
from datetime import datetime
import time

# создадим время в секундах для формата UNIX_TIME
AMOUNT_DAYS_AGO_IN_SECONDS = int(time.time())-int(input("За сколько дней вывести сведения? "))*60*60*24

# print(datetime.fromtimestamp(AMOUNT_DAYS_AGO_IN_SECONDS))


URL = 'https://api.stackexchange.com/2.2'
# dop_url = '/tags/' + input("Введите поле поиска: ") + '/faq'
dop_url = '/tags/python/faq'
params = {'site': 'stackoverflow', 'limit': 10}
auth = {'Authorization': 'hzUr3MIMzLQcl2R*Li*CQA))'}

# req = requests.get('https://api.stackexchange.com/2.2/tags/python/faq?site=stackoverflow', headers=auth)
req = requests.get(URL+dop_url, params=params)
req2 = requests.get(URL+'/questions', params={'fromdate': AMOUNT_DAYS_AGO_IN_SECONDS, 'tagged': 'python', 'site': 'stackoverflow'})
print(req2.json())

for i in req2.json()['items']:
    if i['creation_date'] > AMOUNT_DAYS_AGO_IN_SECONDS:
        print(datetime.fromtimestamp(i['creation_date']))
        pprint(i['title'])
        print()