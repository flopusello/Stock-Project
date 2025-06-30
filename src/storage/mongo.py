from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

local_client = MongoClient("localhost", 27017)


def db_connect(db_name: str):
    try:
        local_client.db_name
        print(f"Connected to database: {db_name}")
        return True
    except ConnectionFailure as e:
        print(f"Connection failed: {e}")
        return False


def insert_many(db_name: str, collection_name: str, data):
    try:
        db = local_client[db_name]
        collection = db[collection_name]
        result = collection.insert_many(data, ordered=False)
        print(
            f"Inserted {len(result.inserted_ids)} documents into {collection_name} collection."
        )
    except OperationFailure as e:
        print(f"Error inserting data: {e}")


def clean_collection(db_name: str, collection_name: str):
    try:
        db = local_client[db_name]
        collection = db[collection_name]
        result = collection.delete_many({})
        print(
            f"Deleted {result.deleted_count} documents from {collection_name} collection."
        )
    except OperationFailure as e:
        print(f"Error cleaning collection: {e}")
