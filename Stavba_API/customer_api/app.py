from flask import Flask, jsonify, request, make_response

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

# Vrácení všech zákazníků
@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers)

# Vrácení konkrétního zákazníka
@app.route('/customer/<string:username>', methods=['GET'])
def get_customer(username):
    for customer in customers:
        if customer['username'] == username:
            return jsonify(customer), 200
    return jsonify({'message': 'customer not found'}), 404

# Vytvoření nového zákazníka
@app.route('/customer', methods=['POST'])
def create_customer():
    request_data = request.get_json()
    new_customer = {
        "email": request_data['email'],
        "username": request_data['username'],
        "name": request_data['name'],
        "newsletter_status": request_data['newsletter_status'],
        "trips": []
    }

    for customer in customers:
        if customer['username'] == new_customer['username']:
            return jsonify({'error': 'username already exist'}), 409

    customers.append(new_customer)
    return jsonify(new_customer), 201

# Uprava zákazníka
@app.route('/customer/<string:username>', methods=['PUT'])
def update_customer(username):
    request_data = request.get_json()
    updated_customer = {
        "email": request_data['email'],
        "name": request_data['name'],
        "newsletter_status": request_data['newsletter_status'],
        "trips": []
    }

    for customer in customers:
        if customer['username'] == username:
            customer.update(updated_customer)
            return jsonify({'message': 'customer updated'},updated_customer), 200


    new_customer = updated_customer.copy()
    new_customer['username'] = username
    new_customer.update(new_customer)

    customers.append(new_customer)
    return jsonify({'message': 'customer created'}, new_customer), 201


# Vymazání zákazníka
@app.route('/customer/<string:username>', methods=['DELETE'])
def delete_customer(username):
    for customer in customers:
        if customer['username'] == username:
            customers.remove(customer)
            return jsonify({'message': str('customer: '+username+ ' was deleted.')}), 200
    return jsonify({'message': str('customer: '+username+ ' not found.')}), 404

# Vrácení všech zájezdů pod zákazníkem
@app.route('/customer/<string:username>/trips', methods=['GET'])
def get_customer_trip(username):
    for customer in customers:
        if customer['username'] == username:
            return jsonify({'trips': customer['trips']})
    return jsonify({'message': 'customer not found'}), 404

# Vytvoření zájezdu pod zákazníkem
@app.route('/customer/<string:username>/trips', methods=['POST'])
def create_customer_trip(username):
    for customer in customers:
        if customer['username'] == username:
            request_data = request.get_json()
            new_customer_trip = {
                "destination": request_data['destination'],
                "price": request_data['price']
            }

            customer['trips'].append(new_customer_trip)
            return new_customer_trip, 201
    return jsonify({'message': 'customer not found'}),404






app.run(port=3333, debug=True)

