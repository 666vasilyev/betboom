import asyncio
import os
import logging

from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.events import NewMessage

from config import config
from src.tg_parse.recognize import text_from_image
from src.db.crud import add_new_prediction, get_match_id_and_winner_count
from src.db.connection import Connection
from src.tg_parse.telegramclient_factory import TelegramClientFactory
from src.betboom_auto.worker import make_bet

logging.basicConfig(level=logging.INFO)


async def handle_new_message(event):

    if event.message.photo:
        logging.info("started downoloading message")
        image = await event.message.download_media(f'{config.MEDIA_DIR}/{event.message.id}')
        logging.info("finished downoloading media")
        # Проверка на существование медиа в посте, которое является картинкой .jpg
        if image is not None and image.split('.')[-1] == 'jpg':
            # Получение текста из изображения
            results = text_from_image(event.message.id)
            if results:
                async with Connection.getConnection() as session:
                    add_new_prediction(
                        session=session,
                        first_team=results[0],
                        second_team=results[1],
                        winner=results[2],
                        bet=results[3],
                        ratio=results[4])
                    
                    logging.info("make prediction in db")

                    # получим match_id для ставки
                    match_id, winner, odd = get_match_id_and_winner_count(
                        session=session,
                        first_team=results[0],
                        second_team=results[1],
                        winner_team=results[2]
                    )

                    # ставим ставку
                    make_bet(
                        match_id=match_id, 
                        winner=winner,
                        odd=odd,
                        )
                    logging.info(f"make bet in betboom")
                    
        os.remove(image)



async def join_channel(client: TelegramClient):
    try:
        await client(JoinChannelRequest(config.CHANNEL_USERNAME))
    except Exception as e:
        logging.error(f"Ошибка при подключении к каналу: {str(e)}")


async def main():

    factory = TelegramClientFactory()
    factory.register_handler(NewMessage(chats=config.CHANNEL_USERNAME), handle_new_message)
    # client = factory.create_client(config.PHONE_NUMBER, config.API_ID, config.API_HASH)
    # await client.start()
    async with factory.create_client(config.PHONE_NUMBER, config.API_ID, config.API_HASH) as client:

        logging.info(f"client started")
        await join_channel(client)  
        logging.info(f"joined channel")
        await client.run_until_disconnected()
        logging.info(f"disconnected")


if __name__ == '__main__':
    asyncio.run(main())