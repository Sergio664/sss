import discord
from discord.ext import commands

# Импортируем токен бота из другого файла
import credits

# Получаем токен бота из переменной
token = credits.bot_token
# Определяем намерения бота
intents = discord.Intents.default()
# Включаем намерение "message_content" для получения содержимого сообщений
intents.message_content = True

# Создаем бота с указанным префиксом команд
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    # Проверяем, что сообщение не отправлено ботом
    if message.author == bot.user:
        return

    words = message.content.split()

    if "Волан-де-Морт" in words:
        await message.channel.send('Это имя не произносится вслух!')


# Запускаем бота с указанным токеном
bot.run(token)