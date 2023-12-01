# celery -A src.core.celery.celery_tasks worker --loglevel=INFO --purge
# celery -A src.core.celery.celery_tasks beat --loglevel=INFO
import logging
import asyncio
from celery import Celery

from src.betboom_parse.get_odds import parse_odds
from src.config import config

logging.basicConfig(level=logging.INFO)

celery = Celery(
    "celery_tasks",
    broker=config.broker(),
    backend=config.backend(),
)

celery.conf.update(
    result_backend=config.backend(),
    beat_schedule=config.BEAT_SCHEDULE,
)


@celery.task
def sync_parse_odds():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        parse_odds()
    )
