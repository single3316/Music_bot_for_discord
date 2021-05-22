import discord
from discord.ext import commands
from config import TOKEN
import ffmpeg
import youtube_dl
import os
from sql import Sql
import sqlite3

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
            elif not (voice is None):
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
            await ctx.channel.send(f'```Now playing song:```')


@bot.event
async def on_message(message):
    user_sql = Sql(author_id=message.author.id, conn=get_connection())
    await bot.process_commands(message)

bot.run(TOKEN)
