import asyncio
import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from halo import Halo



### VARIABLES ###
load_dotenv()

intents = discord.Intents.all()

me = int(os.getenv('OWNER_ID'))
commandPrefix = os.getenv('COMMAND_PREFIX')
botToken = os.getenv('DISCORD_TOKEN')
#################


bot = commands.Bot(command_prefix=commandPrefix, intents=intents)


@bot.event
async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')


async def main():
    for file in os.listdir('cogs'):
        if file.endswith('.py'):
            print(f'Loaded: cogs.{file[:-3]}')
            await bot.load_extension(f'cogs.{file[:-3]}')


asyncio.run(main())
bot.run(botToken)