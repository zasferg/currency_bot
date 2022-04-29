import parsed_page

from telegram_app import bot,dp

from aiogram.types import Message ,ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from config import admin_id

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


@dp.message_handler(commands=['start'])
async def start_message(message:Message):
    start_buttons = ['Полная таблица', 'InSync by Alfa-Bank','imbanking',
                     'Паритетбанк','Белгазпромбанк','Технобанк','БПС-Сбербанк','МТБанк','Статусбанк','БСБ Банк',
                     'Белагропромбанк','БНБ-Банк','Решение','Приорбанк','РРБ-Банк','Альфа-Банк','Дабрабыт',
                     'Белинвестбанк','Беларусбанк','ТК Банк']

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Выберите банк', reply_markup=keyboard)

@dp.message_handler(Text(equals='Полная таблица'))
async def currency_table(message:Message):
    await parsed_page.get_data()
    file = await parsed_page.convert_to_xls()
    chat_id = message.chat.id
    await bot.send_document(chat_id, document=open(file, 'rb'))

@dp.message_handler()
async def currency_message(message:Message):
    try:
        data = await parsed_page.get_data()
        for i in range(len(data)):
            if message.text in data[i]['Bank']:
                Date = str(data[i]['Date'])
                USD_sell = str(data[i]['USD sell'])
                USD_buy = str(data[i]['USD buy'])
                EUR_sell = str(data[i]['EUR sell'])
                EUR_buy = str(data[i]['EUR buy'])
                RUB_sell = str(data[i]['RUB sell'])
                RUB_buy = str(data[i]['RUB buy'])

                await message.reply(f'Дата:{Date}\n'
                        f'USD продажа:{USD_sell}\n'
                        f'USD покупка:{USD_buy}\n'
                        f'EUR продажа:{EUR_sell}\n'
                        f'EUR покупка:{EUR_buy}\n'
                        f'RUB продажа:{RUB_sell}\n'
                        f'RUB покупка:{RUB_buy}\n')

    except Exception as e:
        print(e)
        await message.reply("Произошла ошибка")


