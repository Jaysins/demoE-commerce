# coding=utf-8

"""
Forms package
"""

from wtforms import StringField, PasswordField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm


class AddForm(FlaskForm):
    """
    Register
    """
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=30)])
    quantity = IntegerField('quantity', validators=[InputRequired()])
    price = IntegerField('price', validators=[InputRequired()])


class LoginForm(FlaskForm):
    """
    LoginForm
    """
    name = StringField('Username', validators=[
                           InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8)])
