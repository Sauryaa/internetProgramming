from pathlib import Path

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from ..models import (
    ActingRole,
    Adult,
    CastAssignment,
    CreativeRole,
    CrewRole,
    PerformanceDate,
    Song,
    Student,
    db,
)
from ..services import (
    DEFAULT_CAST_PATH,
    assign_adults_to_role,
    assign_performers_to_song,
    assign_students_to_crew,
    assign_students_to_role,
    delete_creative_role,
    delete_crew_role,
    delete_role,
    delete_song,
    get_active_production,
    import_students_from_csv,
    reset_performance_dates,
)

edit_bp = Blueprint("edit", __name__, template_folder="../templates")


@edit_bp.context_processor
def inject_defaults():
    return {"active_production": get_active_production()}


@edit_bp.route("/")
def dashboard():
    production = get_active_production()
    student_count = Student.query.count()
    cast_roles = (
        db.session.query(ActingRole)
        .filter_by(production_id=production.id)
        .order_by(ActingRole.name)
        .all()
    )
    crew_roles = (
        db.session.query(CrewRole)
        .filter_by(production_id=production.id)
        .order_by(CrewRole.name)
        .all()
    )
    creative_roles = (
        db.session.query(CreativeRole)
        .filter_by(production_id=production.id)
        .order_by(CreativeRole.title)
        .all()
    )
    songs = (
        db.session.query(Song)
        .filter_by(production_id=production.id)
        .order_by(Song.act_number, Song.position)
        .all()
    )
    return render_template(
        "edit/dashboard.html",
        production=production,
        student_count=student_count,
        cast_roles=cast_roles,
        crew_roles=crew_roles,
        creative_roles=creative_roles,
        songs=songs,
        roster_path=Path(DEFAULT_CAST_PATH).name,
    )


@edit_bp.route("/import", methods=["POST"])
def import_students():
    created = import_students_from_csv(DEFAULT_CAST_PATH)
    if created:
        flash(f"Imported {created} students from roster.", "success")
    else:
        flash("No new students were imported (roster may already be loaded).", "info")
    return redirect(url_for("edit.dashboard"))


@edit_bp.route("/general", methods=["GET", "POST"])
def general():
    production = get_active_production()
    if request.method == "POST":
        production.title = request.form.get("title", production.title).strip() or "Untitled Show"
        production.subtitle = request.form.get("subtitle", "").strip() or None
        production.cover_image_url = request.form.get("cover_image_url", "").strip() or None
        production.location = request.form.get("location", "").strip() or None
        production.price = request.form.get("price", "").strip() or None
        production.copyright = request.form.get("copyright", "").strip() or None
        production.notes = request.form.get("notes", "").strip() or None
        production.intermission_length = request.form.get("intermission_length", "").strip() or None
        production.thanks_text = request.form.get("thanks_text", "").strip() or None

        date_lines = request.form.get("dates", "").splitlines()
        date_labels = [line.strip() for line in date_lines if line.strip()]
        reset_performance_dates(production, date_labels)

        db.session.commit()
        flash("Production details updated.", "success")
        return redirect(url_for("edit.general"))

    dates_text = "\n".join([d.label for d in production.performance_dates])
    return render_template(
        "edit/general.html",
        production=production,
        dates_text=dates_text,
        roster_path=Path(DEFAULT_CAST_PATH).name,
    )


@edit_bp.route("/cast", methods=["GET", "POST"])
def cast():
    production = get_active_production()

    if request.method == "POST":
        actions = request.form.getlist("action")
        action = actions[-1] if actions else None
        if action == "add":
            name = request.form.get("name", "").strip()
            if name:
                role = ActingRole(
                    name=name,
                    is_group=bool(request.form.get("is_group")),
                    production_id=production.id,
                )
                db.session.add(role)
                db.session.commit()
                flash("Acting role added.", "success")
        elif action == "update":
            role_id = int(request.form.get("role_id"))
            role = ActingRole.query.get_or_404(role_id)
            role.name = request.form.get("name", role.name).strip() or role.name
            role.is_group = bool(request.form.get("is_group"))
            selected_ids = [int(s) for s in request.form.getlist("students")]
            assign_students_to_role(role, selected_ids)
            flash("Role updated.", "success")
        elif action == "delete":
            role_id = int(request.form.get("role_id"))
            role = ActingRole.query.get_or_404(role_id)
            delete_role(role)
            flash("Role removed.", "info")
        return redirect(url_for("edit.cast"))

    roles = (
        ActingRole.query.filter_by(production_id=production.id)
        .order_by(ActingRole.is_group.asc(), ActingRole.name)
        .all()
    )
    students = Student.query.order_by(Student.name).all()
    return render_template("edit/cast.html", roles=roles, students=students)


