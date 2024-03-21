from telebot import types
from check_calendar import check_calendar
from create_shift_button import create_shift_event
from allowed_users import allowed_users

import datetime  # добавлен импорт модуля datetime

# Функция для записи действий пользователей в файл
def log_user_action(username, action, timestamp):
    with open("user_actions.txt", "a") as file:
        file.write(f"[{timestamp}] Пользователь {username} выполнил действие: {action}\n")


def add_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Поздороваться")
        btn2 = types.KeyboardButton("Работа")
        user_markup.add(btn1, btn2)

        # Проверяем, принадлежит ли пользователь к списку разрешенных
        if message.from_user.username in allowed_users:
            # Добавляем кнопку "Создать смену" только для разрешенных пользователей
            btn3 = types.KeyboardButton("Создать смену")
            user_markup.add(btn3)

        bot.send_message(message.chat.id, f"👋 Привет! Я твой бот-помощник в СТО. Ваше имя пользователя: {message.from_user.username}", reply_markup=user_markup)

    @bot.message_handler(func=lambda message: message.text == "👋 Поздороваться")
    def greet(message):
        bot.send_message(message.chat.id, "Добрый день. Я рад, что вы воспользовались мной. Если вы хотите посмотреть актуальные смены на ближайшую неделю, нажмите кнопку \"РАБОТА\".")

    @bot.message_handler(func=lambda message: message.text == "Работа")
    def check_calendar_handler(message):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_user_action(message.from_user.username, "нажал кнопку 'Работа'", timestamp)  # записываем действие пользователя в файл
            check_calendar(bot, message)
        except Exception as e:
            print("Произошла ошибка: ", e)
            bot.send_message(message.chat.id, "Сейчас есть проблемы с сетью. Пожалуйста, попробуйте снова через 20 минут.")

    @bot.message_handler(func=lambda message: message.text == "Создать смену")
    def create_shift(message):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_user_action(message.from_user.username, "нажал кнопку 'Создать смену'", timestamp)  # записываем действие пользователя в файл
            # Запрашиваем у пользователя дату и тему события
            bot.send_message(message.chat.id, "На какую дату вы хотите создать смену (дд-мм-гггг, Например: 01-01-2024, прошу соблюсти ввод даты как в примере, иначе смена не создастся)?")
            bot.register_next_step_handler(message, ask_date)
        except Exception as e:
            print("Произошла ошибка: ", e)
            bot.send_message(message.chat.id, "Сейчас есть проблемы с сетью. Пожалуйста, попробуйте снова через 20 минут.")

    def ask_date(message):
        date = message.text
        # Запрашиваем тему события
        bot.send_message(message.chat.id, "Напишите тему смены:")
        bot.register_next_step_handler(message, lambda message: ask_summary(message, date))

    def ask_summary(message, date):
        summary = message.text
        try:
            # Создаем событие в календаре
            create_shift_event(bot, message, date, summary)
        except Exception as e:
            print("Произошла ошибка: ", e)
            bot.send_message(message.chat.id, "Сейчас есть проблемы с сетью. Пожалуйста, попробуйте снова через 20 минут.")
