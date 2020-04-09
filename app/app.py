from flask import Flask
from config import configuration
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(configuration)


token = '1077120736:AAFmq-ZM5pCAMMqFLxv5AbbdkOaQ25KggJg'
main_url = f'https://api.telegram.org/bot{token}/'




db = SQLAlchemy(app)