@edit_bp.route("/crew", methods=["GET", "POST"])
def crew():
    production = get_active_production()

    if request.method == "POST":
        actions = request.form.getlist("action")
        action = actions[-1] if actions else None
        if action == "add":
            name = request.form.get("name", "").strip()
            if name:
                role = CrewRole(name=name, production_id=production.id)
                db.session.add(role)
                db.session.commit()
                flash("Crew responsibility added.", "success")
        elif action == "update":
            role_id = int(request.form.get("role_id"))
            role = CrewRole.query.get_or_404(role_id)
            role.name = request.form.get("name", role.name).strip() or role.name
            selected_ids = [int(s) for s in request.form.getlist("students")]
            assign_students_to_crew(role, selected_ids)
            flash("Crew assignment updated.", "success")
        elif action == "delete":
            role_id = int(request.form.get("role_id"))
            role = CrewRole.query.get_or_404(role_id)
            delete_crew_role(role)
            flash("Crew responsibility removed.", "info")
        return redirect(url_for("edit.crew"))

    roles = CrewRole.query.filter_by(production_id=production.id).order_by(CrewRole.name).all()
    students = Student.query.order_by(Student.name).all()
    return render_template("edit/crew.html", roles=roles, students=students)


@edit_bp.route("/creative", methods=["GET", "POST"])
def creative():
    production = get_active_production()

    if request.method == "POST":
        actions = request.form.getlist("action")
        action = actions[-1] if actions else None
        if action == "add_role":
            title = request.form.get("title", "").strip()
            if title:
                role = CreativeRole(title=title, production_id=production.id)
                db.session.add(role)
                db.session.commit()
                flash("Creative role added.", "success")
        elif action == "add_adult":
            name = request.form.get("name", "").strip()
            if name:
                existing = Adult.query.filter_by(name=name).first()
                if not existing:
                    db.session.add(Adult(name=name))
                    db.session.commit()
                    flash("Adult added to roster.", "success")
        elif action == "update":
            role_id = int(request.form.get("role_id"))
            role = CreativeRole.query.get_or_404(role_id)
            role.title = request.form.get("title", role.title).strip() or role.title
            adult_ids = [int(a) for a in request.form.getlist("adults")]
            assign_adults_to_role(role, adult_ids)
            flash("Creative team updated.", "success")
        elif action == "delete":
            role_id = int(request.form.get("role_id"))
            role = CreativeRole.query.get_or_404(role_id)
            delete_creative_role(role)
            flash("Creative role removed.", "info")
        return redirect(url_for("edit.creative"))

    roles = CreativeRole.query.filter_by(production_id=production.id).order_by(CreativeRole.title).all()
    adults = Adult.query.order_by(Adult.name).all()
    return render_template("edit/creative.html", roles=roles, adults=adults)


@edit_bp.route("/songs", methods=["GET", "POST"])
def songs():
    production = get_active_production()

    if request.method == "POST":
        actions = request.form.getlist("action")
        action = actions[-1] if actions else None
        if action == "add":
            title = request.form.get("title", "").strip()
            if title:
                act = int(request.form.get("act_number") or 1)
                position = int(request.form.get("position") or 0)
                song = Song(
                    title=title,
                    act_number=act,
                    position=position,
                    production_id=production.id,
                    notes=request.form.get("notes", "").strip() or None,
                )
                db.session.add(song)
                db.session.commit()
                flash("Song added.", "success")
        elif action == "update":
            song_id = int(request.form.get("song_id"))
            song = Song.query.get_or_404(song_id)
            song.title = request.form.get("title", song.title).strip() or song.title
            song.act_number = int(request.form.get("act_number") or song.act_number)
            song.position = int(request.form.get("position") or song.position)
            song.notes = request.form.get("notes", "").strip() or None
            performer_ids = [int(rid) for rid in request.form.getlist("performers")]
            assign_performers_to_song(song, performer_ids)
            flash("Song updated.", "success")
        elif action == "delete":
            song_id = int(request.form.get("song_id"))
            song = Song.query.get_or_404(song_id)
            delete_song(song)
            flash("Song removed.", "info")
        return redirect(url_for("edit.songs"))

    songs = (
        Song.query.filter_by(production_id=production.id)
        .order_by(Song.act_number, Song.position)
        .all()
    )
    roles = (
        ActingRole.query.filter_by(production_id=production.id)
        .order_by(ActingRole.is_group.asc(), ActingRole.name)
        .all()
    )
    return render_template("edit/songs.html", songs=songs, roles=roles)
