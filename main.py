import discord
from discord.ext import commands
from config import TOKEN
from asyncio import sleep
import youtube_dl
import os

bot = commands.Bot(command_prefix='#')


@bot.event
async def on_ready():
    print('Bot in place!')


server, server_id, name_channel = None, None, None

domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://www.youtu.be/', 'http://www.youtu.be/']


async def check_domains(link):
    for x in domains:
        if link.startwith(x):
            return True
        return False


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@bot.command()
async def play(ctx, arg):
    global vc

    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
                
        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()


bot.run(TOKEN)
