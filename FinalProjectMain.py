# Helmut Brenner #
# 2037275 #
# Dani Hargrove #
# 2037520 #
# Final Draft #

import hashlib
import flask
from flask import jsonify
from flask import request, make_response

import FinalProjectFunctions

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# HB
# Endpoint for Home Page: http://127.0.0.1:5000/
@app.route('/', methods=['GET'])
def home_base():
    # This is for the homepage of our project eventually.
    return 'This is our Final Project Home'


# HB
# Endpoint for authenticating a user: http://127.0.0.1:5000/api/authenticate
@app.route('/api/authenticate', methods=['GET'])
def authenticate_login():
    # Should automatically ask for auth. Must restart browser to re-prompt after successful login.
    if request.authorization:
        # Encode and hash the pass.
        encoded_pass = request.authorization.password.encode()
        hashed_pass = hashlib.sha256(encoded_pass)

        # Turn binary hash into hexadecimal
        hexa_hashed_pass = hashed_pass.hexdigest()

        # User provided username
        provided_username = request.authorization.username

        # Search DB for username query.
        get_combo_query = "SELECT * FROM users WHERE username='%s'" % provided_username

        # Connect to DB
        cnx = FinalProjectFunctions.connect()

        # Search and return user name and pass if found.
        db_user_pass = FinalProjectFunctions.execute_read_query(cnx, get_combo_query)

        # Checks the returned values for correctness.
        if db_user_pass[0]['username'] == provided_username and db_user_pass[0]['password'] == hexa_hashed_pass:
            return "<h1> Your login credentials are valid, Congratulations! </h1>"
        # If the authentication isn't correct then it re-prompts.
    return make_response('Incorrect username or password.', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


# HB
# Endpoint for getting all trips: http://127.0.0.1:5000/api/trip
@app.route('/api/trip', methods=["GET"])
def get_trip():
    # Retrieves all trips in the trip table. Destination id should come with it.
    get_trip_query = "SELECT * FROM trip"

    # Connect to DB
    cnx = FinalProjectFunctions.connect()

    # Execute SQL statement
    trip_dict = FinalProjectFunctions.execute_read_query(cnx, get_trip_query)

    # If no trips in the DB then this string returns.
    if len(trip_dict) == 0:
        return 'No trips in the database!'

    # If there are trips then they are returned here.
    return jsonify(trip_dict)


# DH
# Endpoint for adding a trip: http://127.0.0.1:5000/api/trip
@app.route('/api/trip', methods=["POST"])
def add_trip():
    # Retrieves input as a JSON body payload and then creates a new trip in the trip table.
    requested_data = request.get_json()
    trip_name = requested_data['trip_name']

    # In the end, this destination ID will be available by drop down menu which displays previously entered
    # destinations. For now it is received with the rest of the payload.
    destination_id = requested_data['destination_id']

    transportation = requested_data['transportation']
    leave_date = requested_data['leave_date']
    return_date = requested_data['return_date']
    depart_airport = requested_data['depart_airport']
    arrive_airport = requested_data['arrive_airport']

    # Add input to SQL trip query
    add_trip_query = "INSERT INTO trip (trip_name, destination_id, transportation, leave_date, " \
                     "return_date, depart_airport, arrive_airport) VALUES ('%s', %d, '%s', '%s', '%s', '%s', '%s');" % \
                     (trip_name, destination_id, transportation, leave_date, return_date, depart_airport,
                      arrive_airport)

    # Connect to DB
    cnx = FinalProjectFunctions.connect()

    # Execute the add_trip_query and return success or failure.
    result = FinalProjectFunctions.execute_query(cnx, add_trip_query)

    # Checks for success or failure.
    if result == 0:
        return "Trip added successfully."
    return "ERROR: Trip addition unsuccessful."


# DH
# Endpoint for updating a trip destination: http://127.0.0.1:5000/api/trip
# Based on user submitted trip id
@app.route('/api/trip', methods=["PUT"])
def update_trip():
    # Retrieves input as a JSON body payload and then updates and existing trip in the trip table.
    requested_data = request.get_json()
    trip_id = requested_data['trip_id']

    # In the end, this destination ID will be available by drop down menu which displays previously entered
    # destinations. For now it is received with the rest of the payload.
    new_destination_id = requested_data['destination_id']

    update_destination_query = "UPDATE trip SET destination_id=%d WHERE trip_id=%d" % \
                               (new_destination_id, trip_id)

    # Connect to DB
    cnx = FinalProjectFunctions.connect()

    # Execute the update_destination_query and return success or failure.
    result = FinalProjectFunctions.execute_query(cnx, update_destination_query)

    # Checks for success or failure.
    if result == 0:
        return "Trip destination updated successfully."
    return "ERROR: Trip update unsuccessful."


# HB
# Endpoint for deleting a trip: http://127.0.0.1:5000/api/trip
@app.route('/api/trip', methods=["DELETE"])
def delete_trip():
    # Retrieves a trip id from the user and deletes the corresponding trip from the table
    requested_data = request.get_json()
    trip_id_to_delete = requested_data['trip_id']

    # Create MySQL statement
    delete_trip_query = "DELETE FROM trip WHERE trip_id=%d" % trip_id_to_delete

    # Connect to DB
    cnx = FinalProjectFunctions.connect()

    # Execute delete query on DB
    result = FinalProjectFunctions.execute_query(cnx, delete_trip_query)

    # Checks for success or failure.
    if result == 0:
        return "Trip deleted successfully."
    return "ERROR: Trip deletion unsuccessful."


# DH
# Endpoint for viewing all destinations: http://127.0.0.1:5000/api/destination
@app.route('/api/destination', methods=["GET"])
def get_destination():
    # Retrieves information from the destination table
    get_destination_query = "SELECT * FROM destination"

    # Connect to DB
    cnx = FinalProjectFunctions.connect()

    destination_dict = FinalProjectFunctions.execute_read_query(cnx, get_destination_query)
    # If no destinations in the DB then this string returns.
    if len(destination_dict) == 0:
        return 'No destinations in the database!'

    # If there are destinations then they are returned here.
    return jsonify(destination_dict)


# DH
# Endpoint for adding destination: http://127.0.0.1:5000/api/destination
@app.route('/api/destination', methods=["POST"])
def add_destination():
    # Retrieves input as a JSON body payload and then creates a new destination in the destination table.
    requested_data = request.get_json()
    country = requested_data['country']
    city = requested_data['city']
    sightseeing = requested_data['sightseeing']

    # Add input to MySQL query
    add_trip_query = "INSERT INTO destination (country, city, sightseeing) VALUES ('%s', '%s', '%s');" % \
                     (country, city, sightseeing)

    # Connect to DB
    cnx = FinalProjectFunctions.connect()

    # Execute Query
    result = FinalProjectFunctions.execute_query(cnx, add_trip_query)

    # Checks for success.
    if result == 0:
        return "Destination added successfully."
    return "ERROR: Destination addition unsuccessful."


# HB
# Endpoint for updating destination: http://127.0.0.1:5000/api/destination
@app.route('/api/destination', methods=["PUT"])
def update_destination():
    # Same update code and functionality from the other update query. Takes a destination ID you want to change and
    # the country you wish to change the column to.
    requested_data = request.get_json()
    destination_id = requested_data['destination_id']

    new_destination_country = requested_data['country']

    # Query to update row in destination table.
    update_destination_query = "UPDATE destination SET country='%s' WHERE destination_id=%d" % \
                               (new_destination_country, destination_id)

    # Connect to DB
    cnx = FinalProjectFunctions.connect()

    # Execute the update_destination_query and return success or failure.
    result = FinalProjectFunctions.execute_query(cnx, update_destination_query)

    # Checks for success or failure.
    if result == 0:
        return "Destination updated successfully."
    return "ERROR: Destination update unsuccessful."


# BH
# Endpoint for adding destination: http://127.0.0.1:5000/api/destination
@app.route('/api/destination', methods=["DELETE"])
def delete_destination():
    # Retrieves a trip id from the user and deletes the corresponding trip from the table
    cnx = FinalProjectFunctions.connect()
    requested_data = request.get_json()

    # Gets the destination ID to delete from user in the form of a JSON body payload.
    destination_id_to_delete = requested_data['destination_id']

    # Construct the query.
    delete_destination_query = "DELETE FROM destination WHERE destination_id=%d" % destination_id_to_delete

    # Execute Query
    result = FinalProjectFunctions.execute_query(cnx, delete_destination_query)

    # Checks for success.
    if result == 0:
        return "Destination deleted successfully."
    return "ERROR: Destination deletion unsuccessful."


app.run()
