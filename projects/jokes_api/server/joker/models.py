#!/usr/bin/env python3
"""
jokes api models

@author:
@version: 2025.11
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Joke:
    """
    Represent a single joke returned by pyjokes.

    :param language: Language code (e.g. en, cs)
    :param category: Joke category (neutral|chuck)
    :param text: The actual joke text
    """

    language: str
    category: str
    text: str
