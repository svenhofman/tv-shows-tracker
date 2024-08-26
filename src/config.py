import json
import os

CONFIG_FILE = os.path.expanduser("~/.tv-shows-tracker/config.json")

from . import database


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    config_dir = os.path.dirname(CONFIG_FILE)
    # Create config directory if it does not exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def get_db_name():
    config = load_config()
    if "database_name" in config:
        return config["database_name"]
    else:
        while True:
            db_name = input("Enter a MongoDB database name: ")
            if database.is_db_name_unique(db_name):
                break

            print(
                f"The database name '{db_name}' already exists. Please choose another name."
            )

        config["database_name"] = db_name
        save_config(config)
        database.setup_schema()
        print(f"Database name stored in {CONFIG_FILE}")
        return db_name


def get_auth_key():
    config = load_config()

    if "auth_key" in config:
        return config["auth_key"]
    else:
        auth_key = input(
            "Provide a working TMDB authentication key (API key or Access token): "
        )
        config["auth_key"] = auth_key
        save_config(config)
        print(f"Authentication key stored in {CONFIG_FILE}")
        return auth_key
