from telebot import types
from check_calendar import check_calendar

def add_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Поздороваться")
        btn2 = types.KeyboardButton("Работа")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "👋 Привет! Я твой бот-помощник в аутстафе", reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == "👋 Поздороваться")
    def greet(message):
        bot.send_message(message.chat.id, "Добрый день. Я рад, что вы воспользовались мной. Если вы хотите посмотреть актуальные смены на ближайшую неделю, нажмите кнопку \"РАБОТА\".")

    @bot.message_handler(func=lambda message: message.text == "Работа")
    def check_calendar_handler(message):
        check_calendar(bot, message)
