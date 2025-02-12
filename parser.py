from dataclasses import dataclass
from datetime import datetime
import json
import os
from typing import List
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGODB_URI")


@dataclass
class UserPreferences:
    timezone: str


@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    created_ts: float
    active: bool = True


def parse_roles(data: dict) -> List[str]:
    roles = []
    for key, value in data.items():
        if key.startswith("is_user_") and key != "is_user_active" and value:
            role = key.replace("is_user_", "")
            roles.append(role)
    return roles


def parse_user(data: dict) -> dict:
    user = User(
        username=data["user"],
        password=data["password"],
        roles=parse_roles(data),
        preferences=UserPreferences(timezone=data["user_timezone"]),
        active=data.get("is_user_active", False),
        created_ts=datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
    )

    user_dict = user.__dict__
    user_dict["preferences"] = user.preferences.__dict__
    return user_dict


def import_users(json_file: str, mongo_uri: str, db_name: str, collection_name: str):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    with open(json_file, "r") as file:
        data = json.load(file)

    users_data = data["users"]
    users = [parse_user(user) for user in users_data]
    collection.delete_many({})
    collection.insert_many(users)
    print(f"Imported {len(users)} users into {collection_name} collection.")


if __name__ == "__main__":
    import_users("udata.json", uri, "testDB", "users")
