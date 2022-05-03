import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from main.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from main.models import User, Post
from main import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 7, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=count)

    return render_template("home.html", posts=posts)

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


def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_fname = random_hex + f_ext
    pic_path = os.path.join(app.root_path, "static/profile_pics", pic_fname)

    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)

    return pic_fname

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been successfully updated.", "success")
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form=form)


@app.route("/account/delete", methods=['GET', 'POST'])
@login_required
def delete_account():
    user = User.query.filter_by(username=current_user.username).first()
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 5, type=int)
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=count)
    for post in posts.items:
        db.session.delete(post)
        db.session.commit()

    db.session.delete(user)
    db.session.commit()
    flash('Your account have been deleted!', 'warning')
    return redirect(url_for('home'))



@app.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post have been created!', "success")
        return redirect(url_for('home'))
    return render_template('post_op.html', title = 'New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post have been updated!", "success")
        return redirect(url_for('post', post_id = post.id))

    elif request.method == 'GET':

        form.title.data = post.title
        form.content.data = post.content

    return render_template('post_op.html', title='Update Post', form=form, legend = 'Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Your post have been deleted!", "success")
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 5, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=count)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Mail", sender="noreply@flaskblog.com", recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not made this request, then simply ignore this mail and no changes will be made.
"""
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('This token is expired or invalid!', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f"Your password has been updated! You are now able to Login!", "success")
        return redirect(url_for('login'))

    return render_template('reset_token.html', title='Reset Password', form=form)



@app.route("/admin")
@login_required
def admin_page():
    if current_user.username != "admin":
        abort(403)

    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 7, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=count)
    return render_template("admin.html", title="Admin page", posts=posts)


@app.route("/admin/post/<int:post_id>")
@login_required
def admin_post(post_id):

    if current_user.username != "admin":
        abort(403)
    
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 7, type=int)
    post = Post.query.get_or_404(post_id)
    return render_template("admin_post.html", post=post)


@app.route("/admin/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def admin_update_post(post_id):

    if current_user.username != "admin":
        abort(403)

    post = Post.query.get_or_404(post_id) 
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post have been updated!", "success")
        return redirect(url_for('post', post_id = post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('admin_post_op.html', title='Update Post', form=form, legend = 'Update Post')


@app.route('/admin/post/<int:post_id>/delete', methods=['POST'])
@login_required
def admin_delete_post(post_id):
    
    if current_user.username != "admin":
        abort(403)

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Your post have been deleted!", "success")
    return redirect(url_for('admin_page'))
