# coding=utf-8
"""
Config
"""

import os

# file_path = os.path.abspath(os.getcwd()) + "\service.db"

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'thisisasecret'
UPLOADED_PHOTOS_DEST = 'static/img'
