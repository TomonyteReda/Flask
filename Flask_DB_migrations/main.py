from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import os

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask("Flask3")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)


class Employees(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email_address = db.Column(db.String(120), unique=True)
    position = db.Column(db.String(120), nullable=False)

    def __init__(self, name, surname, position):
        self.name = name
        self.surname = surname
        self.position = position

    def __repr__(self):
        return f'{self.name} ({self.position}) - email:{self.email_address}'

