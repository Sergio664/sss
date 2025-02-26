import os  # Импорт модуля os для работы с файловой системой

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters

from credits import bot_token  # Импорт токена бота из файла credits.py

# Определение состояний разговора
FIO, GENDER, PHOTO, BIO = range(4)

# Обработчик команды /start
async def start(update: Update, context):
    """Начало разговора и запрос ФИО пользователя."""
    await update.message.reply_text(
        "ФИО?",
        reply_markup=ReplyKeyboardRemove(),  # Убираем клавиатуру
    )
    return FIO  # Переход к следующему шагу - вводу ФИО

# Обработчик ввода ФИО
async def fio(update: Update, context):
    """Сохраняет ФИО и запрашивает фотографию."""
    context.user_data['fio'] = update.message.text  # Сохраняем ФИО в контекст пользователя
    await update.message.reply_text(
        "Отлично! Пожалуйста, напишите свой пол",
        reply_markup=ReplyKeyboardRemove(),  # Убираем клавиатуру
    )
    return GENDER # Переход к следующему шагу - запросу фотографии


async def gender(update: Update, context):
    context.user_data['gender'] = update.message.text
    await update.message.reply_text(
        "Хорошо! Пожалуйста, пришлите фотографию себя.")
    return PHOTO # Переход к следующему шагу - запросу фотографии



# Обработчик получения фотографии
async def photo(update: Update, context):
    """Сохраняет фотографию и запрашивает биографию."""
    photo_file = await update.message.photo[-1].get_file()  # Получаем файл фотографии
    await photo_file.download_to_drive(f"data/{context.user_data['fio']}.jpg")  # Сохраняем фотографию



# Обработчик получения фотографии
async def video(update: Update, context):
    video_file = await update.message.video[-1].get_file()  # Получаем файл фотографии
    await video_file.download_to_drive(f"data/{context.user_data['fio']}.jpg")  # Сохраняем фотографию

    await update.message.reply_text(
        "Отлично! Теперь напишите вашу биографию.",
        reply_markup=ReplyKeyboardRemove(),  # Убираем клавиатуру
    )
    return BIO  # Переход к следующему шагу - запросу биографии


# Функция для сохранения данных о сотруднике в файл
async def save_data_to_file(user_data, photo_file):
    """Сохраняет данные о сотруднике в текстовый файл."""
    # Создаем папку 'data', если ее еще нет
    if not os.path.exists('data'):
        os.makedirs('data')

    with open(f"data/{user_data['fio']}.txt", "w", encoding="utf-8") as file:
        file.write(f"ФИО: {user_data['fio']}\n")
        file.write(f"Пол: {user_data['gender']}\n")
        file.write(f"Биография: {user_data['bio']}\n")


# Обработчик ввода биографии
async def bio(update: Update, context):
    """Сохраняет биографию и завершает разговор."""
    context.user_data['bio'] = update.message.text  # Сохраняем биографию в контекст пользователя

    # Сохраняем данные в текстовый файл и фотографию в папку
    await save_data_to_file(context.user_data, await context.bot.get_file(context.user_data['photo_file_id']))

    await update.message.reply_text("Спасибо! Ваша информация сохранена.")  # Сообщаем пользователю об успешном добавлении
    return ConversationHandler.END  # Завершаем разговор

# Обработчик команды отмены
async def cancel(update: Update, context):
    """Отменяет и завершает разговор."""
    await update.message.reply_text(
        "Отменено.", reply_markup=ReplyKeyboardRemove()  # Сообщаем пользователю об отмене и убираем клавиатуру
    )
    return ConversationHandler.END  # Завершаем разговор

# Создание приложения и передача ему токена бота
application = Application.builder().token(bot_token).build()


# Создаем ConversationHandler для управления состояниями разговора с пользователем.
# entry_points определяет точки входа, которые начинают разговор.
# В данном случае, разговор начинается с команды "/start", вызывающей функцию start.
# После выполнения команды "/start" пользователю предлагается ввести ФИО.
# Состояние разговора переходит к FIO.
# Если пользователь отправит текстовое сообщение, обработчик fio сработает и сохранит ФИО пользователя.
# После ввода ФИО, пользователю предлагается отправить фотографию.
# Состояние разговора переходит к PHOTO.
# Если пользователь отправит фотографию, обработчик photo сработает и сохранит ее.
# После этого пользователю предлагается отправить биографию.
# Состояние разговора переходит к BIO.
# Если пользователь отправит текстовое сообщение, обработчик bio сработает и сохранит биографию.
# По завершении разговора вызывается функция save_data_to_file для сохранения данных в файл.
# В случае отмены разговора команда "/cancel" вызывает функцию cancel.

# Добавляем обработчик разговора с состояниями FIO, PHOTO и BIO
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, fio)],
        GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
        PHOTO: [MessageHandler(filters.PHOTO & ~filters.COMMAND, photo)],
        BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

print("Hello"
      "а")

application.add_handler(conv_handler)  # Добавляем обработчик разговора в приложение

application.run_polling(allowed_updates=Update.ALL_TYPES)  # Запускаем бота до нажатия пользователем Ctrl-C