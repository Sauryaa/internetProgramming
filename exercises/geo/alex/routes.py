#!/usr/bin/env python3
"""
Geography app routes

@author:
@version: 2025.11
"""

from __future__ import annotations

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

from .retrieval import get_data_from_db

main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
def world() -> str:
    """Display default page"""
    query = """
        select
            c.name,
            c.official_name,
            c.continental_region,
            c.subregion,
            c.area,
            c.population_2023,
            c.government_system,
            ci.name as capital_name
        from country as c
        left join city as ci on c.capital = ci.id
        order by c.name;
    """
    records = [dict(row) for row in get_data_from_db(query)]
    heading = f"{len(records)} countries and territories of the world"
    return render_template(
        "world.jinja",
        countries=records,
        heading=heading,
        message=None,
        country_options=current_app.config["countries"],
    )


@main.get("/region", defaults={"name": None})
@main.get("/region/<string:name>")
def region(name: str | None) -> str | Response:
    """Display region information"""
    selected_region = name or request.args.get("name")
    options = current_app.config["regions"]
    if not selected_region:
        return render_template(
            "region.jinja",
            countries=[],
            heading=None,
            message="Choose a continental region to see the list of countries.",
            country_options=current_app.config["countries"],
            region_options=options,
            selected_region=None,
        )
    query = """
        select
            c.name,
            c.official_name,
            c.continental_region,
            c.subregion,
            c.area,
            c.population_2023,
            c.government_system,
            ci.name as capital_name
        from country as c
        left join city as ci on c.capital = ci.id
        where c.continental_region=?
        order by c.name;
    """
    records = [dict(row) for row in get_data_from_db(query, (selected_region,))]
    if not records:
        abort(404, description=f"Region '{selected_region}' was not found.")
    heading = f"{len(records)} countries and territories of {selected_region}"
    return render_template(
        "region.jinja",
        countries=records,
        heading=heading,
        message=None,
        country_options=current_app.config["countries"],
        region_options=options,
        selected_region=selected_region,
    )


@main.get("/subregion", defaults={"name": None})
@main.get("/subregion/<string:name>")
def subregion(name: str | None) -> str | Response:
    """Display subregion information"""
    selected_subregion = name or request.args.get("name")
    options = current_app.config["subregions"]
    if not selected_subregion:
        return render_template(
            "subregion.jinja",
            countries=[],
            heading=None,
            message="Choose a subregion to see the list of its countries.",
            country_options=current_app.config["countries"],
            subregion_options=options,
            selected_subregion=None,
        )
    query = """
        select
            c.name,
            c.official_name,
            c.continental_region,
            c.subregion,
            c.area,
            c.population_2023,
            c.government_system,
            ci.name as capital_name
        from country as c
        left join city as ci on c.capital = ci.id
        where c.subregion=?
        order by c.name;
    """
    records = [dict(row) for row in get_data_from_db(query, (selected_subregion,))]
    if not records:
        abort(404, description=f"Subregion '{selected_subregion}' was not found.")
    heading = f"{len(records)} countries and territories of {selected_subregion}"
    return render_template(
        "subregion.jinja",
        countries=records,
        heading=heading,
        message=None,
        country_options=current_app.config["countries"],
        subregion_options=options,
        selected_subregion=selected_subregion,
    )


@main.get("/country", defaults={"name": None})
@main.get("/country/<string:name>")
def country(name: str | None) -> str | Response:
    """Display country information"""
    selected_country = name or request.args.get("name")
    options = current_app.config["countries"]
    if not selected_country:
        return render_template(
            "country.jinja",
            cities=None,
            heading=None,
            country_options=options,
            selected_country=None,
            capital_id=None,
            country_info=None,
        )
    country_query = "select * from country where name=?;"
    country_data = get_data_from_db(country_query, (selected_country,))
    if not country_data:
        abort(404, description=f"Country '{selected_country}' was not found.")
    country_info = dict(country_data[0])
    city_query = "select * from city where country_code=? order by name;"
    cities = [dict(row) for row in get_data_from_db(city_query, (country_info["code3"],))]
    heading = f"{len(cities)} cities of {country_info['name']}"
    return render_template(
        "country.jinja",
        cities=cities,
        heading=heading,
        country_options=options,
        selected_country=selected_country,
        capital_id=country_info.get("capital"),
        country_info=country_info,
    )


@main.errorhandler(404)
def not_found(err):
    description = getattr(err, "description", "Requested resource was not found.")
    flash(description, "warning")
    path = request.path
    if path.startswith("/region"):
        return (
            render_template(
                "region.jinja",
                countries=[],
                heading=None,
                message=description,
                country_options=current_app.config["countries"],
                region_options=current_app.config["regions"],
                selected_region=None,
            ),
            404,
        )
    elif path.startswith("/subregion"):
        return (
            render_template(
                "subregion.jinja",
                countries=[],
                heading=None,
                message=description,
                country_options=current_app.config["countries"],
                subregion_options=current_app.config["subregions"],
                selected_subregion=None,
            ),
            404,
        )
    elif path.startswith("/country"):
        return (
            render_template(
                "country.jinja",
                cities=[],
                heading=None,
                country_options=current_app.config["countries"],
                selected_country=None,
                capital_id=None,
                country_info=None,
                message=description,
            ),
            404,
        )
    else:
        return (
            render_template(
                "world.jinja",
                countries=[],
                heading=None,
                message=description,
                country_options=current_app.config["countries"],
            ),
            404,
        )
