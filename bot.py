import os
import time
from dotenv import load_dotenv

import pandas as pd

import discord
from discord.ext import commands

from halo import Halo

##
load_dotenv()
me = 267369024969637890

fileName = 'hell'
outDir = 'out'
##

async def data(message):
    datascrapeLoading = Halo(text='Data collecting: ', spinner='line', color='white', placement='right')
    datascrapeLoading.start()

    # creates new file
    newFile = os.path.join(outDir, fileName + '.txt')
    fileOpen = open(newFile, 'w', encoding="utf-8")

    t0 = time.time()

    # iterates through message history most recent to oldest
    previousUserId = message.author.id
    async for msg in message.channel.history(limit=10000000000000000000000):
        currentUserId = msg.author.id
        
        if currentUserId != previousUserId:
            if currentUserId == me:
                fileOpen.write('### CONTEXT')
                fileOpen.write('\n')
            if previousUserId == me:
                fileOpen.write('### RESPONSE')
                fileOpen.write('\n') 


        fileOpen.write(str(msg.content))
        fileOpen.write('<|endoftext|>')
        fileOpen.write('\n')

        previousUserId = msg.author.id
    fileOpen.close()

    # reorders to oldest -> recent 
    with open(newFile, 'r', encoding='utf-8') as file:
        data = file.readlines()
    reorderedData = data[::-1]

    with open(newFile, 'w', encoding='utf-8') as file:
        file.writelines(reorderedData)

    t1 = time.time()
    dt = t1 - t0

    datascrapeLoading.stop()
    print(f'Data collecting: success || time: {dt}s')

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

        if message.content == 'data':

            if message.author.id == me:
                await message.reply('ok')

                await data(message)

            else:
                await message.reply('no')


client = MyClient(intents=discord.Intents.all())
client.run(os.getenv('DISCORD_TOKEN'))