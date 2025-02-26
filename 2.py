from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, CallbackQueryHandler, ConversationHandler
from credits import bot_token
# Определяем состояния для разговора
CREATE_NOTE, VIEW_NOTES = range(2)

application = Application.builder().token(bot_token).build()

async def start(update: Update, context: CallbackContext):
    user = update.effective_user

    keyboard = [
        [KeyboardButton("СОЗДАТЬ ЗАМЕТКУ")],
        [KeyboardButton("ПОСМОТРЕТЬ ЗАМЕТКИ")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(f"Привет, {user.first_name}! Это бот для заметок.", reply_markup=reply_markup)

async def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "СОЗДАТЬ ЗАМЕТКУ":
        await update.message.reply_text("Пожалуйста, введите текст вашей заметки:")
        return CREATE_NOTE
    elif text == "ПОСМОТРЕТЬ ЗАМЕТКИ":
        notes = get_data_from_file(update.effective_user.username)
        await update.message.reply_text(notes)

async def create_note(update: Update, context: CallbackContext):
    user = update.effective_user.username
    note_text = update.message.text

    save_notes(user, [note_text])
    await update.message.reply_text("Заметка сохранена!")
    return ConversationHandler.END


# Функция для сохранения расписания в файл
def save_notes(user_name, notes):
    with open(f'{user_name.lower()}.txt', 'w', encoding='utf-8') as file:
        for note in notes:
            file.write(f'{note}\n')

# Функция для получения данных из файла
def get_data_from_file(user_name):
    try:
        with open(f'{user_name.lower()}.txt', 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        return "Заметки отсутствуют."

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
    states ={
        CREATE_NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_note)],
    },
    fallbacks=[],
)

application.add_handler(CommandHandler("start", start))
application.add_handler(conv_handler)

# Запускаем бота, ожидаем завершения по нажатию Ctrl-C
application.run_polling(allowed_updates=Update.ALL_TYPES)