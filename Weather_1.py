import logging

from pyexpat.errors import messages
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, ConversationHandler
import requests
from credits import bot_token  # Убедитесь, что у вас есть файл credits.py с токеном бота

# Определяем состояния для ConversationHandler
CURRENCY_EXCHANGE, EXCHANGE_RATE = range(2)

# Настройка логирования
logging.basicConfig(format=">>> %(message)s", level=logging.INFO)

# URL для получения курсов валют
url = "https://api.fxratesapi.com/latest?api_key=fxr_live_59db6ad572877dbf9ee8ca4a4c4a846d1ee6&base=USD"


async def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("CURRENCY EXCHANGE")],
        [KeyboardButton("EXCHANGE RATE OF WORLD CURRENCIES")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Привет! Это бот для просмотра курса и обмена мировых валют.",
        reply_markup=reply_markup
    )
    return ConversationHandler.END


async def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    logging.info(f"Received text: {text}")

    if text == "CURRENCY EXCHANGE":
        await update.message.reply_text("Пожалуйста, введите сумму для обмена (рубли к USD):")
        return CURRENCY_EXCHANGE
    elif text == "EXCHANGE RATE OF WORLD CURRENCIES":
        await rate_currency(update, context)
        return ConversationHandler.END

async def get_course():
    currency = "RUB"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("success"):
            rate = data["rates"].get(currency)
            if rate:
                return round(rate, 2)
    except Exception as e:
        return 0



async def rate_currency(update: Update, context: CallbackContext):
    course = await get_course()
    if course == 0:
        await update.message.reply_text("Ошибка")
    else:
        await update.message.reply_text(f"Курс рубля к USD: {course}")
    return ConversationHandler.END

async def handle_currency_exchange(update: Update, context: CallbackContext):
    # Здесь можно добавить логику для обработки обмена валют
    text = update.message.text
    logging.info(f"Amount: {text}")
    course = await get_course()
    await update.message.reply_text(round(int(text)/course, 2))


    #await update.message.reply_text(f"Вы ввели сумму для обмена: {amount}. (Здесь должна быть логика обмена.)")
    return ConversationHandler.END  # Завершение разговора


# Настройка ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
    states={
        CURRENCY_EXCHANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_currency_exchange)],
        EXCHANGE_RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, rate_currency)],
    },
    fallbacks=[],
)

# Создание приложения и добавление обработчиков
application = Application.builder().token(bot_token).build()
application.add_handler(conv_handler)

application.add_handler(CommandHandler("start", start))

# Запуск бота
if __name__ == "__main__":
    application.run_polling(allowed_updates=Update.ALL_TYPES)


