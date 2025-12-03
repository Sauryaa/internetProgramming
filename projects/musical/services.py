import csv
from pathlib import Path
from typing import Iterable

from .models import (
    ActingRole,
    Adult,
    CastAssignment,
    CreativeAssignment,
    CreativeRole,
    CrewAssignment,
    CrewRole,
    PerformanceDate,
    Production,
    Song,
    SongPerformer,
    Student,
    db,
)

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CAST_PATH = BASE_DIR / "cast.csv"


def get_active_production() -> Production:
    """Return the most recently created production (create one if missing)."""
    production = Production.query.order_by(Production.created_at.desc()).first()
    if not production:
        production = Production(title="High School Musical", subtitle="Main Stage")
        db.session.add(production)
        db.session.commit()
    return production


def reset_performance_dates(production: Production, labels: Iterable[str]) -> None:
    production.performance_dates.clear()
    for idx, label in enumerate(labels):
        production.performance_dates.append(
            PerformanceDate(label=label.strip(), position=idx)
        )


def import_students_from_csv(csv_path: Path = DEFAULT_CAST_PATH) -> int:
    """Import roster from CSV; returns number of new records created."""
    created = 0
    if not csv_path.exists():
        return created

    with csv_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            name = (row.get("name") or "").strip()
            if not name:
                continue
            student = Student.query.filter_by(name=name).first()
            if student:
                continue
            student = Student(
                name=name,
                sex=(row.get("sex") or "").strip(),
                year=(row.get("year") or "").strip(),
            )
            db.session.add(student)
            created += 1
    if created:
        db.session.commit()
    return created


def delete_role(role: ActingRole) -> None:
    db.session.delete(role)
    db.session.commit()


def delete_crew_role(role: CrewRole) -> None:
    db.session.delete(role)
    db.session.commit()


def delete_creative_role(role: CreativeRole) -> None:
    db.session.delete(role)
    db.session.commit()


def delete_song(song: Song) -> None:
    db.session.delete(song)
    db.session.commit()


def assign_students_to_role(role: ActingRole, student_ids: Iterable[int]) -> None:
    role.cast_assignments.clear()
    for student_id in student_ids:
        student = Student.query.get(student_id)
        if student:
            role.cast_assignments.append(CastAssignment(student=student))
    db.session.commit()


def assign_students_to_crew(role: CrewRole, student_ids: Iterable[int]) -> None:
    role.assignments.clear()
    for student_id in student_ids:
        student = Student.query.get(student_id)
        if student:
            role.assignments.append(CrewAssignment(student=student))
    db.session.commit()


def assign_adults_to_role(role: CreativeRole, adult_ids: Iterable[int]) -> None:
    role.assignments.clear()
    for adult_id in adult_ids:
        adult = Adult.query.get(adult_id)
        if adult:
            role.assignments.append(CreativeAssignment(adult=adult))
    db.session.commit()


def assign_performers_to_song(song: Song, role_ids: Iterable[int]) -> None:
    song.performers.clear()
    for role_id in role_ids:
        role = ActingRole.query.get(role_id)
        if role:
            song.performers.append(SongPerformer(role=role))
    db.session.commit()
