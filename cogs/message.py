import os
import time
from dotenv import load_dotenv

import discord
from discord.ext import commands

from halo import Halo

class Message(commands.Cog, name='message command'):
    def __init__(self, bot:commands.bot):
        self.bot = bot

    @commands.command(name='message', usage='', description='ai message (ai is dumb)')
    @commands.cooldown(3, 1, commands.BucketType.member)
    async def message(self, ctx):
        await ctx.send('message!')


async def setup(bot: commands.Bot):
    await bot.add_cog(Message(bot))