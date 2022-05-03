from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username",
            validators = [DataRequired(), Length(min=4, max = 15)])

    email = StringField("Email",
            validators = [DataRequired(), Email()])

    password = PasswordField("Password",
            validators = [DataRequired()])

    confirm_password = PasswordField("Confirm Password",
            validators = [DataRequired(), EqualTo('password')])

    
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

class LoginForm(FlaskForm):
    
    email = StringField("Email",
            validators = [DataRequired(), Email()])

    password = PasswordField("Password",
            validators = [DataRequired()])
    
    remember = BooleanField("Remember Me")

    submit = SubmitField("Sign In")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
            validators = [DataRequired(), Length(min=4, max = 15)])

    email = StringField("Email",
            validators = [DataRequired(), Email()])

    picture = FileField("Update Profile Picture",
            validators = [FileAllowed(["png", "jpg", "jpeg"])])

    submit = SubmitField("Update")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if username.data != current_user.username:
            if user:
                raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if email.data != current_user.email:
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Title"})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Content"})
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",
            validators = [DataRequired()])

    confirm_password = PasswordField("Confirm Password",
            validators = [DataRequired(), EqualTo('password')])

    submit = SubmitField('Reset Password')

