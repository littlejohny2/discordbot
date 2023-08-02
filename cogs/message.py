import sys
import os
import time
from datetime import datetime
from dotenv import load_dotenv

import discord
from discord.ext import commands

sys.path.insert(1, 'C:\\Users\\Ty\\Documents\\coding\\python\\discordbot\\gpt')
import sample

from halo import Halo

class Message(commands.Cog, name='message command'):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name='message', usage='', description='ai message (ai is dumb)')
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def message(self, ctx):
        t0 = time.time()

        # creates new file
        newFile = os.path.join('gpt', 'context', 'context' + '.txt')
        fileOpen = open(newFile, 'w', encoding="utf-8")


        # reads message history, writes to file
        previousUserId = self.bot.user.id
        async for msg in ctx.channel.history(limit=25):
            if msg.content == '!d message':
                continue
            
            currentUserId = msg.author.id
            
            if currentUserId != previousUserId:
                if currentUserId == self.bot.user.id:
                    fileOpen.write('### CONTEXT')
                    fileOpen.write('\n')
                if previousUserId == self.bot.user.id:
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
            file.write('### CONTEXT')
            file.write('\n')
            file.writelines(reorderedData)


        # runs sampler
        sample.sample()


        # reads output
        outputPath = os.path.join('gpt', 'output', 'sample.txt')

        with open(outputPath, 'r', encoding='utf-8') as file:
            sampleLines = file.readlines()
        
        outputLines: list[str] = list()
        for line in sampleLines:

            if line == '### CONTEXT\n' or line.startswith('###'):
                break
            
            if not line.endswith('<|endoftext|>\n'):
                continue

            line = line.replace('<|endoftext|>', '') # temporary fix until i add other stuff
            outputLines.append(line)


        for line in outputLines:
            await ctx.send(line)

        t1 = time.time()
        dt = round(t1 - t0, 3)
        print(f'{ctx.author} ran !d message | time taken: {dt}s | date: {datetime.now()}')


async def setup(bot: commands.Bot):
    await bot.add_cog(Message(bot))