#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)
    
    #  creating a patch method
    def patch(self, id):
        # querying ad filtering the plants table by the id
        plant = Plant.query.filter_by(id = id).first()

        data = request.get_json()
        #  setting attribute using a for loop and data
        for attr in data:
            setattr(plant, attr, data[attr])

        #  adding and commiting the updated record to the db
        db.session.add(plant)
        db.session.commit()

        # using to_dict() to convert the updated plant to a dictionary
        plant_dict = plant.to_dict()

        # creating and returning a response
        response = make_response(plant_dict, 200, {"Content-Type": "application/json"})
        return response
    
    # creating a delete method
    def delete(self, id):
        # querying ad filtering the plants table by the id
        plant = Plant.query.filter_by(id = id).first()

        #  deleting and commiting the plant changes to the db
        db.session.delete(plant)
        db.session.commit()

        #  creating a message to show that deleion was successful 
        delete_message = {
            "message" : "Internal Server Error"
        }
        # creating and returning a response
        response = make_response(delete_message, 204)
        return response
    


api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
