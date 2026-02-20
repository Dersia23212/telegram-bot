import telebot
from telebot import types
import json
import os

# ========= НАЛАШТУВАННЯ =========

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

            "💬 Написати менеджеру в Telegram",

            url=f"https://t.me/{MANAGER_USERNAME}"

        )

    )

    bot.send_message(

        message.chat.id,

        "Вас вітає бот Profi Protect! 👋\n\n"

        "Я буду інформувати вас про статус вашого замовлення 📦",

        reply_markup=reply

    )

    bot.send_message(

        message.chat.id,

        "📩 Зв'язок з менеджером:",

        reply_markup=inline

    )


# ========= КАТАЛОГ =========

@bot.message_handler(func=lambda m: m.text == "🎨 Каталог кольорів")
def catalog(message):

    if os.path.exists(CATALOG_FILE):

        file = open(CATALOG_FILE, "rb")

        bot.send_document(

            message.chat.id,

            file,

            caption="📘 Каталог кольорів Profi Protect"

        )

    else:

        bot.send_message(message.chat.id, "❌ Файл catalog.pdf не знайдено")


# ========= ТЕЛЕФОН =========

@bot.message_handler(func=lambda m: m.text == "📞 Зателефонувати менеджеру")
def phone(message):

    bot.send_message(

        message.chat.id,

        f"📞 Номер менеджера:\n{MANAGER_PHONE}"

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

    markup.add("📦 Статус")

    bot.send_message(

        message.chat.id,

        "CRM меню:",

        reply_markup=markup

    )


# ========= КЛІЄНТИ =========

@bot.message_handler(func=lambda m: m.text == "👥 Клієнти")
def clients(message):

    db = load_db()

    text = ""

    for i in db:

        text += f"{db[i]} — {i}\n"

    bot.send_message(message.chat.id, text)


# ========= РОЗСИЛКА =========

@bot.message_handler(func=lambda m: m.text == "📢 Розсилка")
def send_all(message):

    msg = bot.send_message(message.chat.id, "Введіть текст розсилки:")

    bot.register_next_step_handler(msg, send_all_finish)


def send_all_finish(message):

    db = load_db()

    sent = 0

    for i in db:

        try:

            bot.send_message(i, message.text)

            sent += 1

        except:

            pass

    bot.send_message(message.chat.id, f"✅ Надіслано: {sent}")


# ========= PDF =========

pdf_wait = {}

@bot.message_handler(func=lambda m: m.text == "🧾 Надіслати PDF")
def pdf_start(message):

    msg = bot.send_message(message.chat.id, "Введіть ID клієнта:")

    bot.register_next_step_handler(msg, pdf_client)


def pdf_client(message):

    pdf_wait[message.chat.id] = message.text

    bot.send_message(message.chat.id, "Надішліть PDF файл")


@bot.message_handler(content_types=['document'])
def pdf_send(message):

    if message.chat.id in pdf_wait:

        client = pdf_wait[message.chat.id]

        bot.send_document(client, message.document.file_id)

        bot.send_message(message.chat.id, "✅ PDF надіслано")

        del pdf_wait[message.chat.id]


# ========= ТТН =========

ttn_wait = {}

@bot.message_handler(func=lambda m: m.text == "🚚 Надіслати ТТН")
def ttn_start(message):

    msg = bot.send_message(message.chat.id, "Введіть ID клієнта:")

    bot.register_next_step_handler(msg, ttn_number)


def ttn_number(message):

    ttn_wait[message.chat.id] = message.text

    msg = bot.send_message(message.chat.id, "Введіть номер ТТН:")

    bot.register_next_step_handler(msg, ttn_send)


def ttn_send(message):

    client = ttn_wait[message.chat.id]

    bot.send_message(

        client,

        f"🚚 Ваше замовлення відправлено\n\nТТН:\n{message.text}"

    )

    bot.send_message(message.chat.id, "✅ ТТН надіслано")

    del ttn_wait[message.chat.id]


# ========= СТАТУС =========

status_wait = {}

@bot.message_handler(func=lambda m: m.text == "📦 Статус")
def status_start(message):

    msg = bot.send_message(message.chat.id, "Введіть ID клієнта:")

    bot.register_next_step_handler(msg, status_choose)


def status_choose(message):

    status_wait[message.chat.id] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("📦 Готово")

    markup.add("🚚 Відправлено")

    markup.add("✅ Доставлено")

    msg = bot.send_message(

        message.chat.id,

        "Оберіть статус:",

        reply_markup=markup

    )

    bot.register_next_step_handler(msg, status_send)


def status_send(message):

    client = status_wait[message.chat.id]

    bot.send_message(client, f"📦 Статус замовлення:\n{message.text}")

    bot.send_message(message.chat.id, "✅ Статус надіслано")

    del status_wait[message.chat.id]


# ========= RUN =========

print("BOT STARTED")

bot.infinity_polling()
