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
        'x-sbi': 'b46529e1-98f7-4256-930e-445c702d42eb',
    }
    SYNC_DB_URL = os.getenv("DATABASE_URL")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")
    BEAT_SCHEDULE = {
        "sync-parse-odds": {
            "task": "src.betboom_parse.celery_tasks.sync_parse_odds",
            "schedule": timedelta(seconds=15),
        },
        "sync-parse-tennis-odds": {
            "task": "src.betboom_parse.celery_tasks.sync_parse_tennis_odds",
            "schedule": timedelta(seconds=15),
        },
    }
    def broker(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    def backend(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"
    
    
    API_ID: int = os.getenv("API_ID")
    API_HASH: str = os.getenv("API_HASH")
    PHONE_NUMBER: str = os.getenv("PHONE_NUMBER")
    
    # CHANNEL_USERNAME: str = "travobet"
    # CHANNEL_USERNAME: str = "test_channel_for_botsapi3"
    MEDIA_DIR: str = "media"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()