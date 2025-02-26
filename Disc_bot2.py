import discord
import credits
import os
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
token = credits.bot_token

# Словарь для хранения игр
game_dictionary = {}
# Список участников
member_list = []
# Словарь для хранения скриншотов
screen_dictionary = {}

@bot.command()
async def start(ctx):
    global member_list
    if ctx.author.name in member_list:
        await ctx.send("Ты уже со мной здоровался - я тебя знаю " + ctx.author.name)
    else:
        await ctx.send("Привет, " + ctx.author.name + "! Добро пожаловать ко мне!")
        member_list.append(ctx.author.name)

    dir_name = ctx.author.name
    if dir_name.isalnum():
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    global game_dictionary
    if ctx.author.name not in game_dictionary:
        game_dictionary[ctx.author.name] = []

    global screen_dictionary
    if ctx.author.name not in screen_dictionary:
        screen_dictionary[ctx.author.name] = []

@bot.command()
async def addgame(ctx, *, game_name: str):
    global game_dictionary
    if ctx.author.name not in game_dictionary:
        await ctx.send("Сначала запустите команду !start, чтобы зарегистрироваться.")
        return

    game_dictionary[ctx.author.name].append(game_name)
    await ctx.send(f'Игра "{game_name}" добавлена в ваш список!')

@bot.command()
async def showmygames(ctx):
    global game_dictionary
    if ctx.author.name not in game_dictionary:
        await ctx.send("Сначала запустите команду !start, чтобы зарегистрироваться.")
        return

    games = game_dictionary[ctx.author.name]
    if games:
        await ctx.send(f'Ваши игры: {", ".join(games)}')
    else:
        await ctx.send("У вас пока нет добавленных игр.")

@bot.command()
async def sendscreen(ctx):

    global screen_dictionary

    if ctx.author.name not in game_dictionary:
        await ctx.send("Сначала запустите команду !start, чтобы зарегистрироваться.")
        return

    # Проверяем, есть ли вложения в сообщении
    if not ctx.message.attachments:
        await ctx.send("Пожалуйста, прикрепите файл скриншота.")
        return

    # Проверяем, есть ли папка
    dir_name = ctx.author.name
    if not os.path.exists(dir_name):
        await ctx.send("Ошибка папки.")
        return

    for attach in ctx.message.attachments:
        # Сохраняем файл в папку пользователя
        await attach.save(f"{dir_name}/{attach.filename}")

        # Добавляем путь к файлу в словарь
        screen_list = screen_dictionary.get(dir_name)
        screen_list.append(f"{dir_name}/{attach.filename}")
        screen_dictionary[ctx.author.name] = screen_list

    await ctx.send("Скриншот успешно сохранен!")

@bot.command()
async def getlastscreen(ctx):
    global screen_dictionary
    if ctx.author.name not in screen_dictionary or not screen_dictionary[ctx.author.name]:
        await ctx.send("У вас нет сохраненных скриншотов.")
        return

    screen_list = screen_dictionary.get(ctx.author.name)
    last_screen_path = screen_list[-1]

    if os.path.exists(last_screen_path):
        await ctx.send(file=discord.File(last_screen_path))
    else:
        await ctx.send("Последний скриншот не найден.")


bot.run(token)


