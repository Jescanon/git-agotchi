from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, CheckConstraint, Integer

from datetime import datetime


from app.core.database import Base

class User(Base):
    __tablename__ = "user"

    telegram_id: Mapped[int] = mapped_column(primary_key=True)

    github_name: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    github_token: Mapped[str] = mapped_column(unique=True, nullable=True)

    agotchi: Mapped["Agotchi"] = relationship("Agotchi", uselist=False, back_populates="users")

class Agotchi(Base):
    __tablename__ = "agotchi"

    user_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'), unique=True, primary_key=True)
    avatar_url: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hp: Mapped[int] = mapped_column(Integer)
    mood: Mapped[str] = mapped_column(String)
    last_commit_check: Mapped[datetime]

    users: Mapped["User"] = relationship("User", back_populates="agotchi")

    __table_args__ = (
        CheckConstraint("hp <= 100", name="agotchi_hp_max"),
        CheckConstraint("hp >= 0", name="agotchi_hp_mix"),
        CheckConstraint("mood IN ('Happy', 'Angry', 'Dead')", name="agotchi_mood"),
    )

