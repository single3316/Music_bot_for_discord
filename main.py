import discord
from discord.ext import commands
from config import *
import youtube_dl
import os
from fuction.sql import Sql
import sqlite3
from fuction.webhook import send_webhook
from fuction.card import create_personal_card, create_rating_card
from fuction.diablo import *

bot = commands.Bot(command_prefix='#')


def get_connection():
    con = sqlite3.connect('db.sqlite')
    return con


@bot.event
async def on_ready():
    print('Bot is working!')


server, server_id, name_channel = None, None, None

domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://www.youtu.be/', 'http://www.youtu.be/']


async def check_domains(link):
    for x in domains:
        if link.startwith(x):
            return True
        return False


@bot.command()
async def play(ctx, *, command=None):
    global server, server_id, name_channel
    author = ctx.author
    if command is None:
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name=name_channel)
    params = command.split(' ')
    if len(params) == 1:
        source = params[0]
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name=name_channel)
    elif len(params) == 3:
        server_id = params[0]
        voice_id = params[1]
        source = params[2]
        try:
            server_id = int(server_id)
            voice_id = int(voice_id)
        except Exception as e:
            await ctx.chanell.sen(f'{author.mention}, id the server or voice must be an integer!')
            print(e)
            return
        server = bot.get_guild(server_id)
        voice_channel = discord.utils.get(server.voice_channels, id=voice_id)
    else:
        await ctx.channel.send(f'{author.mention}, command is not correct')
        return

    voice = discord.utils.get(bot.voice_clients, guild=server)
    if voice is None:
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=server)

    if source is None:
        pass
    elif source.startswith('http'):
        if not check_domains(source):
            await ctx.channel.send(f'{author.mention}, link is not allowed')
            return
        song_there = os.path.isfile('music/song.mp3')
        try:
            if song_there and voice is None:
                os.remove('music/song.mp3')
            elif not (voice is None) and False:
                await ctx.channel.send(f'{author.mention}, wait then bot stop.')
        except PermissionError:
            await ctx.channel.send('Not enough rights to delete file!')
            return

        ydl_opts = {
            'outtmpl': "music/song.mp3",
            'format': 'bestaudio/best',
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192', }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([source])
            voice.play(discord.FFmpegPCMAudio(executable='ffmpeg.exe', source='music/song.mp3'))
            await ctx.channel.send(f'')


@bot.event
async def on_message(message):
    if message.author.id != '839621007614672896':
        if message.content[0] != '#':
            user_sql = Sql(author_id=message.author.id, conn=get_connection(), name=message.author.name)
            user_sql.add_point(len(message.content.split()))
        if message.author == '576307747566387223':
            await message.channel.send('Сева даун')
        await bot.process_commands(message)


@bot.command()
async def level(ctx, member: discord.Member = None):
    if member is not None:
        user = Sql(member.id, get_connection(), member.name)
        name = member.name
    else:
        user = Sql(ctx.author.id, get_connection(), ctx.author.name)
        member = ctx.author
        name = ctx.author.name
    rank = user.get_rank()
    score = user.get_score()
    image_av = member.avatar_url_as(format='png', size=256)
    create_personal_card(image_av, rank, score, user.get_level(), name)
    await ctx.channel.send(file=discord.File('images/w.png'))


@bot.command()
async def rating(ctx):
    user = Sql(ctx.author.id, get_connection(), ctx.author.name)
    rank = user.get_rank()
    user_list = user.get_ten_users()
    user_list.append([user.author_name, ctx.author.id, user.get_rank()])
    h = 0
    for i in user_list:
        user_list[h][1] = await bot.fetch_user(i[1])
        user_list[h][1] = user_list[h][1].avatar_url_as(format='png', size=64)
        h += 1
    create_rating_card(user_list)
    await ctx.channel.send(file=discord.File('images/w.png'))


@bot.event
async def on_member_join(member):
    send_webhook(f'Добро пожаловать {member.mention}',
                 'Рады вас приветствовать на нашем сервере для игр и IT индустрии',
                 WEBHOOK_URL)


@bot.command()
async def diablo(ctx):
    message = ctx.message.content[8:].split()
    category = message[0]
    item = str(message[1])
    data = parsing_item(item, get_category_name(category))
    webhook: discord.Webhook = await ctx.channel.create_webhook(name='Diablo')
    await webhook.send(avatar_url='https://www.rpgnuke.ru/wp-content/uploads/2019/10/476283675867580477693459876583645-e1572520886177.jpg',
                       embed=data)
    webhook.delete()


bot.run(TOKEN)
