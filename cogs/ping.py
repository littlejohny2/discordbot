import csv
import os
import discord
from discord.ext import commands
import time
from datetime import datetime


class PingCog(commands.Cog, name="ping command"):
    def __init__(self, bot:commands.bot):
        self.bot = bot
        
    @commands.command(name = "ping",
                    usage="",
                    description = "displays the bot's ping.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ping(self, ctx):
        print(f'{ctx.author} ran !d ping | date: {datetime.now()}')

        before = time.monotonic()
        message = await ctx.send("🏓 Pong !")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 Pong !  `{int(ping)} ms`")


        # logging
        fieldNames = ['user', 'command', 'date', 'misc info']
        logFile = os.path.join('out', 'log.csv')
        with open(logFile, 'a', newline='') as file:
            logWriter = csv.DictWriter(file, fieldNames)

            newLog = { 'user': f'{ctx.author}', 'command': 'ping',
                       'date': f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}', 
                       'misc info': '' }
            
            logWriter.writerow(newLog)


async def setup(bot:commands.Bot):
    await bot.add_cog(PingCog(bot))