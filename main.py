from flask import Flask, render_template, request, jsonify, redirect, url_for
from sql import create_connection, execute_query, execute_read_query
import os

app = Flask(__name__)

# Database connection
db_conString = os.getenv('DB_CONSTRING')
db_userName = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
conn = create_connection(db_conString, db_userName, db_password, db_name)
cursor = conn.cursor()

# Pre-configured username and password (for demonstration purposes)
valid_username = 'admin'
valid_password = 'mypassword'

# Homepage route
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Render floors page
@app.route('/floors', methods=['GET'])
def render_floors():
    query = "SELECT * FROM floor;"
    result = execute_read_query(conn, query)
    return render_template('floors.html', floors=result)

# Create a new floor
@app.route('/api/floors', methods=['POST'])
def add_floor():
    data = request.get_json()
    level = data.get('level')
    name = data.get('name')

    query = f"INSERT INTO floor (level, name) VALUES ({level}, '{name}')"
    execute_query(conn, query)
    conn.commit()

    return jsonify({'message': 'Floor added successfully'}), 200

# Retrieve all floors
@app.route('/api/floors', methods=['GET'])
def get_floors():
    query = "SELECT * FROM floor;"
    result = execute_read_query(conn, query)
    return jsonify(result), 200

# Update a floor by ID
@app.route('/api/floors/<int:floor_id>', methods=['PUT'])
def update_floor(floor_id):
    data = request.get_json()
    level = data.get('level')
    name = data.get('name')
    query = f"UPDATE floor SET level={level}, name='{name}' WHERE id={floor_id}"
    execute_query(conn, query)
    return jsonify({"message": f"Floor {floor_id} updated successfully"}), 200

# Delete a floor by ID
@app.route('/api/floors/<int:floor_id>', methods=['DELETE'])
def delete_floor(floor_id):
    query = f"DELETE FROM floor WHERE id={floor_id}"
    execute_query(conn, query)
    return jsonify({"message": f"Floor {floor_id} deleted successfully"}), 200

# Render rooms page
@app.route('/rooms', methods=['GET'])
def render_rooms():
    query = "SELECT * FROM room;"
    result = execute_read_query(conn, query)
    return render_template('rooms.html', rooms=result)

# Render residents page
@app.route('/residents', methods=['GET'])
def render_residents():
    query = "SELECT * FROM resident;"
    result = execute_read_query(conn, query)
    return render_template('residents.html', residents=result)

# Create a new room
@app.route('/api/rooms', methods=['POST'])
def add_room():
    data = request.get_json()
    capacity = data.get('capacity')
    number = data.get('number')
    floor_id = data.get('floor_id')

    query = f"INSERT INTO room (capacity, number, floor_id) VALUES ({capacity}, {number}, {floor_id})"
    execute_query(conn, query)
    conn.commit()

    return jsonify({'message': 'Room added successfully'}), 200

# Retrieve all rooms
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    query = "SELECT * FROM room;"
    result = execute_read_query(conn, query)
    return jsonify(result), 200

# Update a room by ID
@app.route('/api/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.get_json()
    capacity = data.get('capacity')
    number = data.get('number')
    floor_id = data.get('floor_id')
    query = f"UPDATE room SET capacity={capacity}, number={number}, floor_id={floor_id} WHERE id={room_id}"
    execute_query(conn, query)
    return jsonify({"message": f"Room {room_id} updated successfully"}), 200

# Delete a room by ID
@app.route('/api/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    query = f"DELETE FROM room WHERE id={room_id}"
    execute_query(conn, query)
    return jsonify({"message": f"Room {room_id} deleted successfully"}), 200

# Create a new resident
@app.route('/api/residents', methods=['POST'])
def add_resident():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    age = data.get('age')
    room_id = data.get('room_id')

    query = f"INSERT INTO resident (firstname, lastname, age, room_id) VALUES ('{firstname}', '{lastname}', {age}, {room_id})"
    execute_query(conn, query)
    conn.commit()

    return jsonify({'message': 'Resident added successfully'}), 200

# Retrieve all residents
@app.route('/api/residents', methods=['GET'])
def get_residents():
    query = "SELECT * FROM resident;"
    result = execute_read_query(conn, query)
    return jsonify(result), 200

# Update a resident by ID
@app.route('/api/residents/<int:resident_id>', methods=['PUT'])
def update_resident(resident_id):
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    age = data.get('age')
    room_id = data.get('room_id')
    query = f"UPDATE resident SET firstname='{firstname}', lastname='{lastname}', age={age}, room_id={room_id} WHERE id={resident_id}"
    execute_query(conn, query)
    return jsonify({"message": f"Resident {resident_id} updated successfully"}), 200

# Delete a resident by ID
@app.route('/api/residents/<int:resident_id>', methods=['DELETE'])
def delete_resident(resident_id):
    query = f"DELETE FROM resident WHERE id={resident_id}"
    execute_query(conn, query)
    return jsonify({"message": f"Resident {resident_id} deleted successfully"}), 200

# Render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if username == valid_username and password == valid_password:
            # Valid login, redirect to homepage
            return redirect(url_for('homepage'))
        else:
            # Invalid login
            return jsonify({"error": "Invalid username or password"}), 401

    return render_template('login.html')

if __name__ == '__main__':
    app.run()
