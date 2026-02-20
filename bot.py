import telebot
from telebot import types
import json
import os

TOKEN = "8397279335:AAHVEyh5sSGDOUcrSukgv3rFZIBp8ywaJdA"
ADMIN_ID = 6391072366

bot = telebot.TeleBot(TOKEN)

DB_FILE = "clients.json"

# ---------------- БАЗА ----------------

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# ---------------- START ----------------

@bot.message_handler(commands=['start'])
def start(message):

    db = load_db()

    db[str(message.chat.id)] = {
        "name": message.from_user.first_name,
        "status": "Новий"
    }

    save_db(db)

    bot.send_message(
        message.chat.id,
        "Вітаємо! Ви додані в систему."
    )

# ---------------- CRM ----------------

@bot.message_handler(commands=['crm'])
def crm(message):

    if message.chat.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("👥 Клієнти")
    markup.add("🧾 Надіслати PDF")
    markup.add("🚚 Надіслати ТТН")
    markup.add("📦 Змінити статус")

    bot.send_message(
        message.chat.id,
        "CRM меню:",
        reply_markup=markup
    )

# ---------------- СПИСОК ----------------

@bot.message_handler(func=lambda m: m.text == "👥 Клієнти")
def clients(message):

    db = load_db()

    text = ""

    for i in db:
        text += f"{db[i]['name']} — {i}\n"

    bot.send_message(message.chat.id, text)

# ---------------- PDF ----------------

pdf_wait = {}

@bot.message_handler(func=lambda m: m.text == "🧾 Надіслати PDF")
def ask_pdf(message):

    msg = bot.send_message(message.chat.id, "Введіть ID клієнта:")

    bot.register_next_step_handler(msg, get_pdf_client)

def get_pdf_client(message):

    pdf_wait[message.chat.id] = message.text

    bot.send_message(
        message.chat.id,
        "Тепер надішліть PDF файл"
    )

@bot.message_handler(content_types=['document'])
def send_pdf(message):

    if message.chat.id not in pdf_wait:
        return

    client = pdf_wait[message.chat.id]

    file_id = message.document.file_id

    bot.send_document(client, file_id)

    bot.send_message(message.chat.id, "PDF надіслано")

# ---------------- ТТН ----------------

ttn_wait = {}

@bot.message_handler(func=lambda m: m.text == "🚚 Надіслати ТТН")
def ask_ttn(message):

    msg = bot.send_message(message.chat.id, "ID клієнта:")

    bot.register_next_step_handler(msg, get_ttn)

def get_ttn(message):

    ttn_wait[message.chat.id] = message.text

    msg = bot.send_message(message.chat.id, "Введіть номер ТТН:")

    bot.register_next_step_handler(msg, send_ttn)

def send_ttn(message):

    client = ttn_wait[message.chat.id]

    number = message.text

    bot.send_message(
        client,
        f"🚚 Ваш номер ТТН:\n{number}"
    )

    bot.send_message(message.chat.id, "ТТН надіслано")

# ---------------- СТАТУС ----------------

status_wait = {}

@bot.message_handler(func=lambda m: m.text == "📦 Змінити статус")
def ask_status(message):

    msg = bot.send_message(message.chat.id, "ID клієнта:")

    bot.register_next_step_handler(msg, choose_status)

def choose_status(message):

    client = message.text

    status_wait[message.chat.id] = client

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("📦 Готово")
    markup.add("🚚 Відправлено")
    markup.add("✅ Доставлено")

    msg = bot.send_message(
        message.chat.id,
        "Оберіть статус:",
        reply_markup=markup
    )

    bot.register_next_step_handler(msg, send_status)

def send_status(message):

    client = status_wait[message.chat.id]

    bot.send_message(
        client,
        f"📦 Статус замовлення:\n{message.text}"
    )

    bot.send_message(message.chat.id, "Статус надіслано")

# ---------------- RUN ----------------

print("BOT STARTED")

bot.infinity_polling()
