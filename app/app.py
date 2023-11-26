#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# routes

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_data = [
        {'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address}
        for restaurant in restaurants
    ]
    return jsonify(restaurant_data)

@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if not restaurant:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)

    pizzas = [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in restaurant.pizzas]

    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'pizzas': pizzas
    }

    return jsonify(restaurant_data)

@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if not restaurant:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)

    # Delete associated RestaurantPizza entries
    RestaurantPizza.query.filter_by(restaurant_id=restaurant.id).delete()

    # Delete the restaurant
    db.session.delete(restaurant)
    db.session.commit()

    return '', 204  # Empty response with 204 status code

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_data = [
        {'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}
        for pizza in pizzas
    ]
    return jsonify(pizza_data)

if __name__ == '__main__':
    app.run(port=5555)



























# from flask import Flask, make_response
# from flask_migrate import Migrate

# from models import db, Restaurant

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/')
# def home():
#     return ''


# if __name__ == '__main__':
#     app.run(port=5555)
