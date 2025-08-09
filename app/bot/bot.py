import asyncio
import environ
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from pathlib import Path


env = environ.Env(
    DEBUG=(bool, False)
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_file = BASE_DIR / ".env"

if env_file.exists():
    environ.Env.read_env(str(env_file))
    print(f"Загружен .env из: {env_file}")
else:
    print(f"Файл .env не найден по пути: {env_file}")


try:
    TOKEN = env("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN пустой или не найден")
except KeyError:
    raise ValueError("Переменная окружения BOT_TOKEN не найдена")

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I'm a bot created with aiogram.")


async def main() -> None:
    bot = Bot(token=str(TOKEN))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
          