import requests
##from utils import *

def squeezed (client_name):
    return client_name.replace('Индивидуальный предприниматель', 'ИП')

def get_kkm_filled_fn(max_fill=75):
## возвращает список ККМ с ФН заполненными больше max_fill в %
    LOGIN_URL = 'https://pk.platformaofd.ru/auth/login'
    API_URL = 'https://pk.platformaofd.ru/api/monitoring'

    session = requests.Session()
    print('-= подключение к серверу =-')
    session.get(LOGIN_URL)

    login_data = {
        'email': 'efimova@21smart.ru',
        'password': 'smart620514',
        'username': 'efimova@21smart.ru',
        'phone':''}

    print('-= авторизация =-')
    session.post(LOGIN_URL, data=login_data)

    # запрос всех ККМ, кроме архивных (headers обязательно !)
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    payload = '{"badgeId":17,"type":"terminal","filterValues":[],"withArchive":0}'
    print('-= получение данных с сервера =-')
    r = session.post (API_URL, data=payload, headers=headers)

    data_from_api = r.json()
    all_kkm_list = data_from_api['result']['data']
    kkm_quanity = len(all_kkm_list)

    print('-= обработка данных =-')
    kkm_with_filled_fn = []
    for kkm in all_kkm_list:
        fn_used = int(kkm['fnSpaceUsed'].strip("'%"))
        if fn_used >= max_fill:
            kkm_with_filled_fn.append(kkm)
    return kkm_with_filled_fn


max_fill = 80
x = get_kkm_filled_fn(max_fill)
text_list = []
text_list.append( f'ККМ с заполненностью ФН выше {max_fill}%.\n')
for k in x:
    text_list.append("{:4} {:39.37} {:31.30}".format(k['fnSpaceUsed'],
                                    k['deviceName'], squeezed(k['clientName'])))

text = '\n'.join(text_list)
print(text)
