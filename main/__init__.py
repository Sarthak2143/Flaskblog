from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import json
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

from main import routes

