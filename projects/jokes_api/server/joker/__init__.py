#!/usr/bin/env python3
"""
jokes api

@author:
@version: 2025.11
"""

import pathlib

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - fallback for Python <3.11
    import tomli as tomllib

from flask import Flask

try:
    from flask_cors import CORS
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    def CORS(app, *_, **__):
        return app

from .logic import Joker


def create_app() -> Flask:
    this_app = Flask(__name__)

    CORS(this_app)

    config_path = pathlib.Path(__file__).resolve().parents[1] / "config.toml"
    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file)
    this_app.config.update(config)

    Joker.init_dataset()

    from .routes import main

    this_app.register_blueprint(main)

    return this_app
