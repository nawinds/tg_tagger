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


@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("This is a bot for tagging admins in Telegram supergroups based on their custom title.\n"
                         "E.g. to tag all admins you can write one of these examples:\n"
                         "- /all <...>\n"
                         "- /t all <...>\n"
                         "- /group all <...>\n"
                         "- /t all, <...>\n"
                         "- /group all, <...>\n"
                         "\n"
                         "If some of your admins have the same title \"A room\", "
                         "you can try these commands to tag them:\n"
                         "- /t A <...>\n"
                         "- /group A <...>\n"
                         "- /t A, <...>\n"
                         "- /group A room <...>\n"
                         "\n"
                         "---\n"
                         "If you would like to make a bot of your own, "
                         "you can view and run the code in [main.py]"
                         "(https://github.com/nawinds/tg_tagger/blob/master/main.py) file. [Full source code]"
                         "(https://github.com/nawinds/tg_tagger)\n"
                         "\n"
                         "Feel free to write me! My contacts are on my [nawinds.top](https://nawinds.top) website.",
                         parse_mode="markdown")


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
