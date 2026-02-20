import telebot
from telebot import types
import json
import os

# ===== НАСТРОЙКИ =====

TOKEN = "8397279335:AAHVEyh5sSGDOUcrSukgv3rFZIBp8ywaJdA"

ADMIN_ID = 6391072366

MANAGER_PHONE = "+380666508711"

MANAGER_USERNAME = "profi_protect_official"

bot = telebot.TeleBot(TOKEN)

DB_FILE = "clients.json"

# ===== БАЗА =====

def load_db():

    if not os.path.exists(DB_FILE):

        with open(DB_FILE, "w") as f:

            json.dump({}, f)

    with open(DB_FILE, "r") as f:

        return json.load(f)


def save_db(data):

    with open(DB_FILE, "w") as f:

        json.dump(data, f)


def add_client(user):

    data = load_db()

    data[str(user.id)] = user.first_name

    save_db(data)

# ===== START =====

@bot.message_handler(commands=['start'])
def start(message):

    add_client(message.from_user)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("🎨 Каталог кольорів")

    kb.add("📞 Зателефонувати менеджеру")

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

        reply_markup=kb

    )

    bot.send_message(

        message.chat.id,

        "📩 Зв'язок з менеджером:",

        reply_markup=inline

    )

# ===== КАТАЛОГ =====

@bot.message_handler(func=lambda m: m.text == "🎨 Каталог кольорів")
def catalog(message):

    try:

        file = open("catalog.pdf", "rb")

        bot.send_document(

            message.chat.id,

            file,

            caption="📘 Каталог кольорів Profi Protect"

        )

        file.close()

    except:

        bot.send_message(

            message.chat.id,

            "❌ Файл catalog.pdf не знайдено"

        )

# ===== PHONE =====

@bot.message_handler(func=lambda m: m.text == "📞 Зателефонувати менеджеру")
def phone(message):

    bot.send_message(

        message.chat.id,

        f"📞 Номер менеджера:\n{MANAGER_PHONE}"

    )

# ===== CRM =====

@bot.message_handler(commands=['crm'])
def crm(message):

    if message.chat.id != ADMIN_ID:

        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("📦 Статус замовлення")

    bot.send_message(

        message.chat.id,

        "CRM меню:",

        reply_markup=kb

    )

# ===== STATUS =====

temp = {}

@bot.message_handler(func=lambda m: m.text == "📦 Статус замовлення")
def status(message):

    msg = bot.send_message(message.chat.id, "Введіть ID клієнта:")

    bot.register_next_step_handler(msg, status_choose)


def status_choose(message):

    temp[message.chat.id] = message.text

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("📦 Готово")

    kb.add("⚙️ Формується")

    kb.add("🚚 Відправлено")

    msg = bot.send_message(

        message.chat.id,

        "Оберіть статус:",

        reply_markup=kb

    )

    bot.register_next_step_handler(msg, status_send)


def status_send(message):

    client = temp[message.chat.id]

    status = message.text

    if status == "🚚 Відправлено":

        msg = bot.send_message(message.chat.id, "Введіть ТТН:")

        bot.register_next_step_handler(msg, send_ttn, client)

    else:

        bot.send_message(

            client,

            f"📦 Статус замовлення:\n{status}"

        )

        bot.send_message(message.chat.id, "✅ Надіслано")


def send_ttn(message, client):

    bot.send_message(

        client,

        f"📦 Статус замовлення:\n🚚 Відправлено\n\n🚚 ТТН:\n{message.text}"

    )

    bot.send_message(

        message.chat.id,

        "✅ Статус і ТТН надіслано"

    )

# ===== RUN =====

print("BOT STARTED")

bot.infinity_polling()
