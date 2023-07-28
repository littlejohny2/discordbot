import os
from dotenv import load_dotenv

import pandas as pd

import discord
from discord.ext import commands

from halo import Halo

##
load_dotenv()
me = 267369024969637890

fileName = 'test'
outDir = 'out'
##


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content == 'goon':
            await message.reply('cave', mention_author=True)
            print(f'gooncave completion')

        if message.content == 'test':

            if message.author.id == me:
                await message.reply('ok')
                
                datascrapeLoading = Halo(text='Data collecting: ', spinner='line', color='white', placement='right')
                datascrapeLoading.start()

                newFile = os.path.join(outDir, fileName + '.txt')
                fileOpen = open(newFile, 'w', encoding="utf-8")
                async for msg in message.channel.history(limit=10000000000000000000000):
                    if msg.author.id == me:
                        fileOpen.write(str(msg.content))
                        # fileOpen.write('<|endoftext|>')
                        fileOpen.write('\n')

                datascrapeLoading.succeed()

            else:
                await message.reply('no')


client = MyClient(intents=discord.Intents.all())
client.run(os.getenv('DISCORD_TOKEN'))