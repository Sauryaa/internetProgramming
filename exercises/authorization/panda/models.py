#!/usr/bin/env python3
"""
PandAuth models

@author:
@version: 2025.12
"""

import datetime

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column

from . import db, mm


# SQLAlchemy model
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(db.String(256), primary_key=True)
    email: Mapped[str] = mapped_column(db.String(256), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(256), nullable=False)
    picture: Mapped[str] = mapped_column(db.String(512), nullable=True)
    registered: Mapped[datetime.datetime] = mapped_column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover - convenience for debugging
        return f"<User {self.email}>"


# Marshmallow schema
class UserSchema(mm.SQLAlchemyAutoSchema):
    """User schema"""

    class Meta:
        """Metadata"""

        model = User
        load_instance = True
        include_relationships = True
