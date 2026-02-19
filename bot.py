import telebot
from telebot import types

TOKEN = "8397279335:AAHVEyh5sSGDOUcrSukgv3rFZIBp8ywaJdA"

bot = telebot.TeleBot(TOKEN)

# создаём кнопки
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💰 Прайс")
    btn2 = types.KeyboardButton("🎨 Подобрать цвет")
    btn3 = types.KeyboardButton("📞 Связаться")
    markup.add(btn1, btn2, btn3)
    return markup

# команда старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите нужный пункт:",
        reply_markup=main_menu()
    )

# обработка кнопок
@bot.message_handler(func=lambda message: True)
def buttons(message):

    if message.text == "💰 Прайс":
        bot.send_message(
            message.chat.id,
            "Отправьте запрос и мы вышлем актуальный прайс 📄"
        )

    elif message.text == "🎨 Подобрать цвет":
        bot.send_message(
            message.chat.id,
            "Напишите:\n• породу дерева\n• где используется (внутри/снаружи)\n• желаемый цвет\n\nМы подберём лучший вариант 🎨"
        )

    elif message.text == "📞 Связаться":
        bot.send_message(
            message.chat.id,
            "Телефон: +380XXXXXXXXX\nTelegram: @your_username"
        )

bot.infinity_polling()
