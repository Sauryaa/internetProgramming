#!/usr/bin/env python3
"""
Geography app initialization

@author: Roman Yasinovskyy
@version: 2025.11
"""

import pathlib

from flask import Flask

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  
    def load_dotenv(*args, **kwargs):  
        return False


def create_app():
    from .routes import main
    from .retrieval import get_data_from_db

    app = Flask(__name__)
    if pathlib.Path(".flaskenv").exists():
        load_dotenv(".flaskenv")
    else:
        load_dotenv("exercises/geo/.flaskenv")
    app.config.from_prefixed_env()
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "geo-secret-key"
    app.config.setdefault("DB_FILE", "world.sqlite3")
    if __name__ == "alex":
        db_dir = "data"
    else:
        db_dir = "exercises/geo/data"
    data_source = pathlib.Path(pathlib.Path(db_dir) / pathlib.Path(app.config["DB_FILE"]))
    if not data_source.exists():
        raise FileNotFoundError("Database not found")
    app.config["DB_FILE"] = data_source
    app.register_blueprint(main)
    with app.app_context():
        app.config["regions"] = [
            row["continental_region"]
            for row in get_data_from_db(
                "select distinct continental_region from country where continental_region is not null order by continental_region;"
            )
            if row["continental_region"]
        ]
        app.config["subregions"] = [
            row["subregion"]
            for row in get_data_from_db(
                "select distinct subregion from country where subregion is not null and subregion!='' order by subregion;"
            )
            if row["subregion"]
        ]
        app.config["countries"] = [
            row["name"]
            for row in get_data_from_db("select name from country order by name;")
            if row["name"]
        ]
    return app
