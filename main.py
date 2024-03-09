import telebot
from handlers import add_handlers

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        add_handlers(self.bot)

    def start_polling(self):
        self.bot.polling(none_stop=True)

if __name__ == "__main__":
    bot = Bot('7029317973:AAFoUffqtX66UOcGK-ye1B0D299LTl0ze4E')
    bot.start_polling()