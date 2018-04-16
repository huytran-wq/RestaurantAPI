from flask import request
from flask_restful import Resource
from model import db, RestaurantModel, RestaurantSchema

restaurants_schema = RestaurantSchema(many=True)
restaurant_schema = RestaurantSchema()

class RestaurantResource(Resource):
    def get(self):
        restaurants = RestaurantModel.query.all()
        restaurants = restaurants_schema.dump(restaurants).data
        return {'status': 'success', 'data': restaurants}, 200


    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = restaurant_schema.load(json_data)
        if errors:
            return errors, 422
        restaurant = RestaurantModel.query.filter_by(name=data['name']).first()
        if restaurant:
            return {'message': 'Restaurant already exists'}, 400
        restaurant = RestaurantModel(
            name=json_data['name']
            )

        db.session.add(restaurant)
        db.session.commit()

        result = restaurant_schema.dump(restaurant).data

        return { "status": 'success', 'data': result }, 201


    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = restaurant_schema.load(json_data)
        if errors:
            return errors, 422
        restaurant = RestaurantModel.query.filter_by(id=data['id']).first()
        if not restaurant:
            return {'message': 'Category does not exist'}, 400
        restaurant.name = data['name']
        db.session.commit()

        result = restaurant_schema.dump(restaurant).data

        return { "status": 'success', 'data': result }, 204


    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = restaurant_schema.load(json_data)
        if errors:
            return errors, 422
        category = RestaurantSchema.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = restaurant_schema.dump(category).data

        return { "status": 'success', 'data': result}, 204
