import info
from base import DataFetcherAfisha, DataFetcherCategory, Days
from info import *
import logging
import aiogram
from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import datetime

logging.basicConfig(level=logging.INFO)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

YOUR_TOKEN = ''
bot = Bot(token=YOUR_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot)

'''Стартовое сообщение'''


# 9 числа стартовое сообщение меняется на сообщение о закрытии

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    if check_date():
        await bot.send_message(message.chat.id, text=info.bot_end_message, parse_mode='html')
    else:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton('Начать', callback_data='main_menu')
        markup.row(button)
        await bot.send_message(message.chat.id, text=info.bot_start_message,
                               parse_mode='html', reply_markup=markup)


'''Стартовое меню'''


def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Интересы", callback_data="menu1"),
               InlineKeyboardButton("Афиша", callback_data="menu2"))
    return markup


'''Генерация меню'''


def create_menu_second(buttons):
    markup = InlineKeyboardMarkup()
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            button1 = InlineKeyboardButton(buttons[i][0], callback_data=buttons[i][1])
            button2 = InlineKeyboardButton(buttons[i + 1][0], callback_data=buttons[i + 1][1])
            markup.add(button1, button2)
        else:
            button1 = InlineKeyboardButton(buttons[i][0], callback_data=buttons[i][1])
            markup.insert(button1)
    markup.add(InlineKeyboardButton("Показать меню", callback_data="main_menu"))
    return markup


menu1 = create_menu_second(menu1_buttons)
menu2 = create_menu_second(menu2_buttons)
menu2_8jan = create_menu_second(menu2_buttons_8jan)

'''Обработка кнопок меню'''


@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def process_main_menu(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=info.menu_message, reply_markup=main_menu())


@dp.callback_query_handler(lambda c: c.data == 'menu1')
async def process_main_menu(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=info.category_message, reply_markup=menu1, parse_mode='html')


@dp.callback_query_handler(lambda c: c.data == 'menu2')
async def process_main_menu(callback_query: types.CallbackQuery):
    today = datetime.date.today()
    if today.year >= 2024 and (today.month == 1 and today.day == 8):  # изменение меню 8 числа
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=info.afisha_message, reply_markup=menu2_8jan, parse_mode='html')
    elif check_date():
        await start_command(callback_query.message)
    else:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=info.afisha_message, reply_markup=menu2, parse_mode='html')


'''Функция, для изменения работы кнопок 9 января'''


def check_date():
    today = datetime.date.today()
    if today.year >= 2024 and (today.month > 1 or (today.month == 1 and today.day >= 9)):
        return True
    else:
        return False


'''Интересы, ниже обработка кнопок'''


async def process_category_menu(callback_query: types.CallbackQuery, api_parameter, category_message):
    try:
        data = DataFetcherCategory(api_parameter=api_parameter)
        data_category = data.fetch_data()
        text = ''
        if len(data_category[0]) == 0:
            text += info.category_empty_message
        else:
            for item in data_category[0]:
                text += f"<a href='{item['Ссылка']}?utm_source=tg-bot'>{item['Название']}</a>\n\n"
            text += category_message
            text += info.second_message_category
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=text,
                                    parse_mode='HTML', disable_web_page_preview=True, reply_markup=menu1)
    except Exception as e:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id, text=data_category[1],
                                    reply_markup=menu1, disable_web_page_preview=True, parse_mode='HTML')


