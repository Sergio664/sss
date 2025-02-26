import os
from telegram import Update, ReplyKeyboardRemove

from PIL import Image, ImageFont, ImageDraw

from credits import bot_token

# Определение состояний разговора
PHOTO, TOP_STRING, BOT_STRING = range(3)

def set_meme_text(username, ts, bs, modifier=5):
    img = Image.open(os.path.join("data", username + '.jpg'))
    rgb_img = img.convert("RGB")
    title_font = ImageFont.truetype('arial.ttf', 60)
    width, height = rgb_img.size

    # Создаем объект ImageDraw
    draw = ImageDraw.Draw(rgb_img)

    # Получаем ограничивающий прямоугольник текста
    ts_bbox = draw.textbbox((0, 0), ts, font=title_font)
    bs_bbox = draw.textbbox((0, 0), bs, font=title_font)

    # Получаем размеры текста
    ts_width = ts_bbox[2] - ts_bbox[0]
    ts_height = ts_bbox[3] - ts_bbox[1]
    bs_width = bs_bbox[2] - bs_bbox[0]
    bs_height = bs_bbox[3] - bs_bbox[1]

    # Определяем отступы сверху и снизу с учетом модификатора
    top_offset = modifier
    bottom_offset = modifier

    # Расположение текста по центру изображения с равными отступами сверху и снизу
    ts_x = (width - ts_width) / 2
    ts_y = top_offset - ts_bbox[1]  # Верхний край текста
    bs_x = (width - bs_width) / 2
    bs_y = height - bottom_offset - bs_bbox[3]  # Нижний край текста

    # Нанесение текста
    draw.text((ts_x, ts_y), ts, (255, 0, 0), font=title_font)
    draw.text((bs_x, bs_y), bs, (255, 0, 0), font=title_font)

    # Сохранение изображения
    meme_path = os.path.join("data", username + "_meme.jpg")
    rgb_img.save(meme_path)

async def start(update: Update, context):
    await update.message.reply_text("Добро пожаловать в генератор мемов! Отправь картинку, чтобы начать с ним работать!")
    return PHOTO

async def photo(update: Update, context):
    user = str(update.message.from_user.username)
    photo_file = await update.message.photo[-1].get_file()
    if not os.path.exists('data'):
        os.makedirs('data')
    await photo_file.download_to_drive(f"data/{user}.jpg")
    await update.message.reply_text("Отлично! Теперь добавь верхнюю надпись или отправь /skip если хочешь пропустить этот шаг")
    return TOP_STRING

async def top_string(update: Update, context):
    await update.message.reply_text(
        'Смешно =) А теперь вводи нижнюю надпись или отправь /skip если хочешь пропустить этот шаг')
    context.user_data['top_string'] = update.message.text
    return BOT_STRING

async def skip_top_string(update: Update, context):
    await update.message.reply_text('Тогда пиши что должно быть внизу')
    return BOT_STRING

async def bottom_string(update: Update, context):
    user = str(update.message.from_user.username)

    top_string = context.user_data.get('top_string')

    bottom_string = update.message.text

    set_meme_text(user, top_string or "", bottom_string)

    sending_img = open(os.path.join("data", user + "_meme.jpg"), "rb")
    await context.bot.send_document(update.effective_chat.id, sending_img)

    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text("Отменено.")
    return ConversationHandler.END

application = Application.builder().token(bot_token).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        PHOTO: [MessageHandler(filters.PHOTO, photo)],
        TOP_STRING: [MessageHandler(filters.TEXT & ~filters.COMMAND, top_string),
                     CommandHandler('skip', skip_top_string)],
        BOT_STRING: [MessageHandler(filters.TEXT & ~filters.COMMAND, bottom_string)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
application.add_handler(conv_handler)

application.run_polling(allowed_updates=Update.ALL_TYPES)
