from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse

customers = [
             {
              "email" : "jan.novak@example.cz",
              "username" : "johny",
              "name" : "Jan Novák",
              "newsletter_status" : True,
              "trips" : [
                            {
                             "destination" : "Oslo, Norway",
                             "price" : 150.00
                            },
                            {
                             "destination" : "Bangkok, Thailand",
                             "price" : 965.00
                            }
                          ]
             },
             {
              "email" : "ivan.opletal@example.com",
              "username" : "ivan123",
              "name" : "Ivan Opletal",
              "newsletter_status" : False,
              "trips" : []
             }
        ]

app = Flask(__name__)
api = Api(app)

# Vrácení všech zákazníků RESTful
class Customers(Resource):
    def get(self):
        return {'customers': customers}, 200

class Customer(Resource):
    # stené jako funkce get_customer() z minulé verze
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('newsletter_status', type=bool, required=True)
    def get(self, username):
        for customer in customers:
            if customer['username'] == username:
                return customer, 200
        return {'message': 'username not found'}, 404

    # create_customer
    def post(self, username):
        data = self.parser.parse_args()
        new_customer = {
            "email": data['email'],
            "username": username,
            "name": data['name'],
            "newsletter_status": data['newsletter_status'],
            "trips": []
        }

        for customer in customers:
            if customer['username'] == new_customer['username']:
                return {'error': 'username already exist'}, 409

        customers.append(new_customer)
        return new_customer, 201

    # Uprava zákazníka
    # update_customer
    def put(self, username):
        data = self.parser.parse_args()
        updated_customer = {
            "email": data['email'],
            "username": username,
            "name": data['name'],
            "newsletter_status": data['newsletter_status'],
            "trips": []
        }

        for customer in customers:
            if customer['username'] == updated_customer['username']:
                customer.update(updated_customer)
                return ({'message': 'customer updated'},updated_customer), 200

        customers.append(updated_customer)
        return ({'message': 'customer created'},updated_customer), 201

    # Vymazání zákazníka
    # delete_customer
    def delete(self,username):
        for customer in customers:
            if customer['username'] == username:
                customers.remove(customer)
                return {'message': str('customer: ' + username + ' was deleted.')}, 200
        return {'message': str('customer: ' + username + ' not found.')}, 404



class Trips(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('destination', type=str, required=True)
    parser.add_argument('price', type=float, required=True)

    # Vrácení všech zájezdů pod zákazníkem
    # get_customer_trip
    def get(self, username):
        for customer in customers:
            if customer['username'] == username:
                return {'trips': customer['trips']}
        return {'message': 'customer not found'}, 404

    # Vytvoření zájezdu pod zákazníkem
    # create_customer_trip
    def post(self, username):
        data = self.parser.parse_args()
        new_customer_trip = {
            "destination": data['destination'],
            "price": data['price']
        }
        for customer in customers:
            if customer['username'] == username:
                customer['trips'].append(new_customer_trip)
                return ({'message': str('New trip added to customer: '+username+'.')},new_customer_trip), 201
        return {'message': 'customer not found'}, 404


api.add_resource(Customers, '/customers')
api.add_resource(Customer, '/customer/<string:username>')
api.add_resource(Trips, '/customer/<string:username>/trips')

app.run(port=3333, debug=True)

