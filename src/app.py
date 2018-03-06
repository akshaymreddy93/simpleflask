from flask import Flask, render_template, request

#Mappers
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from sqlalchemy import create_engine
from mongoengine import *

#Local
from forms import Login


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


@app.route('/', methods = ['GET','POST'])
def home():
    form = Login(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        s = select([Users])
        result = conn.execute(s)
        validation = result.fetchone()
        if username == validation[1] and password == validation[2]:
            return render_template('search.html')
        else:
            return render_template('home.html', message = {'error':'Invalid Login'}, form = form)
    return render_template('home.html', form = form)

if __name__ == '__main__' :
    app.run(debug=True)
