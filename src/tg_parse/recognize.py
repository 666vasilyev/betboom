import cv2
import pytesseract
import logging
from utils import find_substring, compare_strings

from src.config import config

# TODO: попрежнему проблема с определением суммы, буква Р определяется то как 2, то как Р, нужно разбираться

logging.basicConfig(level=logging.INFO)

# сгенерированно ChatGPT
def resize_image(image, target_height=1280, fill_color=(0, 0, 0)):
    # Загрузка изображения с использованием OpenCV

    # Получение текущих размеров изображения
    current_height, width, _ = image.shape

    # Проверка, нужно ли изменять размер изображения
    if current_height < target_height:
        # Вычисление разницы в высоте
        height_diff = target_height - current_height

        # Создание нового изображения с дополненной высотой (только сверху)
        top_padding = height_diff
        new_img = cv2.copyMakeBorder(image, top_padding, 0, 0, 0, cv2.BORDER_CONSTANT, value=fill_color)
        new_img = cv2.resize(new_img, (1000, 1000))
        # Возвращение нового изображения
        return new_img
    else:
        # Если изображение уже достаточно большое, вернуть его без изменений
        image = cv2.resize(image, (1000, 1000))
        return image


def extract_text_from_region(image, x_min: int, y_min: int, x_max: int, y_max: int) -> str:
    region = image[y_min:y_max, x_min:x_max]  # Выделение области интереса
    custom_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=\bABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:.'
    text = pytesseract.image_to_string(region, config=custom_config, lang='eng')
    return text


def extract_nums_from_region(image, x_min: int, y_min: int, x_max: int, y_max: int) -> str:
    region = image[y_min:y_max, x_min:x_max]  # Выделение области интереса
    custom_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=1234567890.'
    text = pytesseract.image_to_string(region, config=custom_config, lang='eng')
    return text


def text_from_image(message_id: int):
    raw_image = cv2.imread(f'{config.MEDIA_DIR}/{message_id}.jpg')
    image = resize_image(raw_image)
    # if is_predict:

    # logging.info("It's a predict")
    team_one = extract_text_from_region(image, x_min=50, y_min=585, x_max=430, y_max=690).replace('\n', '')
    team_two = extract_text_from_region(image, x_min=580, y_min=585, x_max=940, y_max=690).replace('\n', '')
    predict = extract_text_from_region(image, x_min=50, y_min=745, x_max=820, y_max=830).replace('\n', '')

    bet = extract_nums_from_region(image, x_min=50, y_min=850, x_max=310, y_max=1000).replace('\n', '')
    ratio = extract_nums_from_region(image, x_min=820, y_min=730, x_max=1000, y_max=840).replace('\n', '')

    logging.info(f'Team one is {team_one}')
    logging.info(f'Team two is {team_two}')
    logging.info(f'Predict is {predict}')
    logging.info(f'Bet is {bet}')
    logging.info(f'Ratio is {ratio}')
    ### ChatGPT написала функцию, которая сравнивает строки и устойчива к опечаткам, надо тестить опять же
    if find_substring(predict, team_one):
        logging.info(f'Find substring is {find_substring(predict, team_one)} for {team_one}')
        winner = team_one
    elif find_substring(predict, team_two):
        logging.info(f'Find substring is {find_substring(predict, team_two)} for {team_one}')
        winner = team_two
    else:
        winner = predict

    logging.info(f'Winner is {winner}')

    logging.info(f'Compare is {compare_strings(team_one, winner)} for {team_one}')
    logging.info(f'Compare is {compare_strings(team_two, winner)} for {team_two}')

    if compare_strings(team_one, winner) or compare_strings(team_two, winner):
        logging.info("It's a predict")


        # бывает так, что Tesseract определяет последний символ в ставке как 8, вместо Р(рубль)
        if bet[-1:] != '0':
            new_bet = bet[:-1]
        else:
            new_bet = bet

        # TODO: сделать постобработку записей
        return (
            team_one, 
            team_two,
            winner, 
            new_bet, 
            ratio
        )
