import telebot
from handlers import add_handlers

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        add_handlers(self.bot)

    def start_polling(self):
        self.bot.polling(none_stop=True)

if __name__ == "__main__":
    bot = Bot('Ваш токет чат бота')
    bot.start_polling()

