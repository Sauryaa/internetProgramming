#!/usr/bin/env python3
"""
jokes api routes

@author:
@version: 2025.11
"""

from typing import Literal

from flask import Blueprint, abort, jsonify
from werkzeug import Response
from werkzeug.exceptions import NotFound

from .logic import Joker

main = Blueprint("main", __name__, url_prefix="/api/v1/jokes")


@main.route("/<string:language>/<string:category>/all")
def get_all_jokes_by_language_and_category(language: str, category: str) -> Response:
    """Get all jokes in the specified language/category combination

    :param language: language of the joke
    :param category: category of the joke
    """
    try:
        jokes = Joker.get_jokes(language=language, category=category, number=0)
    except ValueError as error:
        abort(404, description=str(error))
    return jsonify({"jokes": [joke.text for joke in jokes]})


@main.route("/<string:language>/<string:category>/<int:number>")
def get_n_jokes_by_language_and_category(language: str, category: str, number: int):
    """Get multiple jokes

    :param language: language of the jokes
    :param category: category of the jokes
    :param number: number of the jokes to return
    """
    try:
        jokes = Joker.get_jokes(language=language, category=category, number=number)
    except ValueError as error:
        abort(404, description=str(error))
    return jsonify({"jokes": [joke.text for joke in jokes]})


@main.route("/<int:joke_id>")
def get_the_joke(joke_id: int):
    """Get a specific joke by id

    :param joke_id: joke id
    """
    try:
        joke = Joker.get_the_joke(joke_id)
    except ValueError as error:
        abort(404, description=str(error))
    return jsonify(
        {
            "joke": {
                "id": joke_id,
                "language": joke.language,
                "category": joke.category,
                "text": joke.text,
            }
        }
    )


@main.errorhandler(404)
def not_found(error: NotFound) -> tuple[Response, Literal[404]]:
    return jsonify({"error": str(error)}), 404
