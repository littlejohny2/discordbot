import sys
import os
import time
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
    @commands.cooldown(3, 1, commands.BucketType.member)
    async def message(self, ctx):

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


        await ctx.send('message!')


async def setup(bot: commands.Bot):
    await bot.add_cog(Message(bot))