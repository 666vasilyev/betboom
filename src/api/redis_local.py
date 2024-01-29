import redis
import json
import logging


logging.basicConfig(level=logging.INFO)

# Подключение к серверу Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# TODO: expiry_seconds нужно забирать из betboom api(конец матча = удаление запси автоматически)
def write_match_data_to_redis(match_id: int, match_data: dict[str, dict[str, float]], expiry_seconds: int):
    """
    Функция для записи данных о матче в формате JSON в Redis по заданному идентификатору матча.

    :param match_id: Идентификатор матча (int)
    :param match_data: Данные о матче в формате JSON
    """
    try:
        json_data = json.dumps(match_data)  # Преобразование данных в JSON строку
        redis_client.setex(
            name=f"match:{match_id}", 
            time=expiry_seconds, 
            value=json_data
        )
        logging.info(f"Данные о матче успешно записаны в Redis под ключом 'match:{match_id}'")
        return f"Данные о матче успешно записаны в Redis под ключом 'match:{match_id}'"
    except redis.RedisError as e:
        logging.error(f"Ошибка при записи в Redis: {e}")
        return f"Ошибка при записи в Redis: {e}"

def read_match_data_from_redis(match_id: int) -> dict[str, dict[str, float]]:
    """
    Функция для считывания данных о матче в формате JSON из Redis по заданному идентификатору матча.

    :param match_id: Идентификатор матча (int)
    :return: Данные о матче в формате JSON, если ключ существует и содержит JSON данные, иначе None
    """
    try:
        json_data = redis_client.get(f"match:{match_id}")
        if json_data is not None:
            data = json.loads(json_data)  # Преобразование JSON строки в объект Python
            logging.info(f"Данные о матче из Redis по идентификатору матча '{match_id}': {data}")
            return data
        else:
            logging.info(f"Данные по идентификатору матча '{match_id}' не найдены в Redis")
            return None
    except (redis.RedisError, json.JSONDecodeError) as e:
        logging.error(f"Ошибка при чтении из Redis: {e}")
        return None

# # Пример использования функций для работы с данными о матче в вашем формате JSON
# match_id = 124
# match_data = {
#     "first_odd": {"minn": 1.1, "maxx": 2.2},
#     "second_odd": {"minn": 3, "maxx": 4},
#     "first_handicap": {"minn": -1, "maxx": 1},
#     "second_handicap": {"minn": -2, "maxx": 2}
# }

# write_match_data_to_redis(match_id, match_data, 1)
# read_match_data_from_redis(match_id)
