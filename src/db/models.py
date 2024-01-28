import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Odd(Base):
    __tablename__ = "Odds"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    match_id: Mapped[int] = mapped_column()

    first_team: Mapped[str] = mapped_column(nullable=False)
    second_team: Mapped[str] = mapped_column(nullable=False)

    first_odd: Mapped[float] = mapped_column()
    second_odd: Mapped[float] = mapped_column()

    draw_odd: Mapped[float] = mapped_column(server_default=None, nullable=True)

    first_handicap: Mapped[str] = mapped_column(nullable=True)
    second_handicap: Mapped[str] = mapped_column(nullable=True)

    sport_name: Mapped[str] = mapped_column(nullable=False)


class Prediction(Base):
    __tablename__ = "Predictions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    first_team: Mapped[str] = mapped_column()
    second_team: Mapped[str] = mapped_column()

    winner: Mapped[str] = mapped_column()

    bet: Mapped[str] = mapped_column()
    ratio: Mapped[str] = mapped_column()


class TennisOdd(Base):
    __tablename__ = "TennisOdds"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    match_id: Mapped[int] = mapped_column()
    time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    first_player: Mapped[str] = mapped_column()
    second_player: Mapped[str] = mapped_column()

    p1: Mapped[float] = mapped_column()
    p2: Mapped[float] = mapped_column()

    fora_f1: Mapped[str] = mapped_column()
    fora_f2: Mapped[str] = mapped_column()

    
    total_b: Mapped[str] = mapped_column(nullable=True)
    total_m: Mapped[str] = mapped_column(nullable=True)

