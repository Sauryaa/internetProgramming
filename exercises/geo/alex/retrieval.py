#!/usr/bin/env python3
"""
Geography query data retrieval

@author:
@version: 2025.11
"""

from __future__ import annotations

from functools import cache
import sqlite3

from flask import current_app


@cache
def get_data_from_db(query: str, params: tuple | None = None) -> list:
    """Retrieve data from the database

    :param query: parametrized query to execute
    :param params: query parameters
    """
    params = params or tuple()
    connection = sqlite3.connect(current_app.config["DB_FILE"])
    connection.row_factory = sqlite3.Row
    try:
        cursor = connection.execute(query, params)
        return cursor.fetchall()
    finally:
        connection.close()
