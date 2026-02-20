import telebot
from telebot import types
import json
import os

# ========= НАСТРОЙКИ =========

TOKEN = "8397279335:AAHVEyh5sSGDOUcrSukgv3rFZIBp8ywaJdA"

ADMIN_ID = 6391072366

MANAGER_PHONE = "+380666508711"

MANAGER_USERNAME = "profi_protect_official"

CATALOG_FILE = "catalog.pdf"

bot = telebot.TeleBot(TOKEN)

DB_FILE = "clients.json"

# ========= БАЗА =========

def load_db():

    if not os.path.exists(DB_FILE):

        with open(DB_FILE, "w") as f:

            json.dump({}, f)

    return json.load(open(DB_FILE))


def save_db(data):

    json.dump(data, open(DB_FILE, "w"))


def add_client(user):

    data = load_db()

    data[str(user.id)] = user.first_name

    save_db(data)

# ========= ГОЛОВНЕ МЕНЮ =========

def main_menu():

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("🎨 Каталог кольорів")

    kb.add("📞 Зателефонувати менеджеру")

    kb.add("📦 Статус замовлення")

    return kb

# ========= CRM MENU =========

def crm_menu():

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("📦 Статус замовлення")

    kb.add("⬅️ Назад")

    return kb

# ========= START =========

@bot.message_handler(commands=['start'])
def start(message):

    add_client(message.from_user)

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

        reply_markup=main_menu()

    )

    bot.send_message(

        message.chat.id,

        "📩 Зв'язок з менеджером:",

        reply_markup=inline

    )

# ========= КАТАЛОГ =========

@bot.message_handler(func=lambda m: m.text == "🎨 Каталог кольорів")
def catalog(message):

    try:

        file = open(CATALOG_FILE, "rb")

        bot.send_document(

            message.chat.id,

            file,

            caption="📘 Каталог кольорів"

        )

        file.close()

    except:

        bot.send_message(

            message.chat.id,

            "❌ Файл не знайдено"

        )

# ========= PHONE =========

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

    bot.send_message(

        message.chat.id,

        "CRM меню:",

        reply_markup=crm_menu()

    )

# ========= BACK =========

@bot.message_handler(func=lambda m: m.text == "⬅️ Назад")
def back(message):

    bot.send_message(

        message.chat.id,

        "Головне меню:",

        reply_markup=main_menu()

    )

# ========= STATUS =========

temp = {}

@bot.message_handler(func=lambda m: m.text == "📦 Статус замовлення")
def status(message):

    msg = bot.send_message(

        message.chat.id,

        "Введіть ID клієнта:"

    )

    bot.register_next_step_handler(msg, status2)


def status2(message):

    temp[message.chat.id] = message.text

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("📦 Готово")

    kb.add("⚙️ Формується")

    kb.add("🚚 Відправлено")

    kb.add("⬅️ Назад")

    msg = bot.send_message(

        message.chat.id,

        "Оберіть статус:",

        reply_markup=kb

    )

    bot.register_next_step_handler(msg, status3)


def status3(message):

    client = temp[message.chat.id]

    if message.text == "🚚 Відправлено":

        msg = bot.send_message(

            message.chat.id,

            "Введіть ТТН:"

        )

        bot.register_next_step_handler(msg, send_ttn, client)

    elif message.text == "⬅️ Назад":

        back(message)

    else:

        bot.send_message(

            client,

            f"📦 Статус:\n{message.text}"

        )

        bot.send_message(

            message.chat.id,

            "✅ Надіслано",

            reply_markup=main_menu()

        )


def send_ttn(message, client):

    bot.send_message(

        client,

        f"📦 Відправлено\n🚚 ТТН: {message.text}"

    )

    bot.send_message(

        message.chat.id,

        "✅ Готово",

        reply_markup=main_menu()

    )

# ========= RUN =========

print("BOT STARTED")

bot.infinity_polling()
