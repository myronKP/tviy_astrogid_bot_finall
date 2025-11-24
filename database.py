from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Optional

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, mapped_column, sessionmaker, Mapped

DATABASE_URL = "sqlite:///tviyastrogid.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    zodiac_sign: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    cards: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    last_gift: Mapped[Optional[str]] = mapped_column(String(32))
    invited_by: Mapped[Optional[int]] = mapped_column(Integer)


Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_or_create_user(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if user is None:
        user = User(id=user_id, cards=50)
        session.add(user)
        session.flush()
    return user
