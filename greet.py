@bot.message_handler(func=lambda message: message.text == "👋 Поздороваться")
def greet(message):
    bot.send_message(message.chat.id, "Добрый день. Я рад, что вы воспользовались мной. Если вы хотите посмотреть актуальные смены на ближайшую неделю, нажмите кнопку \"РАБОТА\".")
