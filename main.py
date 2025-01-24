import logging
import asyncio
from abc import ABC, abstractmethod
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '7666128404:AAF3Ng7rsjhYzpqUbrPIP-aeRXcHqA1teN4'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, message: Message):
        pass

class StartCommandHandler(CommandHandler):
    def __init__(self, keyboard: ReplyKeyboardMarkup):
        self.keyboard = keyboard

    async def handle(self, message: Message):
        await message.reply("Привет! Я твой новый телеграмм бот.", reply_markup=self.keyboard)

class HelpCommandHandler(CommandHandler):
    async def handle(self, message: Message):
        await message.reply("Я могу помочь тебе с различными задачами. Просто выбери нужную опцию на клавиатуре!")

class ShowUserIdHandler(CommandHandler):
    async def handle(self, message: Message):
        await message.reply(f"Ваш ID: {message.from_user.id}")

class ShowUserNickHandler(CommandHandler):
    async def handle(self, message: Message):
        if message.from_user.username:
            await message.reply(f"Ваш ник: @{message.from_user.username}")
        else:
            await message.reply("У вас нет ника в Telegram.")

class KeyboardFactory:
    @staticmethod
    def create_keyboard() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Показать мой ID")],
                [KeyboardButton(text="Показать мой ник")]
            ],
            resize_keyboard=True
        )
        return keyboard

class TelegramBot:
    def __init__(self, api_token: str):
        self.bot = Bot(token=api_token)
        self.dp = Dispatcher()
        self.keyboard = KeyboardFactory.create_keyboard()

        self.command_handlers = {
            'start': StartCommandHandler(self.keyboard),
            'help': HelpCommandHandler(),
        }

        self.message_handlers = {
            "Показать мой ID": ShowUserIdHandler(),
            "Показать мой ник": ShowUserNickHandler()
        }

    def register_handlers(self):
        for command, handler in self.command_handlers.items():
            self.dp.message(Command(commands=[command]))(handler.handle)

        for text, handler in self.message_handlers.items():
            self.dp.message(lambda message: message.text == text)(handler.handle)

        # Обработчик для всех остальных текстовых сообщений
        @self.dp.message(lambda message: True)
        async def default_handler(message: Message):
            await message.reply("Я не понимаю эту команду. Попробуйте использовать клавиатуру для выбора команды.")

    async def run(self):
        self.register_handlers()
        await self.dp.start_polling(self.bot)

if __name__ == '__main__':
    bot = TelegramBot(API_TOKEN)
    asyncio.run(bot.run())
