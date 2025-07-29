from flask import Flask, jsonify, request
import json
import os
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="admin",  # empty if you didn’t set one in XAMPP
        database="pet_api",
        port=3307
    )

def save_to_mysql(name, animal):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO pets (name, animal) VALUES (%s, %s)"
    values = (name, animal)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()


app = Flask(__name__)
DATA_FILE = 'pets.json'

# Load pets from JSON file
def load_pets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Save pets to JSON file
def save_pets(pets):
    with open(DATA_FILE, 'w') as file:
        json.dump(pets, file, indent=4)

# A list of pets (our fake database)

# pets = [
#     {"id": 1, "name": "Snowy", "animal": "Dog"},
#     {"id": 2, "name": "Mimi", "animal": "Cat"}
# ]

# Route: GET /pets
@app.route("/pets", methods=["GET"])
def get_pets():
    pets=load_pets()
    return jsonify(pets)

# Route: GET /pets/<id>
@app.route("/pets/<int:pet_id>", methods=["GET"])
def get_pet(pet_id):
    pets=load_pets()
    for pet in pets:
        if pet["id"] == pet_id:
            return jsonify(pet)
    return jsonify({"error": "Pet not found"}), 404

#comment : pets store in mysql
@app.route("/pets", methods=["POST"])
def add_pet():
    data = request.get_json()
    save_to_mysql(data["name"], data["animal"])
    return jsonify({"message": "Pet saved to MySQL"}), 201


# Route: POST /pets (comment : pets store in json file)
# @app.route("/pets", methods=["POST"])
# def add_pet():
#     pets=load_pets()
#     data = request.get_json()
#     print("my test",data)
#     new_pet = {
#         "id": len(pets) + 1,
#         "name": data["name"],
#         "animal": data["animal"]
#     }
#     pets.append(new_pet)
#     save_pets(pets)
#     return jsonify(new_pet), 201

# Route: DELETE /pets/<int:pet_id>
@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def delete_pet(pet_id):
    pets=load_pets()
    for pet in pets:
        if pet["id"] == pet_id:
            pets.remove(pet)
            save_pets(pets)
            return jsonify({"message": "Pet deleted"})
    return jsonify({"error": "Pet not found"}), 404

# Route: PUT /pets/<int:pet_id>
@app.route("/pets/<int:pet_id>", methods=["PUT"])
def update_pet(pet_id):
    pets=load_pets()
    data = request.get_json()
    for pet in pets:
        if pet["id"] == pet_id:
            # pet["name"] = data.get("name", pet["name"])
            # pet["animal"] = data.get("animal", pet["animal"])
            pet["name"] = data["name"]
            pet["animal"] = data["animal"]
            save_pets(pets)
            return jsonify(pet)
    return jsonify({"error": "Pet not found"}), 404


# Start the app
if __name__ == "__main__":
    app.run(debug=True)
