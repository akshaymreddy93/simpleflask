from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

#Mappers
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import create_engine
from mongoengine import *

#Local
from forms import Login, SearchForm

app = Flask(__name__)  # Setting up the flask application

# MySQL Database and SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql9224878:4sLR1fLK9s@sql9.freemysqlhosting.net/sql9224878'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('mysql+pymysql://sql9224878:4sLR1fLK9s@sql9.freemysqlhosting.net/sql9224878', echo=True)
conn = engine.connect()

# Instatiating the application
db = SQLAlchemy(app)

#Connect mongodb
connect('local')

# User Mapper Class (SQLAlchemy)
class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.Unicode)
    password = db.Column('password', db.Unicode)

    # Inserting via ORM
    def __init__(self, id, username, password):
        db.id = id
        db.username = username
        db.password = password


# mongodb
class Basic(DynamicDocument):
    nconst = StringField(required=True)
    primaryName = StringField(required=True)
    birthYear = StringField(required=True)
    deathYear = StringField(required=True)
    primaryProfession = StringField(required=True)
    knownForTitles = StringField(required=True)


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('LoginPage'))
    return wrap


#Login
@app.route('/', methods = ['GET','POST'])
def LoginPage():
    message = ""
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        s = select([Users])
        result = conn.execute(s)
        validation = result.fetchone()
        if username == validation[1] and password == validation[2]:
            session['logged_in'] = True
            return redirect(url_for('search'))
        else:
            return render_template('home.html', form = form, message = 'Invalid Credentials')
    return render_template('home.html', form = form)


#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('LoginPage'))


#Search
@app.route('/search', methods = ['GET','POST'])
@is_logged_in
def search():
    search = ""
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        search = form.search.data

    return render_template('search.html', form=form, search = search)


if __name__ == '__main__' :
    app.secret_key='demo123'
    app.run(debug=True)
