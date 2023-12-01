import asyncio
from telethon import TelegramClient
from config import Config


async def main():
    phone = "6289676645345"
    async with TelegramClient(phone, Config().API_ID, Config().API_HASH) as client:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input("enter code: ")
            await client.sign_in(phone, code)


if __name__ == "__main__":
    asyncio.run(main())