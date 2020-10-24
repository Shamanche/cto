from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'informersmart@yandex.ru'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'informersmart@yandex.ru'  # и здесь
app.config['MAIL_PASSWORD'] = 'Smart620514'  # введите пароль

with app.app_context():
    mail = Mail(app)
    msg = Message("Subject", recipients=['tsvet005@yandex.ru'])
    msg.body = ' test message body'
    mail.send(msg)