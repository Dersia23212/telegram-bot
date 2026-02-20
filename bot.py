import telebot
from telebot import types

TOKEN = "8397279335:AAHVEyh5sSGDOUcrSukgv3rFZIBp8ywaJdA"

bot = telebot.TeleBot(TOKEN)

# ВАЖЛИВО! Встав свій Telegram ID
ADMIN_ID = 6391072366

MANAGER_PHONE = "+6391072366"
REVIEW_LINK = "https://www.google.com/maps/place/Profi+Protect/@50.5091268,30.4629253,21z/data=!4m8!3m7!1s0x472b2b008d32e03b:0x9e906a87a1af6440!8m2!3d50.5090198!4d30.4629729!9m1!1b1!16s%2Fg%2F11vm5x966f?entry=ttu&g_ep=EgoyMDI2MDIxNy4wIKXMDSoASAFQAw%3D%3D"  # посилання на відгуки

# старт клієнта
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Вітаємо! 😊\nМи будемо інформувати вас про статус замовлення."
    )

# меню для менеджера
@bot.message_handler(commands=['crm'])
def crm_menu(message):

    if message.chat.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🧾 Надіслати чек")
    markup.add("📦 Замовлення готове")
    markup.add("🚚 Замовлення відправлено")
    markup.add("⭐ Запросити відгук")

    bot.send_message(message.chat.id, "CRM меню:", reply_markup=markup)

# обробка кнопок
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID)
def admin_buttons(message):

    if message.text == "🧾 Надіслати чек":

        msg = bot.send_message(ADMIN_ID, "Введіть ID клієнта:")
        bot.register_next_step_handler(msg, send_receipt)

    elif message.text == "📦 Замовлення готове":

        msg = bot.send_message(ADMIN_ID, "Введіть ID клієнта:")
        bot.register_next_step_handler(msg, send_ready)

    elif message.text == "🚚 Замовлення відправлено":

        msg = bot.send_message(ADMIN_ID, "Введіть ID клієнта:")
        bot.register_next_step_handler(msg, send_sent)

    elif message.text == "⭐ Запросити відгук":

        msg = bot.send_message(ADMIN_ID, "Введіть ID клієнта:")
        bot.register_next_step_handler(msg, send_review)


def send_receipt(message):

    bot.send_message(
        message.text,
        "🧾 Ваш чек готовий.\nДякуємо за покупку!"
    )


def send_ready(message):

    bot.send_message(
        message.text,
        "📦 Ваше замовлення готове до відправки."
    )


def send_sent(message):

    bot.send_message(
        message.text,
        f"🚚 Ваше замовлення відправлено!\n\n📞 Менеджер: {MANAGER_PHONE}"
    )


def send_review(message):

    bot.send_message(
        message.text,
        f"❤️ Дякуємо за покупку!\nБудемо вдячні за відгук:\n{REVIEW_LINK}"
    )


bot.infinity_polling()
