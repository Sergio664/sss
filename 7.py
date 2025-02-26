from telegram import Update, KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, CallbackQueryHandler, ConversationHandler


from credits import bot_token


S1, S2, S3, G4 = range(4)

async def start(update: Update, context: CallbackContext):

    if update.message == "":
        context.user_data['points'] = 1

    keyboard = [
        [KeyboardButton("Дарт Пол")],
        [KeyboardButton("Дарт Мол")],
        [KeyboardButton("Дарт Гард")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Привет! Это бот для проверки твоих знаний о фильме Звездные Войны, ответь на первый вопрос. Как зовут лорда ситхов с остроконечной головой, держащего световой меч с двумя лезвиями?", reply_markup=reply_markup)
    return S1



async def s1(update: Update, context: CallbackContext):

    if update.message == "Дарт Мол":
        context.user_data['points'] += 1

    keyboard = [
        [KeyboardButton("Раб-1")],
        [KeyboardButton("Призрак")],
        [KeyboardButton("Сокол Тысячелетия")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Как назывался корабль Хана Соло?",
        reply_markup=reply_markup)
    return S2


async def s2(update: Update, context: CallbackContext):

    if update.message == "Сокол Тысячелетия":
        context.user_data['points'] += 1

    keyboard = [
        [KeyboardButton("Падме Амидала")],
        [KeyboardButton("Лея")],
        [KeyboardButton("Асока Тано")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Кто был королевой планеты Набу?",
        reply_markup=reply_markup)
    return S3


async def s3(update: Update, context: CallbackContext):

    if update.message == "Падме Амидала":
        context.user_data['points'] += 1

    keyboard = [
        [KeyboardButton("Погиб")],
        [KeyboardButton("Потерял правую руку")],
        [KeyboardButton("Потерял левую ногу")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Что случилось с Энакином Скайуокером во время битвы с графом Дуку?",
        reply_markup=reply_markup)
    return G4





async def g4(update: Update, context: CallbackContext, keyboard=None):

    if update.message == "Потерял правую руку":
        context.user_data['points'] += 1

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    points = context.user_data['points']
    await update.message.reply_text(f"У вас {points}! Вы прошли наш квиз, поздровляем!", reply_markup=reply_markup)






async def cancel(update: Update, context: CallbackContext):
    return ConversationHandler.END


application = Application.builder().token(bot_token).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        S1: [MessageHandler(filters.TEXT & ~filters.COMMAND, s1)],
        S2: [MessageHandler(filters.TEXT & ~filters.COMMAND, s2)],
        S3: [MessageHandler(filters.TEXT & ~filters.COMMAND, s3)],
        G4: [MessageHandler(filters.TEXT & ~filters.COMMAND, g4)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)


application.add_handler(conv_handler)


application.run_polling(allowed_updates=Update.ALL_TYPES)