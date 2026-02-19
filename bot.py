import telebot

TOKEN = "8397279335:AAHVEyh5ssGDOUcrSukgv3rfZIBp8ywaJdA"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это твой бот 🔥")

bot.infinity_polling()


