#!/usr/bin/env python3
"""
jokes api logic

@author:
@version: 2025.11
"""

import pathlib
import random
from functools import cache
from typing import Optional

import pyjokes
from pyjokes.exc import CategoryNotFoundError, LanguageNotFoundError

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - fallback for Python <3.11
    import tomli as tomllib

from .models import Joke


class Joker:
    """
    A layer to retrieve jokes from the pyjokes package

    :raises ValueError: the dataset has not been initialized
    :raises ValueError: the language is invalid
    :raises ValueError: the category is invalid
    :raises ValueError: the joke id is invalid
    :raises ValueError: requested number of jokes is below 0
    """

    _dataset: Optional[list[Joke]] = None
    _languages: Optional[dict[str, str]] = None
    _config_path = pathlib.Path(__file__).resolve().parents[1] / "config.toml"

    @classmethod
    def init_dataset(cls):
        """
        Initialize the dataset

        Load jokes from the `pyjokes` package into a list of jokes
        """
        if cls._dataset is not None:
            return

        languages = cls._load_languages()
        dataset: list[Joke] = []
        for language in sorted(languages.keys()):
            for category in ("neutral", "chuck"):
                try:
                    jokes = pyjokes.get_jokes(language=language, category=category)
                except (LanguageNotFoundError, CategoryNotFoundError):
                    jokes = []
                dataset.extend(Joke(language, category, text) for text in jokes)

        cls._dataset = dataset

    @classmethod
    def get_jokes(cls, language: str = "any", category: str = "any", number: int = 0) -> list[Joke]:
        """Get all jokes in the specified language/category combination

        :param language: language of the joke
        :param category: category of the joke
        :param number: number of jokes to return, 0 to return all
        """
        cls._ensure_dataset()
        cls._validate_language(language)
        cls._validate_category(category)
        if number < 0:
            raise ValueError("Number of jokes must be a non-negative integer")

        jokes = [cls._dataset[idx] for idx in cls._filter_indices(language, category)]

        if number == 0 or number >= len(jokes):
            return jokes

        return random.sample(jokes, k=number)

    @classmethod
    def get_the_joke(cls, joke_id: int) -> Joke:
        """Get a specific joke by id

        :param joke_id: joke id
        """
        cls._ensure_dataset()
        if joke_id < 0 or joke_id >= len(cls._dataset):
            raise ValueError(f"Joke {joke_id} not found, try an id between 0 and {len(cls._dataset) - 1}")
        return cls._dataset[joke_id]

    @classmethod
    def _load_languages(cls) -> dict[str, str]:
        if cls._languages is None:
            with cls._config_path.open("rb") as config_file:
                config = tomllib.load(config_file)
            cls._languages = config.get("LANGUAGES", {})
        return cls._languages

    @classmethod
    def _ensure_dataset(cls) -> None:
        if cls._dataset is None:
            raise ValueError("Dataset has not been initialized")

    @classmethod
    def _validate_language(cls, language: str) -> None:
        if language != "any" and language not in cls._load_languages():
            raise ValueError(f"Language {language} does not exist")

    @staticmethod
    def _validate_category(category: str) -> None:
        if category not in {"any", "neutral", "chuck"}:
            raise ValueError(f"Category {category} does not exist")

    @staticmethod
    @cache
    def _filter_indices(language: str, category: str) -> tuple[int, ...]:
        dataset = Joker._dataset
        if dataset is None:
            raise ValueError("Dataset has not been initialized")
        return tuple(
            idx
            for idx, joke in enumerate(dataset)
            if (language == "any" or joke.language == language)
            and (category == "any" or joke.category == category)
        )