@dp.callback_query_handler(lambda c: c.data == 'menu1_katki')
async def process_menu1_katki(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_category_menu(callback_query, api_parameter='katki', category_message=info.category_rp)


@dp.callback_query_handler(lambda c: c.data == 'menu1_museum')
async def process_menu1_museum(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_category_menu(callback_query, api_parameter='museu,',
                                    category_message=info.category_rp)


@dp.callback_query_handler(lambda c: c.data == 'menu1_ex')
async def process_menu1_ex(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_category_menu(callback_query, api_parameter='ex',
                                    category_message=info.category_rp)


@dp.callback_query_handler(lambda c: c.data == 'menu1_festwiner')
async def process_menu1_festwinter(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_category_menu(callback_query, api_parameter='winter',
                                    category_message=info.category_usadba)


@dp.callback_query_handler(lambda c: c.data == 'menu1_festtea')
async def process_menu1_festtea(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_category_menu(callback_query, api_parameter='tea',
                                    category_message=info.category_chaepitie)


@dp.callback_query_handler(lambda c: c.data == 'menu1_gastr')
async def process_menu1_gastr(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_category_menu(callback_query, api_parameter='gastr',
                                    category_message=info.category_turnir)


'''Афиша, ниже обработка кнопок'''


async def process_afisha_menu(callback_query: types.CallbackQuery, date_end, date_start, day_end, day_start,
                              is_next_week=False):
    try:
        data_fetcher = DataFetcherAfisha(date_end=date_end, date_start=date_start, day_end=day_end,
                                         day_start=day_start)
        data_afisha = data_fetcher.fetch_data()
        text = f"\U0001F4C5 <b>{data_afisha[0]}:</b>\n\n"
        today = datetime.date.today()
        if today.year >= 2024 and (today.month == 1 and today.day == 8):  # изменение меню 8 числа
            reply_markup = menu2_8jan
        else:
            reply_markup = menu2
        if len(data_afisha[1]) == 0:
            text += info.afisha_empty_message
        else:
            for event in data_afisha[1]:
                try:
                    startdate = datetime.datetime.strptime(event['Дата_начала'], "%Y-%m-%d")
                    enddate = datetime.datetime.strptime(event['Дата_окончания'], "%Y-%m-%d")
                except (ValueError, TypeError):
                    startdate = None
                    enddate = None
                formatteddate1 = startdate.strftime("%d.%m") if startdate else ''
                formatteddate2 = enddate.strftime("%d.%m") if enddate else ''
                category = event['Категория']
                link = event['Ссылка']
                title = event['Название']
                if is_next_week:
                    if enddate is None:
                        text += f"<b>{formatteddate1}</b> <b>{category}</b> // <a href='{link}'>{title}</a>\n\n"
                    elif enddate and startdate:
                        text += f"<b>{formatteddate1} - {formatteddate2}</b> <b>{category}</b> // <a href='{link}'>{title}</a>\n\n"
                    else:
                        text += f"<b>{category}</b> // <a href='{link}'>{title}</a>\n\n"
                else:
                    text += f"<b>{category}</b> // <a href='{link}'>{title}</a>\n\n"
        text += info.second_message_afisha
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=text,
                                    parse_mode='HTML', disable_web_page_preview=True, reply_markup=reply_markup)
    except Exception as e:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=data_afisha[2],
                                    reply_markup=menu2, disable_web_page_preview=True, parse_mode='HTML')


@dp.callback_query_handler(lambda c: c.data == 'menu2_today')
async def process_menu2_today(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_afisha_menu(callback_query, date_end=Days.today_str, date_start=Days.today_str,
                                  day_end=Days.today_day, day_start=Days.today_day)


@dp.callback_query_handler(lambda c: c.data == 'menu2_tomorrow')
async def process_menu2_tomorrow(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_afisha_menu(callback_query, date_end=Days.tomorrow_str, date_start=Days.tomorrow_str,
                                  day_end=Days.tomorrow_day, day_start=Days.tomorrow_day)


@dp.callback_query_handler(lambda c: c.data == 'menu2_next_week')
async def process_menu2_next_weekend(callback_query: types.CallbackQuery):
    if check_date():
        await start_command(callback_query.message)
    else:
        await process_afisha_menu(callback_query, date_end=Days.next_week_day_str, date_start=Days.today_str,
                                  day_end=Days.next_week_day_day, day_start=Days.today_day, is_next_week=True)


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
