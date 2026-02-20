import telebot
from telebot import types
import json
import os

TOKEN = "8397279335:AAHVEyh5sSGDOUcrSukgv3rFZIBp8ywaJdA"
ADMIN_ID = "6391072366"

bot = telebot.TeleBot(TOKEN)

DB = "clients.json"

# база
def load():
    if not os.path.exists(DB):
        return {}
    return json.load(open(DB))

def save(data):
    json.dump(data, open(DB,"w"))

# старт
@bot.message_handler(commands=['start'])
def start(message):

    db = load()
    db[str(message.chat.id)] = {
        "name": message.from_user.first_name,
        "status": "Новий"
    }
    save(db)

    bot.send_message(message.chat.id,"Вітаємо!")

# CRM меню
@bot.message_handler(commands=['crm'])
def crm(message):

    if message.chat.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🧾 Чек PDF")
    markup.add("🚚 ТТН")
    markup.add("📦 Статус")

    bot.send_message(message.chat.id,"CRM:",reply_markup=markup)

# чек
@bot.message_handler(func=lambda m:m.text=="🧾 Чек PDF")
def check(message):

    msg=bot.send_message(message.chat.id,"ID клієнта:")
    bot.register_next_step_handler(msg,send_check)

def send_check(message):

    client=message.text

    file=open("check.pdf","rb")

    bot.send_document(client,file)

    bot.send_message(message.chat.id,"Готово")

# ттн
@bot.message_handler(func=lambda m:m.text=="🚚 ТТН")
def ttn(message):

    msg=bot.send_message(message.chat.id,"ID клієнта:")
    bot.register_next_step_handler(msg,ttn2)

def ttn2(message):

    client=message.text

    msg=bot.send_message(message.chat.id,"Номер ТТН:")
    bot.register_next_step_handler(msg,ttn3,client)

def ttn3(message,client):

    bot.send_message(
        client,
        f"🚚 Ваша ТТН:\n{message.text}"
    )

    bot.send_message(message.chat.id,"Готово")

# статус
@bot.message_handler(func=lambda m:m.text=="📦 Статус")
def status(message):

    msg=bot.send_message(message.chat.id,"ID клієнта:")
    bot.register_next_step_handler(msg,status2)

def status2(message):

    client=message.text

    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("Готово")
    markup.add("Відправлено")
    markup.add("Доставлено")

    msg=bot.send_message(
        message.chat.id,
        "Оберіть:",
        reply_markup=markup
    )

    bot.register_next_step_handler(msg,status3,client)

def status3(message,client):

    bot.send_message(
        client,
        f"📦 Статус:\n{message.text}"
    )

    bot.send_message(message.chat.id,"Готово")

bot.infinity_polling()
