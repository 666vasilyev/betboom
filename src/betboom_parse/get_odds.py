import json
import requests
import logging


from src.config import config 

from src.betboom_parse.esports import Esport
from src.utils import hash_coder
from src.json_local import get_json_for_all_matches

from src.db.crud import add_new_odds
from src.db.models import Odd
from src.db.connection import Connection

logging.basicConfig(level=logging.INFO)

# работа с requests и с сервером BetBoom. На данном этапе получаем данные из сервера
def get_nodes(sport: Esport):
    response = requests.post(
        'https://api-bifrost.oddin.gg/main/bifrost/query', 
        headers=config.HEADERS, 
        json=get_json_for_all_matches(sport.value)
        )

    try:
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        logging.error(f'JSONDecodeError: {e}')
        raise TypeError(f'JSONDecodeError: {e}')
        
    return data['data']['allMatch']['edges']


# работа с данными с сервера, которые представляют собой nodes = [], где каждая node - содержит информацию о коэффициентах
def parse_info_from_node(sport: Esport, node: dict):
    main_market_groups = node['node']['mainMarketGroups']

    # идентификатор команды
    raw_match_id = node['node']['id']
    match_id = int(hash_coder(raw_match_id).split(':')[2])

    if isinstance(main_market_groups, list) and len(main_market_groups) > 0:
        # название команд
        first_team = main_market_groups[0]['selections'][0]['name']
        second_team = main_market_groups[0]['selections'][1]['name']

        # коэффициент на выигрыш
        first_odd = main_market_groups[0]['markets'][0]['outcomes'][0]['odds']
        second_odd = main_market_groups[0]['markets'][0]['outcomes'][1]['odds']

        # коэффициент на фору по картам
        try:
            first_handicap = main_market_groups[1]['markets'][0]['outcomes'][0]['odds']
            second_handicap = main_market_groups[1]['markets'][0]['outcomes'][1]['odds']

            info = float(main_market_groups[1]['markets'][0]['info'])

            first_handicap_db = f'{info}:{first_handicap}'
            second_handicap_db = f'{-1*info}:{second_handicap}'

        except Exception as e:
            # logging.error(f'Handicaps not found for {match_id}')

            info = 0
            first_handicap_db = ''
            second_handicap_db = ''

        return Odd(
                match_id=match_id,
                first_team=first_team,
                second_team=second_team,
                first_odd=first_odd,
                second_odd=second_odd,
                first_handicap=first_handicap_db,
                second_handicap=second_handicap_db,
                sport_name=str(sport.name)
                )
    else:
        logging.error("Main Market Groups not found")
        return None


# main
async def parse_odds():
    data_to_add = []
    nodes = []
    for sport in Esport:
        try:
            nodes = get_nodes(sport=sport)
        except Exception as e:
            logging.error(f'Exception: {e}')

        for node in nodes:
            try:
                odd = parse_info_from_node(sport, node)
            except Exception as e:
                logging.error(f'Exception: {e}')

            if odd is not None:
                data_to_add.append(odd)

        # данные отправляются в базу данных сразу массивом, чтобы не обрабатывать каждое значение по отдельности
        # и тем самым сэкономить время работы программы
        async with Connection.getConnection() as session:
            add_new_odds(session, data_to_add)
        data_to_add = []

        