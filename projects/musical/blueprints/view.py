from collections import defaultdict

from flask import Blueprint, redirect, render_template, url_for

from ..models import ActingRole, CreativeRole, CrewRole, Song
from ..services import get_active_production

view_bp = Blueprint("view", __name__, template_folder="../templates")


@view_bp.context_processor
def inject_active():
    return {"active_production": get_active_production()}


@view_bp.route("/")
def landing():
    return redirect(url_for("view.program"))


@view_bp.route("/program")
def program():
    production = get_active_production()
    cast_roles = (
        ActingRole.query.filter_by(production_id=production.id)
        .order_by(ActingRole.is_group.asc(), ActingRole.name)
        .all()
    )
    crew_roles = (
        CrewRole.query.filter_by(production_id=production.id)
        .order_by(CrewRole.name)
        .all()
    )
    creative_roles = (
        CreativeRole.query.filter_by(production_id=production.id)
        .order_by(CreativeRole.title)
        .all()
    )
    songs = (
        Song.query.filter_by(production_id=production.id)
        .order_by(Song.act_number, Song.position, Song.title)
        .all()
    )

    songs_by_act = defaultdict(list)
    for song in songs:
        songs_by_act[song.act_number].append(song)

    acts = sorted(songs_by_act.items(), key=lambda pair: pair[0])

    return render_template(
        "view/program.html",
        production=production,
        cast_roles=cast_roles,
        crew_roles=crew_roles,
        creative_roles=creative_roles,
        acts=acts,
    )
