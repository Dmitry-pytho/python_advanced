from faker import Faker

from flask import Flask, jsonify, redirect, render_template, request, url_for

from flask_sqlalchemy import SQLAlchemy

fake = Faker()

DATABASE = "users.db"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User %r>' % self.name


@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/users/all")
def users_all():
    users = User.query.all()
    users_list = [dict(id=user.id, name=user.name, email=user.email)
                  for user in users]
    return jsonify(users_list)


@app.route("/users/gen")
def users_gen():
    usr = User(name=fake.name(), email=fake.email())
    db.session.add(usr)
    db.session.commit()
    return redirect(url_for('users_all'))


@app.route("/users/delete-all")
def users_del_all():
    User.query.delete()
    db.session.commit()

    return redirect(url_for('users_all'))


@app.route("/users/count")
def users_count():
    numbers = User.query.count()
    return jsonify({"count": numbers})


@app.route("/users/add", methods=['GET', 'POST'])
def users_add():
    if request.method == "GET":
        return render_template("user_add.html")
    else:
        name = request.form["user_name"]
        email = request.form["email"]
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('users_all'))
