import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from main import mail

def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_fname = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, "static/profile_pics", pic_fname)

    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)

    return pic_fname

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Mail", sender="noreply@flaskblog.com", recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not made this request, then simply ignore this mail and no changes will be made.
"""
    mail.send(msg)
