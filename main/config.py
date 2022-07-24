import json

with open('config.json', 'r') as f:
    data = json.loads(f.read())

class Config:
    SECRET_KEY = data['secret-key']
    SQLALCHEMY_DATABASE_URI = data['sqlite-db']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = data['email_id']
    MAIL_PASSWORD = data['email_pwd']

