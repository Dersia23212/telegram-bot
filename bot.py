import telebot

TOKEN = "ВСТАВЬ_СЮДА_TOKEN"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это твой бот 🔥")

bot.infinity_polling()
