from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HomePage(Resource):
    def get(self):
        return "Hello Flask-RESTful!"


api.add_resource(HomePage, '/')


app.run(port=3333)





