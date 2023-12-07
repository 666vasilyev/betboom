from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging

from src.db.models import Odd, Prediction

logging.basicConfig(level=logging.INFO)


def add_new_odds(
        session: Session, 
        new_odds: list[Odd]
        ):
    for new_odd in new_odds:
        # Получаем последнюю запись для данного match_id
        last_odd = (
            session.query(Odd)
            .filter(Odd.match_id == new_odd.match_id)
            .order_by(desc(Odd.id))
            .first()
        )
        if last_odd is None:
            # Если нет предыдущих записей с данным match_id, добавляем новую запись
            session.add(new_odd)
            logging.info(f'new_odd(cause last doesnt exist): {new_odd.match_id}')
        else:
            # Если есть предыдущая запись, проверяем коэффициенты
            if (last_odd.first_odd == new_odd.first_odd and
                last_odd.second_odd == new_odd.second_odd and
                last_odd.first_handicap == new_odd.first_handicap and
                last_odd.second_handicap == new_odd.second_handicap
                ):
                pass
            else:
                session.add(new_odd)
                logging.info(f'new_odd: {new_odd.match_id}')
    session.commit()


def add_new_prediction(
        session: Session,
        first_team: str,
        second_team: str,
        winner: str,
        bet: str,
        ratio: str
        ):
    
    new_prediction = Prediction(
        first_team=first_team,
        second_team=second_team,
        winner=winner,
        bet=bet,
        ratio=ratio
        )
    
    session.add(new_prediction)
    session.commit()


def get_match_id_and_winner_count(session: Session, first_team: str, second_team: str, winner_team: str) -> (int, int):
    # Получаем match_id
    odd = 0
    match = (
        session.query(Odd)
        .filter(Odd.first_team.strip() == first_team, Odd.second_team.strip() == second_team)
        .order_by(Odd.id.desc())
        .first()
    )
    logging.info(f'match: {match.match_id}')
    match_id = match.match_id
    
    # Получаем номер победившей команды
    winner = 0
    if winner_team == first_team:
        winner = 1
        odd = match.first_odd
    else:
        if winner_team == second_team:
            winner = 2
            odd = match.second_odd
    
    logging.info(f'From DB: winner: {winner}, odd: {odd}, match_id: {match_id}')
    return match_id, winner, odd

