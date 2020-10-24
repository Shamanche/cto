from flask import Flask
from funcs import *
from flask_mail import Mail, Message

# адреса почту кому будет приходить уведомление
RECIPIENTS = [
    'td@21smart.ru',
    'tsvet005@yandex.ru']

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'informersmart@yandex.ru'
app.config['MAIL_DEFAULT_SENDER'] = 'informersmart@yandex.ru'
app.config['MAIL_PASSWORD'] = 'Smart620514'

@app.route('/', methods=['get'])
def index():
    message = "Hi! It is CTO - Informer."
    return message

def send_fn_fill(fn_fill=80): # уровень заполнения ФН в %
    kkm_list = get_kkm_filled_fn(fn_fill)
    if not kkm_list :
        print (f'ККМ с заполненностью ФН выше {fn_fill}% не найдено.')
        return
    text_list = []
    text_list.append( f'ККМ с заполненностью ФН выше {fn_fill}%.\n')
    for kkm in kkm_list:
        row = "{:4} {:39.37} {:31.30}".format(kkm['fnSpaceUsed'],
                                kkm['deviceName'], squeezed(kkm['clientName']))
        text_list.append(row)
    text = '\n'.join(text_list)
    with app.app_context():
        mail = Mail(app)
        msg = Message(f"Заполнение ФН более {fn_fill}%", recipients=RECIPIENTS)
        msg.body = text
        print('Отправка писем')
        mail.send(msg)
    print(f'Найдено {len(kkm_list)} ККМ с заполнением ФН более {fn_fill}%')
    print(f'Отправлено писем: {len(RECIPIENTS)}')
    return



if __name__ == '__main__':
    send_fn_fill(85)
    app.run(debug=False)