from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    sex = db.Column(db.String(10))
    year = db.Column(db.String(50))

    castings = db.relationship(
        "CastAssignment",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    crew_positions = db.relationship(
        "CrewAssignment",
        back_populates="student",
        cascade="all, delete-orphan",
    )


class Adult(db.Model):
    __tablename__ = "adults"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    creative_roles = db.relationship(
        "CreativeAssignment",
        back_populates="adult",
        cascade="all, delete-orphan",
    )


class Production(db.Model):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default="Untitled Show", nullable=False)
    subtitle = db.Column(db.String(200))
    cover_image_url = db.Column(db.String(500))
    location = db.Column(db.String(200))
    price = db.Column(db.String(50))
    copyright = db.Column(db.String(200))
    notes = db.Column(db.Text)
    intermission_length = db.Column(db.String(100))
    thanks_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    performance_dates = db.relationship(
        "PerformanceDate",
        order_by="PerformanceDate.position",
        cascade="all, delete-orphan",
    )
    acting_roles = db.relationship(
        "ActingRole",
        order_by="ActingRole.name",
        cascade="all, delete-orphan",
    )
    crew_roles = db.relationship(
        "CrewRole",
        order_by="CrewRole.name",
        cascade="all, delete-orphan",
    )
    creative_roles = db.relationship(
        "CreativeRole",
        order_by="CreativeRole.title",
        cascade="all, delete-orphan",
    )
    songs = db.relationship(
        "Song",
        order_by="Song.act_number, Song.position",
        cascade="all, delete-orphan",
    )


class PerformanceDate(db.Model):
    __tablename__ = "performance_dates"

    id = db.Column(db.Integer, primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    position = db.Column(db.Integer, default=0, nullable=False)


class ActingRole(db.Model):
    __tablename__ = "acting_roles"

    id = db.Column(db.Integer, primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    is_group = db.Column(db.Boolean, default=False, nullable=False)

    cast_assignments = db.relationship(
        "CastAssignment",
        back_populates="role",
        cascade="all, delete-orphan",
    )
    song_performances = db.relationship(
        "SongPerformer",
        back_populates="role",
        cascade="all, delete-orphan",
    )


class CastAssignment(db.Model):
    __tablename__ = "cast_assignments"

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("acting_roles.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    role = db.relationship("ActingRole", back_populates="cast_assignments")
    student = db.relationship("Student", back_populates="castings")


class CrewRole(db.Model):
    __tablename__ = "crew_roles"

    id = db.Column(db.Integer, primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    assignments = db.relationship(
        "CrewAssignment",
        back_populates="role",
        cascade="all, delete-orphan",
    )


class CrewAssignment(db.Model):
    __tablename__ = "crew_assignments"

    id = db.Column(db.Integer, primary_key=True)
    crew_role_id = db.Column(db.Integer, db.ForeignKey("crew_roles.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    role = db.relationship("CrewRole", back_populates="assignments")
    student = db.relationship("Student", back_populates="crew_positions")


class CreativeRole(db.Model):
    __tablename__ = "creative_roles"

    id = db.Column(db.Integer, primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)

    assignments = db.relationship(
        "CreativeAssignment",
        back_populates="role",
        cascade="all, delete-orphan",
    )


class CreativeAssignment(db.Model):
    __tablename__ = "creative_assignments"

    id = db.Column(db.Integer, primary_key=True)
    creative_role_id = db.Column(
        db.Integer, db.ForeignKey("creative_roles.id"), nullable=False
    )
    adult_id = db.Column(db.Integer, db.ForeignKey("adults.id"), nullable=False)

    role = db.relationship("CreativeRole", back_populates="assignments")
    adult = db.relationship("Adult", back_populates="creative_roles")


class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    act_number = db.Column(db.Integer, default=1, nullable=False)
    position = db.Column(db.Integer, default=0, nullable=False)
    notes = db.Column(db.String(200))

    performers = db.relationship(
        "SongPerformer",
        back_populates="song",
        cascade="all, delete-orphan",
    )


class SongPerformer(db.Model):
    __tablename__ = "song_performers"

    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey("songs.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("acting_roles.id"), nullable=False)

    song = db.relationship("Song", back_populates="performers")
    role = db.relationship("ActingRole", back_populates="song_performances")
