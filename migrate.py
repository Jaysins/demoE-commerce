# coding=utf-8
"""
Migrate
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import UserMixin
import datetime

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)


class Goods(db.Model):
    """
    Goods
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    image = db.Column(db.String(255))


class Sold(db.Model):
    """
    Sold
    """
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('goods.id'))
    date = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)


if __name__ == '__main__':
    manager.run()
