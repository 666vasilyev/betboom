import json
import requests
import logging

from src.betboom_parse.tennis.tenniscfg import params, headers
from src.db.models import TennisOdd
from src.db.connection import Connection
from src.db.crud import add_new_tennis_odds

logging.basicConfig(level=logging.INFO)

def get_tennis_nodes() -> dict:    
    response = requests.get(
        'https://sport.betboom.ru/6dd89319-0ee9-4077-9442-db2a408c2222/prematch/geteventslist',
        params=params,
        headers=headers,
    )
    try:
            data = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
            logging.error(f'JSONDecodeError: {e}')
            raise TypeError(f'JSONDecodeError: {e}')  
    return data


# работа с данными с сервера, которые представляют собой nodes = [], где каждая node - содержит информацию о коэффициентах
def parse_info_from_tennis_node(node: dict): 

    # logging.info('--------------------------------')

    total_b = None
    total_m = None
    match_id=node['Id']
    time=node['D']

    first_player=node['HT']
    second_player=node['AT']

    p1=node['StakeTypes'][0]['Stakes'][0]['F']
    p2=node['StakeTypes'][0]['Stakes'][1]['F']

    fora_f1=f"{node['StakeTypes'][1]['Stakes'][0]['A']}:{node['StakeTypes'][1]['Stakes'][0]['F']}"
    fora_f2=f"{node['StakeTypes'][1]['Stakes'][1]['A']}:{node['StakeTypes'][1]['Stakes'][1]['F']}"

    try:
        total_b = f"{node['StakeTypes'][2]['Stakes'][0]['A']}:{node['StakeTypes'][2]['Stakes'][0]['F']}"
        total_m = f"{node['StakeTypes'][2]['Stakes'][1]['A']}:{node['StakeTypes'][2]['Stakes'][1]['F']}"
    except Exception as e:
        logging.error(f"Failed to find totals for {node['Id']}")

    return TennisOdd(
        match_id=match_id,
        time=time,

        first_player=first_player,
        second_player=second_player,

        p1=p1,
        p2=p2, 

        fora_f1=fora_f1,
        fora_f2=fora_f2,

        total_b=total_b,
        total_m=total_m,
    )


# main
async def parse_tennis():
    data_to_add = []
    for node in get_tennis_nodes():
        try:
            odd = parse_info_from_tennis_node(node)
        except Exception as e:
            logging.error(f'Failed - {str(e)}')

        if odd is not None:
                data_to_add.append(odd)

        # данные отправляются в базу данных сразу массивом, чтобы не обрабатывать каждое значение по отдельности
        # и тем самым сэкономить время работы программы
        async with Connection.getConnection() as session:
            add_new_tennis_odds(session, data_to_add)
        data_to_add = []
