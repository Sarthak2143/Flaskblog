import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import json
from flask_mail import Mail
from flask_login import LoginManager

with open("config.json", "r") as f:
    data = json.loads(f.read())

app = Flask(__name__)
app.config['SECRET_KEY'] = data['secret-key']
app.config['SQLALCHEMY_DATABASE_URI'] = data['sqlite-db']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = data['email_id']
app.config['MAIL_PASSWORD'] = data['email_pwd']
mail = Mail(app)

from main import routes

