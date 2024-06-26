import datetime
from google.oauth2 import service_account
from googleapiclient import discovery
from telebot import types
from allowed_users import allowed_users

def create_shift_button(user_id):
    if user_id in allowed_users:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_create_shift = types.KeyboardButton("Создать смену")
        markup.add(btn_create_shift)
        return markup
    else:
        return None

def create_shift_event(bot, message, date, summary):
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    service = discovery.build('calendar', 'v3', credentials=credentials)

    # Проверяем корректность формата даты
    try:
        event_date = datetime.datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        bot.send_message(message.chat.id, "Дата введена некорректно. Пожалуйста, нажмите повторно кнопку 'Создать смену' и введите дату в формате ДД-ММ-ГГГГ (например: 01-01-2024).")
        return

    # Формируем дату и время события на 9:00 UTC+07:00
    event_time = event_date + datetime.timedelta(hours=7)  # Добавляем 7 часов
    event_start = event_time.isoformat() + '+07:00'
    event_end = (event_time + datetime.timedelta(hours=1)).isoformat() + '+07:00'

    # Создаем событие в календаре
    event = {
        'summary': summary,
        'start': {
            'dateTime': event_start,
            'timeZone': 'Asia/Bangkok',  # Указываем временную зону UTC+07:00
        },
        'end': {
            'dateTime': event_end,
            'timeZone': 'Asia/Bangkok',  # Указываем временную зону UTC+07:00
        },
    }

    event = service.events().insert(calendarId='7cf44d58482818e043c1b95b293016277bc379c15b68102f322f276ab657f8e3@group.calendar.google.com', body=event).execute()

    # Отправляем сообщение об успешном создании события
    bot.send_message(message.chat.id, f"Событие '{summary}' успешно создано на {date} в 9:00 UTC+07:00.")
