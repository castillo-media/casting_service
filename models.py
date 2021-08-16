import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


# environment variable for deployment
database_path = os.environ.get('DATABASE_URL')

# database for local development
# database_path = "postgresql://{}/{}".format('localhost:5432', 'agency')

# This is a hack to help Heroku replace the database dialect
# from postgres (no longer supported) to postgresql (supported)
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Person(db.Model):
    __tablename__ = 'People'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    catchphrase = Column(String)

    def __init__(self, name, catchphrase=""):
        self.name = name
        self.catchphrase = catchphrase

    def update(self):
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'catchphrase': self.catchphrase}


class Movie(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    release = Column(String)

    def __init__(self, name, release=""):
        self.name = name
        self.release = release

    def update(self):
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'release': self.release}
