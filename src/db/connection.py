import asyncio
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
import logging

from src.config import config


logger = logging.getLogger(__name__)


class Connection:
	c: Session
	mutex: asyncio.Lock
	isActive: bool
	engine = sqlalchemy.create_engine(config.SYNC_DB_URL,
				   connect_args={"connect_timeout": 10},
				   )
	db_connection_singleton = None

	def __init__(self):
		self.mutex = asyncio.Lock()

	async def __aenter__(self):
		await self.mutex.acquire()
		self.c = sessionmaker(self.engine, expire_on_commit=False, autoflush=True)
		return self.c()
	
	async def __aexit__(self, a, b, c):
		self.mutex.release()

	@classmethod
	def getConnection(cls) -> "Connection":
		if not cls.db_connection_singleton:
			cls.db_connection_singleton = Connection()

		return cls.db_connection_singleton
