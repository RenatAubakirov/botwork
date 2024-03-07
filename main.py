from __future__ import print_function
import telebot
from telebot import types
import httplib2
import datetime
import time
import config
import telepot
import schedule
from google.oauth2 import service_account
from googleapiclient import discovery

bot = telebot.TeleBot('7029317973:AAFoUffqtX66UOcGK-ye1B0D299LTl0ze4E') ## ЗДЕСЬ ВСТАВЛЯЕМ ТОКЕН БОТА

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("Работа")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "👋 Привет! Я твой бот-помощник в аутстафе ТК95", reply_markup=markup)
## Кнопки
@bot.message_handler(func=lambda message: message.text == "Старт")
def start_command(message):
    bot.send_message(message.chat.id, "Выполняю команду start")

@bot.message_handler(func=lambda message: message.text == "Работа")
def check_calendar(message):
    job(message)
# Количество дней просмотра календаря "7"
def job(message):
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    service = discovery.build('calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end_of_week = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'  # End of the week
    print('Checking events from', now, 'to', end_of_week)

    eventsResult = service.events().list(
        calendarId='7cf44d58482818e043c1b95b293016277bc379c15b68102f322f276ab657f8e3@group.calendar.google.com',
        # Здесь вставляем id именно календаря который используется, находится в настройках редактируемого календаря в пункте интеграция календаря
        timeMin=now,
        timeMax=end_of_week,
        maxResults=100,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = eventsResult.get('items', [])
# Вывод
    if not events:
        bot.send_message(message.chat.id, 'На этой неделе нет событий в календаре.')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event['summary']
            msg = f"<b>{summary}</b> - {start}"
            bot.send_message(message.chat.id, msg, parse_mode='HTML')

# Изменение: Добавлен обработчик для кнопки "Поздороваться"
@bot.message_handler(func=lambda message: message.text == "👋 Поздороваться")
def greet(message):
    bot.send_message(message.chat.id, "Добрый день. Я рад, что вы воспользовались мной. Если вы хотите посмотреть актуальные смены на ближайшую неделю, нажмите кнопку \"РАБОТА\".")


bot.polling(none_stop=True)