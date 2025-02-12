import os
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient

load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

app = Flask(__name__)


def convert_objectid_to_str(document):
    if isinstance(document, dict):
        return {
            key: (str(value) if isinstance(value, ObjectId) else value)
            for key, value in document.items()
        }
    return document


@app.route("/users", methods=["GET"])
def get_users():
    skip = request.args.get("skip", 0)
    limit = request.args.get("limit", 10)
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
    skip = request.args.get("skip", 0)
    limit = request.args.get("limit", 10)
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

    return jsonify(users_list)
