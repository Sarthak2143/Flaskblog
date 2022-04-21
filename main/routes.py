from flask import render_template, url_for, flash, redirect, request
from main.forms import RegistrationForm, LoginForm
from main.models import User, Post
from main import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
        {
            "author": "Sarthak Tomar",
            "title": "Post 1",
            "date_posted": "Feb 28 2022",
            "content": "My blog post, where i'll post my daily updates."
            },
        {
            "author": "John Doe",
            "title": "Post 2",
            "date_posted": "Feb 29 2022",
            "content": "My test blog post for testing our page."
            }
        ]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account have been successfully created! You are now able to Login!", "success")

        return redirect(url_for("login"))
    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been successfully logged in your account!", "success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been successfully logged out of your account!", "success")
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = 'Account')

