import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3

# ========= НАЛАШТУВАННЯ =========

TOKEN = "8397279335:AAHVEyh5sSGDOUcrSukgv3rFZIBp8ywaJdA"
ADMIN_ID = 6391072366  # твій Telegram ID

MANAGER_USERNAME = "profi_protect_official"
MANAGER_PHONE = "+0666508711"

CATALOG_FILE = "catalog.pdf"

# ================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ========= БАЗА =========

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER
)
""")
conn.commit()


def add_user(user_id):

    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:

        cursor.execute("INSERT INTO users VALUES(?)", (user_id,))
        conn.commit()


def get_users():

    cursor.execute("SELECT user_id FROM users")
    return cursor.fetchall()


# ========= МЕНЮ =========

menu = ReplyKeyboardMarkup(resize_keyboard=True)

menu.add("🎨 Кольори")
menu.add("👨‍💼 Написати менеджеру")
menu.add("📞 Подзвонити менеджеру")


# ========= СТАРТ =========

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    add_user(message.from_user.id)

    text = (
        "👋 Вітаємо!\n\n"
        "Я бот компанії *Profi Protect*.\n\n"
        "Я допоможу вам отримати інформацію щодо вашого замовлення, "
        "ТТН, статусу, а також надати каталог кольорів.\n\n"
        "Оберіть потрібний пункт меню 👇"
    )

    await message.answer(text, parse_mode="Markdown", reply_markup=menu)


# ========= КАТАЛОГ =========

@dp.message_handler(lambda message: message.text == "🎨 Кольори")
async def catalog(message: types.Message):

    await bot.send_document(
        message.chat.id,
        open(CATALOG_FILE, "rb"),
        caption="🎨 Каталог кольорів Profi Protect"
    )


# ========= МЕНЕДЖЕР =========

@dp.message_handler(lambda message: message.text == "👨‍💼 Написати менеджеру")
async def manager(message: types.Message):

    await message.answer(
        f"Напишіть менеджеру:\nhttps://t.me/{MANAGER_USERNAME}"
    )


@dp.message_handler(lambda message: message.text == "📞 Подзвонити менеджеру")
async def phone(message: types.Message):

    await message.answer(
        f"Телефон менеджера:\n{MANAGER_PHONE}"
    )


# ====================================
# ========= АДМІН КОМАНДИ ===========
# ====================================


# ===== РОЗСИЛКА =====

@dp.message_handler(commands=['broadcast'])
async def broadcast(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.get_args()

    users = get_users()

    for user in users:

        try:

            await bot.send_message(user[0], text)

        except:
            pass

    await message.answer("✅ Розсилка виконана")


# ===== ТТН =====

@dp.message_handler(commands=['ttn'])
async def ttn(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    args = message.get_args().split()

    user_id = args[0]
    number = args[1]

    text = (
        f"📦 Ваше замовлення відправлено!\n\n"
        f"🚚 ТТН: {number}"
    )

    await bot.send_message(user_id, text)

    await message.answer("✅ ТТН відправлено")


# ===== СТАТУС =====

@dp.message_handler(commands=['status'])
async def status(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    args = message.get_args().split()

    user_id = args[0]

    text = "✅ Ваше замовлення готове"

    await bot.send_message(user_id, text)

    await message.answer("✅ Статус відправлено")


# ===== ЧЕК =====

@dp.message_handler(commands=['check'])
async def check(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    args = message.get_args().split()

    user_id = args[0]

    await bot.send_document(
        user_id,
        message.document.file_id,
        caption="🧾 Ваш чек"
    )


# ========= ЗАПУСК =========

if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)
