import csv
import os
import time
from datetime import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

from halo import Halo

load_dotenv()
me = int(os.getenv('OWNER_ID'))

class DataScrapeCog(commands.Cog, name='datascrape command'):
    def __init__(self, bot:commands.bot):
        self.bot = bot
    
    def userCheck(ctx):
        return ctx.message.author.id == me

    @commands.command(name='datascrape', usage='(filename)', description='gathers message history')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(userCheck)
    async def datascrape(self, ctx, fileName):
        print(f'{ctx.author} ran !d datascrape | date: {datetime.today()}')

        datascrapeLoading = Halo(text='Data collecting: ', spinner='line', color='white', placement='right')
        datascrapeLoading.start()
        
        t0 = time.time()


        # creates new file
        newFile = os.path.join('out', fileName + '.txt')
        fileOpen = open(newFile, 'w', encoding="utf-8")


        # iterates through message history most recent to oldest
        previousUserId = ctx.author.id
        async for msg in ctx.channel.history(limit=10000000000000000000000):
            currentUserId = msg.author.id
            
            if currentUserId != previousUserId:
                if currentUserId == ctx.author.id:
                    fileOpen.write('### CONTEXT')
                    fileOpen.write('\n')
                if previousUserId == ctx.author.id:
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


        # output to client
        t1 = time.time()
        dt = round(t1 - t0, 3)

        datascrapeLoading.stop()
        print(f'data collecting: success | time: {dt}s | saved to: {newFile}')

        await ctx.reply(f'data collecting: success | time: {dt}s | saved to: {newFile}')


        # logging
        fieldNames = ['user', 'command', 'date', 'misc info']
        logFile = os.path.join('out', 'log.csv')
        with open(logFile, 'a', newline='') as file:
            logWriter = csv.DictWriter(file, fieldNames)

            newLog = { 'user': f'{ctx.author}', 'command': 'datascrape',
                       'date': f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}', 
                       'misc info': '' }
            
            logWriter.writerow(newLog)


async def setup(bot: commands.Bot):
    await bot.add_cog(DataScrapeCog(bot))