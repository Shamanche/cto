from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'test@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'test@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = 'password'  # введите пароль