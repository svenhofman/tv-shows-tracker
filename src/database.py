import sys
from pymongo import MongoClient, errors
from . import config

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017

def is_db_name_unique(db_name):
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    return not (db_name in client.list_database_names())

def get_db():
    try:
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[config.get_db_name()]
        return db
    except errors.PyMongoError as err:
        print(f"Connection Error: {err}")
        sys.exit("Exiting due to connection error.")

def connect():
    db = get_db()
    return db["shows"]


def setup_schema():
    # Define the schema
    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["id", "name", "last_watched", "has_ended"],
            "properties": {
                "id": {
                    "bsonType": "int",
                    "description": "id of show",
                },
                "name": {
                    "bsonType": "string",
                    "minimum": 0,
                    "description": "name of show",
                },
                "last_watched": {
                    "bsonType": "date",
                    "description": "last date it was watched",
                },
                "has_ended": {
                    "bsonType": "bool",
                    "description": "show has ended or not",
                },
            },
        }
    }

    # Get database with given name, it might already exist
    db = get_db()

    # Create the collection
    print("Creating database with collection named 'shows'.")
    db.create_collection("shows")
    print(f"Collection 'shows' created successfully.")

    # Overwrite the collection schema and create unique index on 'id' field
    try:
        db.command({"collMod": "shows", "validator": schema})
        db["shows"].create_index("id", unique=True)
    except Exception as err:
        print(f"Error creating schema: {err}")
        sys.exit("Exiting due to database error.")

def get_all_shows():
    collection = connect()
    shows_iterable = collection.find()
    return [show for show in shows_iterable]

def get_running_shows():
    collection = connect()
    shows_iterable = collection.find({"has_ended": False})
    return [show for show in shows_iterable]


def add_shows(new_shows):
    collection = connect()

    # Show does not get added if it already exists
    try:
        result =  collection.insert_many(new_shows, ordered=False)
        if result.inserted_ids:
            return f"Show{"s" if len(new_shows)>1 else ""} added to watchlist successfully."
    except errors.BulkWriteError as e:
        # Ignore duplication errors
        filtered_errors = [
            error for error in e.details["writeErrors"] if error["code"] != 11000
        ]
        if filtered_errors:
            # Return a message with the filtered errors
            return f"Errors occurred during insertion: {filtered_errors}"
        else:
            return f"Show{"s" if len(new_shows)>1 else ""} already exist{"s" if len(new_shows) == 1 else ""} on watchlist."


def delete_show(show_id):
    collection = connect()

    try:
        result = collection.delete_one({"id": show_id})

        if result.deleted_count > 0:
            return "Show deleted successfully."
        else:
            return "Show does not exist in database."

    except errors.PyMongoError as err:
        print(f"An error occurred during deletion: {err}")
        sys.exit("Exiting due to error during deletion.")


def update_last_watched(show_id, new_date):
    collection = connect()

    try:
        result = collection.find_one_and_update(
            {"id": show_id}, {"$set": {"last_watched": new_date}}, return_document=True
        )

        if result:
            return "Watch date updated successfully."
        else:
            return "Show does not exist in database."

    except errors.PyMongoError as e:
        return f"An error occurred during the update: {e}"


def update_ended_shows(show_ids):
    collection = connect()
    
    try:
        collection.update_many({"id": {"$in": show_ids}}, {"$set": {"has_ended": True}})
    except errors.PyMongoError as e:
        print(f"An error occurred during the update: {e}")
