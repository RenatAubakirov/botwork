import datetime
from google.oauth2 import service_account
from googleapiclient import discovery

def add_shift_to_calendar(bot, message):
    # Получаем текущее время для установки начала смены
    start_time = datetime.datetime.utcnow().isoformat() + 'Z'
    # Получаем время окончания смены (в данном случае, через 8 часов после начала)
    end_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).isoformat() + 'Z'

    # Создаем JSON объект для события
    event = {
        'summary': 'Новая смена',  # Тема события
        'description': 'Описание смены',  # Описание события
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }

    # Авторизуемся в Google API
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    service = discovery.build('calendar', 'v3', credentials=credentials)

    # Пытаемся добавить событие в календарь
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        # Если событие успешно добавлено, отправляем сообщение об этом
        bot.send_message(message.chat.id, 'Смена успешно добавлена в календарь.')
    except Exception as e:
        # Если произошла ошибка, отправляем сообщение об этом
        bot.send_message(message.chat.id, f'Ошибка при добавлении смены в календарь: {str(e)}')
