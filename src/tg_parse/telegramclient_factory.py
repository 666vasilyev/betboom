import logging
from typing import Callable, Any, NamedTuple

from telethon import TelegramClient
from telethon.events.common import EventBuilder


Handler = Callable[[Any], None]

logging.basicConfig(level=logging.INFO)

class HandlerWrapper(NamedTuple):
    event: EventBuilder
    handler: Handler

class TelegramClientFactoryException(Exception):
    pass


class TelegramClientFactory:
    def __init__(self):
        self.handlers: list[HandlerWrapper] = []

    def register_handler(self, event: EventBuilder, handler: Handler):
        self.handlers.append(HandlerWrapper(event=event, handler=handler))

    def create_client(self, phone_number: str, api_id: int, api_hash: str) -> TelegramClient:
        try:
            
            client = TelegramClient(phone_number, api_id, api_hash)
            
        except Exception as e:
            logging.info(f"Ошибка при подключении к каналу: {str(e)}")
            raise TelegramClientFactoryException from e
        for event, handler in self.handlers:
            client.on(event)(handler)
        return client
