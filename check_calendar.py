import datetime
from google.oauth2 import service_account
from googleapiclient import discovery

def check_calendar(bot, message):
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    service = discovery.build('calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end_of_week = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'  # End of the week
    print('Checking events from', now, 'to', end_of_week)

    eventsResult = service.events().list(
        calendarId='7cf44d58482818e043c1b95b293016277bc379c15b68102f322f276ab657f8e3@group.calendar.google.com',
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
            # Извлекаем дату из времени начала события
            event_date = start.split("T")[0]
            # Формируем сообщение с темой и датой события
            msg = f"<b>{summary}</b> - {event_date}"
            bot.send_message(message.chat.id, msg, parse_mode='HTML')
