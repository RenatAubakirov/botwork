from telebot import types
from check_calendar import check_calendar
from create_shift_button import create_shift_event
from allowed_users import allowed_users

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

        bot.send_message(message.chat.id, f"👋 Привет! Я твой бот-помощник в аутстафе. Ваше имя пользователя: {message.from_user.username}", reply_markup=user_markup)

    @bot.message_handler(func=lambda message: message.text == "👋 Поздороваться")
    def greet(message):
        bot.send_message(message.chat.id, "Добрый день. Я рад, что вы воспользовались мной. Если вы хотите посмотреть актуальные смены на ближайшую неделю, нажмите кнопку \"РАБОТА\".")

    @bot.message_handler(func=lambda message: message.text == "Работа")
    def check_calendar_handler(message):
        try:
            check_calendar(bot, message)
        except Exception as e:
            print("Произошла ошибка: ", e)
            bot.send_message(message.chat.id, "Сейчас есть проблемы с сетью. Пожалуйста, попробуйте снова через 20 минут.")

    @bot.message_handler(func=lambda message: message.text == "Создать смену")
    def create_shift(message):
        # Запрашиваем у пользователя дату и тему события
        bot.send_message(message.chat.id, "На какую дату вы хотите создать смену (дд-мм-гггг)?")
        bot.register_next_step_handler(message, ask_date)

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
