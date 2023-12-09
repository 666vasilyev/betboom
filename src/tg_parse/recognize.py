import cv2
import pytesseract
import logging

from src.config import config

# TODO: попрежнему проблема с определением суммы, буква Р определяется то как 2, то как Р, нужно разбираться

logging.basicConfig(level=logging.INFO)

def resize_image(image):
    return cv2.resize(image, (1000, 1000))

def extract_text_from_region(image, x_min: int, y_min: int, x_max: int, y_max: int) -> str:
    region = image[y_min:y_max, x_min:x_max]  # Выделение области интереса
    custom_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:.'
    text = pytesseract.image_to_string(region, config=custom_config, lang='eng')
    return text


def extract_nums_from_region(image, x_min: int, y_min: int, x_max: int, y_max: int) -> str:
    region = image[y_min:y_max, x_min:x_max]  # Выделение области интереса
    custom_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=1234567890.'
    text = pytesseract.image_to_string(region, config=custom_config, lang='eng')
    return text


def is_predict(image) -> bool:
    return extract_text_from_region(image, x_min=0, y_min=0, x_max=1000, y_max=240).replace('\n', '') == 'BetBoom'

def text_from_image(message_id: int):
    raw_image = cv2.imread(f'{config.MEDIA_DIR}/{message_id}.jpg')
    image = resize_image(raw_image)
    if is_predict:

        logging.info("It's a predict")
        team_one = extract_text_from_region(image, x_min=50, y_min=585, x_max=430, y_max=690).replace('\n', '')
        team_two = extract_text_from_region(image, x_min=580, y_min=585, x_max=940, y_max=690).replace('\n', '')
        predict = extract_text_from_region(image, x_min=50, y_min=745, x_max=820, y_max=830).replace('\n', '')

        bet = extract_nums_from_region(image, x_min=50, y_min=850, x_max=310, y_max=1000).replace('\n', '')
        ratio = extract_nums_from_region(image, x_min=820, y_min=730, x_max=1000, y_max=840).replace('\n', '')

        # TODO: нужно написать функцию, которая будет устойчива к ошибкам, и правильно определяла название команд.
        ### Пример: Cloud9 превратился в Cloudg, а winner = VISAS.OO(что это вообще?)
        logging.info(bet)
        # вместо полного названия команды идет поиск по последним трем символам в названии, чтобы уменьшить число ошибок,
        # когда tesseract ошибается в одном символе в конце к примеру
        if predict.find(team_one[-3:]) != -1:
            winner = team_one
        elif predict.find(team_two[-3:]) != -1:
            winner = team_two
        else:
            winner = predict

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
