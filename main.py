import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = 'TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def webapp_builder():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Open Web-app",
        web_app=WebAppInfo(url="link")
    )
    return builder.as_markup()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply('Open', reply_markup=webapp_builder())


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
