import telebot
from telebot import types
import json
import os

# ========= НАСТРОЙКИ =========

TOKEN = "8397279335:AAHVEyh5sSGDOUcrSukgv3rFZIBp8ywaJdA"

ADMIN_ID = 6391072366 

MANAGER_PHONE = "0666508711"

MANAGER_USERNAME = "profi_protect_official"

CATALOG_FILE = "catalog.pdf"

bot = telebot.TeleBot(TOKEN)

DB_FILE = "clients.json"

# ========= БАЗА =========

def load_db():

    if not os.path.exists(DB_FILE):

        with open(DB_FILE, "w") as f:

            json.dump({}, f)

    with open(DB_FILE, "r") as f:

        return json.load(f)


def save_db(db):

    with open(DB_FILE, "w") as f:

        json.dump(db, f)


def add_client(user):

    db = load_db()

    db[str(user.id)] = user.first_name

    save_db(db)

# ========= START =========

@bot.message_handler(commands=['start'])
def start(message):

    add_client(message.from_user)

    reply = types.ReplyKeyboardMarkup(resize_keyboard=True)

    reply.add("🎨 Каталог кольорів")

    reply.add("📞 Зателефонувати менеджеру")

    inline = types.InlineKeyboardMarkup()

    inline.add(

        types.InlineKeyboardButton(

            "💬 Написати менеджеру",

            url=f"https://t.me/{MANAGER_USERNAME}"

        )

    )

    bot.send_message(

        message.chat.id,

        "Вас вітає бот Profi Protect! 👋",

        reply_markup=reply

    )

    bot.send_message(

        message.chat.id,

        "📩 Зв'язок з менеджером:",

        reply_markup=inline

    )

# ========= CRM =========

@bot.message_handler(commands=['crm'])
def crm(message):

    if message.chat.id != ADMIN_ID:

        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("👥 Клієнти")

    markup.add("📢 Розсилка")

    markup.add("🧾 Надіслати PDF")

    markup.add("🚚 Надіслати ТТН")

    markup.add("📦 Статус замовлення")

    bot.send_message(

        message.chat.id,

        "CRM меню:",

        reply_markup=markup

    )

# ========= СТАТУС =========

status_client = {}

@bot.message_handler(func=lambda m: m.text == "📦 Статус замовлення")
def status_start(message):

    msg = bot.send_message(message.chat.id, "Введіть ID клієнта:")

    bot.register_next_step_handler(msg, status_choose)


def status_choose(message):

    client = message.text

    status_client[message.chat.id] = client

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("📦 Готово")

    markup.add("⚙️ Формується")

    markup.add("🚚 Відправлено")

    msg = bot.send_message(

        message.chat.id,

        "Оберіть статус:",

        reply_markup=markup

    )

    bot.register_next_step_handler(msg, status_send)


def status_send(message):

    client = status_client[message.chat.id]

    status = message.text

    if status == "🚚 Відправлено":

        msg = bot.send_message(message.chat.id, "Введіть ТТН:")

        bot.register_next_step_handler(msg, send_ttn_with_status, client)

    else:

        bot.send_message(

            client,

            f"📦 Статус замовлення:\n{status}"

        )

        bot.send_message(message.chat.id, "✅ Надіслано")


def send_ttn_with_status(message, client):

    ttn = message.text

    bot.send_message(

        client,

        f"📦 Статус замовлення:\n🚚 Відправлено\n\n🚚 ТТН:\n{ttn}"

    )

    bot.send_message(

        message.chat.id,

        "✅ Статус і ТТН надіслано"

    )

# ========= RUN =========

print("BOT STARTED")

bot.infinity_polling()
