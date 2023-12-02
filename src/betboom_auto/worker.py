import requests
import logging

from src.json_local import get_application_json, get_confirmation_json
from src.betboom_auto.headers import headers


# В BetBoom ставка создается двумя пост запросами - один создает заявку и получает внутренний task_id(на фронте мы видим первую менюшку в которой есть кнопка "Подтвердить"),
# а второй запрос уже отправляет task_id и тем самым происходит списание денег со счета
logging.basicConfig(level=logging.INFO)

def make_bet(match_id: int, winner: int, odd: float) -> None:
    ### winner это номер команды(1 или 2) 
    ### match_id это id матча в запросе BetBoom
    logging.info(f"match_id - {match_id}, winner - {winner}")

    # создание зявки на ставку
    bet_application = requests.post('https://api-bifrost.oddin.gg/main/bifrost/query', headers=headers, json=get_application_json(match_id, winner, odd))
    logging.info(f"application status - {bet_application.status_code}")

    # подтверждение ставки
    bet_confirmation = requests.post('https://api-bifrost.oddin.gg/main/bifrost/query', headers=headers, json=get_confirmation_json(match_id, winner, odd))
    logging.info(f"confirmation status - {bet_confirmation.status_code}")

    if bet_application.status_code == 200 and bet_confirmation.status_code == 200:
        logging.info(f"Successfully")
    else:
        logging.info(f"Failed")
