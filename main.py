import discord
from discord.ext import commands
from config import TOKEN

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


@bot.command()
async def play(ctx, *, command=None):
    global server, server_id, name_channel
    author = ctx.author
    if command == None:
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name=name_channel)
    params = command.split(' ')
    if len(params) == 1:
        sourse = params[0]
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name=name_channel)
        print('param 1')
    elif len(params) == 3:
        server_id = params[0]
        voice_id = params[1]
        sourse = params[2]
        try:
            server_id = int(server_id)
            voice_id = int(voice_id)
        except:
            await ctx.chanell.sen(f'{author.mention}, id the server or voice must be an integer!')
            return
        print('param 3')
        server = bot.get_guild(server_id)
        voice_channel = discord.utils.get(server.voice_channels, id=voice_id)
    else:
        await ctx.channel.send(f'{author.mention}, command is not correct')
        return

    voice = discord.utils.get(bot.voice_clients, guild=server)
    if voice is None:
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=server)

    if sourse == None:
        pass
    elif sourse.startswith('http'):
        if not check_domains(sourse):
            await ctx.channel.send(f'{author.mention}, link is not allowed')
            return
        song_there = os.path.isfile('music/song.mp3')
        try:
            if song_there:
                os.remove('music/song.mp3')
        except PermissionError:
            await ctx.channel.send('Not enough rights to delete file!')
            return

        ydl_opts = {
            'outtmpl': 'music/%(title)s.mp3',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
        }]
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sourse])
        for file in os.listdir('music/'):
            if file.endswith('.mp3'):
                os.rename(file, 'music/song.mp3')
            voice.play(discord.FFmpegPCMAudio('music/song.mp3'))
        else:
            voice.play(discord.FFmpegPCMAudio(f'music/{sourse}'))


bot.run(TOKEN)
