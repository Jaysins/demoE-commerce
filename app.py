# coding=utf-8

"""
Project
"""

import datetime
import os
from flask import Flask, render_template, url_for, request, redirect, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_uploads import UploadNotAllowed, UploadSet, configure_uploads, IMAGES

from forms import LoginForm, AddForm

app = Flask(__name__)

app.config.from_pyfile('config.py')

photos = UploadSet('photos', IMAGES)

configure_uploads(app, photos)

db = SQLAlchemy(app)


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


@app.route('/')
def index():
    """
    Index
    """
    check_length = Goods.query.all()
    all_goods = Goods.query.order_by(Goods.id.desc()).limit(6).all()
    if len(all_goods) <= 1:
        all_goods = 'No Items yet.'

    return render_template('index.html', all_goods=all_goods, length=len(check_length))


@app.route('/all_products')
def all_products():
    """
    Index
    """
    check_length = Goods.query.all()
    all_goods = Goods.query.order_by(Goods.id.desc()).limit(6).all()
    if len(all_goods) <= 1:
        all_goods = 'No Items yet.'

    return render_template('allProducts.html', all_goods=all_goods, length=len(check_length))


# :TODO WORK ON
@app.route('/products/<int:page_id>')
def products(page_id):
    """
    products
    """
    check_length = Goods.query.all()
    # :TODO FIGURE THIS OUT BRO
    all_goods = Goods.query.order_by(Goods.id.desc()).limit(6).all()
    prev = page_id * 6
    next = page_id * 2
    all_goods2 = Goods.query.filter(Goods.id > page_id*6).order_by(Goods.id.desc()).limit(6).all()
    pages = 1
    length = len(check_length)
    while True:
        if length % pages != 0:
            break
        pages += 1
    print(pages)
    return render_template('product.html', all_goods=all_goods2, length=length, pages=pages)


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
        good = Goods(name=data['name'].title(), price=data['price'], quantity=data['quantity'], image=filename)
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
    return render_template('cart.html')


@app.route('/add_to_cart')
def add_to_cart():
    """

    :return:
    """
    items = Goods.query.filter_by(id=int(request.args['id'])).first()
    if not items:
        return jsonify({'response': 'failed'})
    return jsonify(
        {'response': 'success', 'id': items.id, 'name': items.name, 'quantity': items.quantity, 'price': items.price,
         'image': items.image})


@app.route('/error/<message>')
def error(message):
    """

    :param message:
    :return:
    """
    return f"<h1> {message} </h1>"


@app.route('/search', methods=['POST'])
def search():
    print(request.form)
    result = Goods.query.filter(Goods.name.like("%{}%".format(request.form['search-product'].title()))).all()
    if 1 > len(result):
        result = 'No result'
    return render_template('index.html', all_goods=result, length=len(result))


@app.route('/sale')
def sale():
    """

    :return:
    """
    data = json.loads(request.args['cart'])
    total_cost = []
    for i in data:
        check_good = Goods.query.filter_by(name=i[1], id=int(i[0])).first()
        if check_good:
            quantity = int(i[2])
            if check_good.quantity >= quantity:
                check_good.quantity -= quantity
                total_cost.append(check_good.price * quantity)
                isold = Sold(product=int(i[0]), quantity=quantity, date=datetime.datetime.now())
                db.session.add(isold)

    db.session.commit()
    total_cost = sum(total_cost)
    return jsonify({'response': 'success', 'cost': total_cost})


if __name__ == '__main__':
    app.run(debug=True)
