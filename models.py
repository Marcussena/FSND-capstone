import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import json

database_name = "agency"
#database_path = 'postgresql://postgres:postgres@localhost:5432/agency'
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()
moment = Moment()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    moment.app = app
    db.init_app(app)
    db.create_all()

'''

    Actor class (name, age and gender)

'''

class Actor(db.Model):

    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    '''
    Setting CRUD operations

    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    method that returns info about a Actor

    '''

    def summarize(self):
        return{
            'id': self.id,
            'actor_name': self.name,
            'actor_age': self.age,
            'actor_gender': self.gender
        }
'''

    Movie class (title and release date)

'''
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    '''
    CRUD operations

    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    method that returns info about a Movie

    '''

    def summarize(self):
        return{
            'movie': self.title,
            'release_date': self.release_date
        }
