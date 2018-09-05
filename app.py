# coding=utf-8

"""
Project
"""

from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadNotAllowed, UploadSet, configure_uploads, IMAGES
from wtforms import StringField, PasswordField, validators, IntegerField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm

import os

app = Flask(__name__)

app.config.from_pyfile('config.py')

photos = UploadSet('photos', IMAGES)

configure_uploads(app, photos)

db = SQLAlchemy(app)

temp_cart = []

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


class AddForm(FlaskForm):
    """
    Register
    """
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=30)])
    quantity = IntegerField('quantity', validators=[InputRequired()])
    price = IntegerField('price', validators=[InputRequired()])


@app.route('/')
def index():
    """
    Index
    """
    all_goods = Goods.query.all()
    return render_template('index.html', all_goods=all_goods, length=len(all_goods))


@app.route('/add', methods=['GET', 'POST'])
def add():
    """

    :return:
    """
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        data = request.form
        filename = 'item-10.jpg'
        if 'image' in request.files:
            photo = request.files['image']
            try:
                check_fold = os.path.isfile(
                    os.path.abspath(os.getcwd()) + '/' + app.config['UPLOADED_PHOTOS_DEST'] + '/' + photo.filename)
                if check_fold is not False:
                    filename = str(photo.filename)
                else:
                    filename = photos.save(photo)
            except UploadNotAllowed:
                return redirect(url_for('error', message='INVALID FILE UPLOAD'))
        good = Goods(name=data['name'], price=data['price'], quantity=data['quantity'], image=filename)
        db.session.add(good)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('add.html', form=form)


@app.route('/cart')
def cart():
    """

    :return:
    """
    return render_template('cart.html', temp_cart=temp_cart)


@app.route('/add_to_cart')
def add_to_cart():
    """

    :return:
    """
    items = Goods.query.filter_by(id=int(request.args['id'])).first()
    if not items:
        return jsonify({'response': 'failed'})
    return jsonify({'response': 'success', 'id': items.id, 'name': items.name, 'quantity': items.quantity, 'price': items.price, 'image': items.image})


@app.route('/error/<message>')
def error(message):
    """

    :param message:
    :return:
    """
    return f"<h1> {message} </h1>"


if __name__ == '__main__':
    app.run(debug=True)
