# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from config import TOKEN

import youtube_dl
import os

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot in place!')

@bot.event
async def on_message():
    print('New message!')

bot.run(TOKEN)