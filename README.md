# Python(Flask) blog application 

[![forthebadgemade-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

A responsive blog application written in python with the help of `flask` framework with multiple functionalities, app is like Twitter where various users can post anything.

## Features:

- Login/Registering of users
- Updating account info
- Reset password mail
- Posting content
- Updating posts
- Deleting posts
- Pagination
- Custom error pages

## Technologies used:

- Flask (as a framework)
- SQLAlchemy (for DB)
- Bootstrap (CSS Lib.)

### Running the application

1. Download the source code using `git`

```bash
git clone https://github.com/Sarthak2143/Flaskblog
cd Flaskblog/
```

2. Configuration

- Rename `demo_config.json` to `config.json`
- Open `config.json` in your editor.

It looks like this:

```json
{
  "secret-key": "something very secret here.",
  "sqlite-db": "sqlite:///site.db",
  "email_id": "youremail@gmail.com",
  "email_pwd": "password for your gmail account"
}
```

Change values according to you and save changes.

3. Install these required packages through `pip`.

```bash
flask
SQLAlchemy
flask-mail
flask-wtf
bcrypt
pillow
flask_SQLAlchemy
```
4. Start the app

```bash
python3 run.py
```

Visit `http://localhost:5000` in your browser to test app.

## Support

As always, you can support my work my starring my projects, following me on [Github](https://github.com/Sarthak2143) and on [Twitter](https://twitter.com/voldemort_shin).
