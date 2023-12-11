from datetime import timedelta
import os
from dotenv import load_dotenv

class Config():
    
    load_dotenv()
    HEADERS = {
        'authority': 'api-bifrost.oddin.gg',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://bifrost.oddin.gg',
        'referer': 'https://bifrost.oddin.gg/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-api-key': 'b94ac61d-b060-4892-8242-923bf2303a38',
        'x-display-resolution': '674x546',
        'x-locale': 'RU',
        'x-sbi': 'd13c565b-ac5c-4142-8b3f-9d6fef2dcff3',
    }
    SYNC_DB_URL = os.getenv("DATABASE_URL")
    # SYNC_DB_URL: str = "postgresql+psycopg2://postgres:123@db:5432/betboom"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    LOG_LEVEL: str = "INFO"
    BEAT_SCHEDULE = {
        "sync-parse-odds": {
            "task": "src.betboom_parse.celery_tasks.sync_parse_odds",
            "schedule": timedelta(seconds=15),
        }
    }
    def broker(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    def backend(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"
    
    
    API_ID: int = 24345605
    API_HASH: str = "955f309500331d79b9f936b4d410a50e"
    PHONE_NUMBER: str = "src/tg_parse/sessions/6289676645345"
    
    CHANNEL_USERNAME: str = "travobet"
    # CHANNEL_USERNAME: str = "test_channel_for_botsapi3"
    MEDIA_DIR: str = "media"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()