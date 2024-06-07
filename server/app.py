#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries=[]
    for bakery in Bakery.query.all():
        bakeries.append(bakery.to_dict())
    return make_response(bakeries)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    return make_response(bakery.to_dict())
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods=[]
    for good in BakedGood.query.order_by(BakedGood.price.desc()):
        goods.append(good.to_dict())
    return make_response(goods)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return (jsonify(most_expensive_good.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
