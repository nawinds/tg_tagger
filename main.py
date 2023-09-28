import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
bot = Bot(token=getenv("TOKEN"))


async def main() -> None:
    await dp.start_polling(bot)


@dp.message(Command("group", "all", "t"), F.chat.type == "supergroup")
async def tag(message: types.Message):
    admins = await message.chat.get_administrators()
    splitted = message.text.split(" ")

    if message.text.startswith("/all"):
        target = admins
    else:
        if len(splitted) < 2:
            return

        code = splitted[1].split(",")[0]
        if code == "all" or message.text.startswith("/all"):
            target = admins
        else:
            target = [admin for admin in admins if admin.custom_title.split()[0] == code]

    if target:
        await message.reply(", ".join([f"[{i.user.first_name}](tg://user?id={i.user.id})" for i in target]),
                            parse_mode="markdown")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
