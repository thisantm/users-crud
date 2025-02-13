from datetime import datetime
import os
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

app = Flask(__name__)
CORS(app)


def validate_user_data(user_data):
    required_keys = {"username", "roles", "preferences", "active"}
    if not all(key in user_data for key in required_keys):
        return False
    if not isinstance(user_data["roles"], list):
        return False
    if not isinstance(user_data["preferences"], dict):
        return False
    if any(key not in required_keys for key in user_data):
        return False
    return True


@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.json
    if not validate_user_data(user_data):
        return jsonify({"error": "Invalid user data"}), 400
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    user_data["created_ts"] = datetime.now()
    result = collection.insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    return jsonify(user_data), 201


def convert_objectid_to_str(document):
    if isinstance(document, dict):
        return {
            key: (str(value) if isinstance(value, ObjectId) else value)
            for key, value in document.items()
        }
    return document


@app.route("/users", methods=["GET"])
def get_users():
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 10))
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    users = (
        collection.find(
            {},
            {
                "_id": 1,
                "username": 1,
                "roles": 1,
                "preferences": 1,
                "created_ts": 1,
                "active": 1,
            },
        )
        .skip(skip)
        .limit(limit)
    )

    users_list = [convert_objectid_to_str(user) for user in users]

    return jsonify(users_list)


@app.route("/users/<id>", methods=["GET"])
def get_user_by_id(id):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    users = collection.find(
        {"_id": ObjectId(id)},
        {
            "_id": 1,
            "username": 1,
            "roles": 1,
            "preferences": 1,
            "created_ts": 1,
            "active": 1,
        },
    )

    users_list = [convert_objectid_to_str(user) for user in users]

    if users_list == []:
        return ("", 404)

    return jsonify(users_list)


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user_data = request.json
    if not validate_user_data(user_data):
        return jsonify({"error": "Invalid user data"}), 400
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": user_data})
    if result.matched_count == 0:
        return ("", 404)
    user_data["_id"] = id
    return jsonify(user_data)


@app.route("/users/<id>", methods=["DELETE"])
def delete_user_by_id(id):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.delete_one({"_id": ObjectId(id)})

    return ("", 204)
