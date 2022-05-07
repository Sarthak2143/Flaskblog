from flask import render_template, request, Blueprint
from main.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 7, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=count)

    return render_template("home.html", posts=posts)

@main.route("/about")
def about():
    return render_template("about.html", title = "About")
