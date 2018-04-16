from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class FoodModel(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    restaurant = db.relationship('RestaurantModel', backref=db.backref('foods', lazy='dynamic' ))

    def __init__(self, comment, restaurant_id):
        self.comment = comment
        self.restaurant_id = restaurant_id


class RestaurantModel(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class RestaurantSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class FoodSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    restaurant_id = fields.Integer(required=True)
    name = fields.String(required=True, validate=validate.Length(1))
    description = fields.String()
    creation_date = fields.DateTime()
