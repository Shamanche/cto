from flask import Flask
#from funcs import *
from flask_mail import Mail, Message
import requests
import datetime

# адреса почты, кому будет приходить уведомление
RECIPIENTS = [
    'td@21smart.ru',
    'tsvet005@yandex.ru']

def squeezed (client_name):
    return client_name.replace('Индивидуальный предприниматель', 'ИП')

def get_kkm_filled_fn(max_fill=80):
## возвращает список ККМ с заполнением ФН больше max_fill в %
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

def send_mail(title, body, html=''):
    with app.app_context():
        mail = Mail(app)
        msg = Message(title, recipients=RECIPIENTS)
        msg.body = body
        print('Отправка писем')
        mail.send(msg)
    print(f'Письма отправлены: {RECIPIENTS}')
    return

def check_fn_fill():
    fn_fill = 80 # уровень заполнения ФН в %
    kkm_list = get_kkm_filled_fn(fn_fill)
    if not kkm_list :
        print (f'ККМ с заполненностью ФН выше {fn_fill}% не найдено.')
        return
    max_fn_fill = max(int(i['fnSpaceUsed'].strip('%')) for i in kkm_list)
##    max_fn_fill = 96
    print('Максимальный уровень заполнения ФН: ', max_fn_fill)
    if max_fn_fill >= 99:
        title = '+++ ВСЁ! ЗВЕЗДЕЦ! ПРОШЛЯПИЛИ!!! >99% !!! +++'
    elif max_fn_fill >= 95:
        title = 'ВНИМАНИЕ !!! Заполненность > 95%'
    elif max_fn_fill >= 90:
        title = 'Внимание! Заполненность ФН > 90%'
    elif max_fn_fill >= 85:
        title = 'Заполненность ФН > 85%'
    elif max_fn_fill >= 80:
        title = 'Заполненность ФН > 80%'
    else:
        title = 'Заполненность ФН < 80%'
    text_list = []
    text_list.append('Внимание! Обнаружены ККМ с заполненностью ФН'
                                            ' выше {}%.\n'.format(max_fn_fill))
    for kkm in kkm_list:
        row = "{:4} {:39.37} {:31.30}".format(kkm['fnSpaceUsed'],
                                kkm['deviceName'], squeezed(kkm['clientName']))
        text_list.append(row)
    text = '\n'.join(text_list)

    send_mail(title=title, body=text)
    return

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'informersmart@yandex.ru'
app.config['MAIL_DEFAULT_SENDER'] = 'informersmart@yandex.ru'
app.config['MAIL_PASSWORD'] = 'Smart620514'

current_date = datetime.datetime.now()
print('Текущий день недели: ',current_date.isoweekday())
#if current_date.isoweekday() == 4:
if current_date.isoweekday() in [1, 2, 3, 4, 5, 6, 0]:
    check_fn_fill()

print('Завершение работы')

##if __name__ == '__main__':
##    check_fn_fill()
##    app.run(debug=False)