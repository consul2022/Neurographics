"""bot neurography"""
from aiogram import Bot, Dispatcher, F
import asyncio
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import dotenv_values

config = dotenv_values(".env")
BOT_TOKEN = config["BOT_TOKEN"]
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    button = [[KeyboardButton(text="Что умеет бот 🤔")]]
    buttons = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(text=f"Приветствую тебя,{message.chat.first_name}, на моей странице.", reply_markup=buttons)

@dp.message(F.text=="Что умеет бот 🤔")
async def menu(message: Message):
    button = [[KeyboardButton(text="Вконтакте"),KeyboardButton(text="Тарифы")],[KeyboardButton(text="Записаться на консультацию к Светлане")]]
    buttons = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(text="В данном боте можно купить курсы Нейрографиги", reply_markup=buttons)

@dp.message(F.text=="Вконтакте")
async def vk(message: Message):
    button = [[InlineKeyboardButton(text="Перейти в группу ВК", url="https://vk.com/svetlana_guru")]]
    buttons = InlineKeyboardMarkup(inline_keyboard=button)
    await message.answer(text="Добро пожаловать в нашу группу ВК",reply_markup=buttons)

@dp.message(F.text=="Записаться на консультацию")
async def consultation(message: Message):
    button = [[InlineKeyboardButton(text="Записаться", callback_data="consul")]]
    buttons = InlineKeyboardMarkup(inline_keyboard=button)
    await message.answer(text="Забронировать консультацию со Светланой", reply_markup=buttons)

@dp.message(F.text=="Тарифы")
async def tarifs(message: Message):
    button = [[InlineKeyboardButton(text="Знакомство", callback_data="consul"),InlineKeyboardButton(text="Подписка на 3 месяца", callback_data="consul")]]
    buttons = InlineKeyboardMarkup(inline_keyboard=button)
    await message.answer(text="Тарифы", reply_markup=buttons)






async def main():
    await dp.start_polling(bot)
asyncio.run(main())