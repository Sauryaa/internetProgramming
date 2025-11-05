#!/usr/bin/env python3

import random
import pyjokes
from flask import Flask, abort, render_template, request
from pyjokes.exc import PyjokesError

LANGUAGES = {
    "cs": "CZECH",
    "de": "GERMAN",
    "en": "ENGLISH",
    "es": "SPANISH",
    "eu": "BASQUE",
    "fr": "FRENCH",
    "gl": "GALICIAN",
    "hu": "HUNGARIAN",
    "it": "ITALIAN",
    "lt": "LITHUANIAN",
    "pl": "POLISH",
    "sv": "SWEDISH",
}

app = Flask(__name__)

@app.get("/")
def index():
    return render_template(
        "jokes.jinja",
        languages=LANGUAGES,
        categories=["all", "neutral", "chuck"],
        numbers=list(range(1, 10)),
        selected_language="en",
        selected_category="all",
        selected_number=1,
        jokes=[],
    )


@app.post("/")
def index_jokes():
    if not request.form:
        abort(418)

    language = request.form.get("language", "en")
    category = request.form.get("category", "all")
    try:
        number = int(request.form.get("number", 1))
    except (TypeError, ValueError):
        number = 1

    jokes = get_jokes(language, category, number)

    return render_template(
        "jokes.jinja",
        languages=LANGUAGES,
        categories=["all", "neutral", "chuck"],
        numbers=list(range(1, 10)),
        selected_language=language,
        selected_category=category,
        selected_number=number,
        jokes=jokes,
    )


def get_jokes(language="en", category="all", number=1) -> list[str]:
    try:
        all_jokes = pyjokes.get_jokes(language=language, category=category)
    except PyjokesError:
        return ["No kidding!"]

    if isinstance(all_jokes, str):
        all_jokes = [all_jokes]
    else:
        try:
            all_jokes = list(all_jokes)
        except Exception:
            all_jokes = [str(all_jokes)]

    if number <= 1:
        return [random.choice(all_jokes)] if all_jokes else []

    if number >= len(all_jokes):
        return all_jokes

    try:
        return random.sample(all_jokes, number)
    except ValueError:
        return all_jokes


if __name__ == "__main__":
    app.run(debug=True)