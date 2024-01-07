"""bot neurography"""
from aiogram import Bot, Dispatcher, F
import asyncio

from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery, LabeledPrice, PreCheckoutQuery
from dotenv import dotenv_values

config = dotenv_values(".env")
BOT_TOKEN = config["BOT_TOKEN"]
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

#admin_id = 593849628
admin_id=1357975325
async def payment_process(price, name, description, chat_id):
    button = [[InlineKeyboardButton(text="Оформить подписку", pay=True)]]
    await bot.send_invoice(
        chat_id=chat_id,
        title=name,
        description=description,
        provider_token=config["PAY_TOKEN"],
        currency="RUB",
        # photo_url="https://i.ibb.co/448wWGc/avatar.png",
        # photo_width=640,
        # photo_height=640,
        # is_flexible=False,
        prices=[LabeledPrice(label="Цена", amount=round(price * 100,2))],
        start_parameter="time-machine-example",
        payload=name,
        need_name=True,
        #need_email=True,
        need_phone_number=True,
        send_email_to_provider=True,
        # provider_data={
        #     "receipt": {
        #         "items": [
        #             {
        #                 "description": "товар ",
        #                 "quantity": "1.00",
        #                 "amount": {
        #                     "value": str(price),
        #                     "currency": "RUB",
        #                 },
        #                 "vat_code": 2,
        #             }
        #         ]
        #     }
        # },
        reply_markup=InlineKeyboardMarkup(inline_keyboard=button)
    )

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

@dp.message(F.text=="Записаться на консультацию к Светлане")
async def consultation(message: Message):
    button = [[InlineKeyboardButton(text="Записаться", url="https://t.me/Aronsveta7")]]
    buttons = InlineKeyboardMarkup(inline_keyboard=button)
    await message.answer(text="Забронировать консультацию со Светланой", reply_markup=buttons)

@dp.message(F.text=="Тарифы")
async def tarifs(message: Message):
    button = [[InlineKeyboardButton(text="Знакомство", callback_data="pay|acquaintance"),InlineKeyboardButton(text="Подписка на 3 месяца", callback_data="pay|subscription")]]
    buttons = InlineKeyboardMarkup(inline_keyboard=button)
    await message.answer(text="Тарифы", reply_markup=buttons)


@dp.callback_query()
async def pay(callback: CallbackQuery):
    data = callback.data.split("|")
    if data[0] == "pay":
        if data[1] == "acquaintance":
            await payment_process(990,"Знакомство","4 онлайн урока по Нейрографики + медитации",callback.message.chat.id)
        elif data[1] == "subscription":
            await payment_process(3300,"Подписка на 3 месяца","12 уроков + медитации + практики с домашним заданием",callback.message.chat.id)


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(
    lambda message: message.content_type
                    in {ContentType.SUCCESSFUL_PAYMENT}
)
async def got_payment(message: Message):
    data = message.successful_payment.invoice_payload
    await message.answer(f"Оплата прошла успешно! Вы приобрели \"{data}\".В ближайшее время Светлана с Вами свяжется")
    if message.chat.username is not None:
        await bot.send_message(chat_id=admin_id, text=f"@{message.chat.username} оформил(а) \"{data}\"")
    else:
        await bot.send_message(chat_id=admin_id, text=f"tg://user?id={message.chat.id} оформил(а) \"{data}\"")






async def main():
    await dp.start_polling(bot)
asyncio.run(main())