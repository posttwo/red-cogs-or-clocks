import discord
from redbot.core import Config, commands, checks, bot
from typing import Optional
import datetime
import re
import requests

BaseCog = getattr(commands, "Cog", object)

class Mention(BaseCog):
    """Le away cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mention(self, ctx, fjusername):
        """FunnyJunk username to Discord mention!"""
        auth_token = await self.bot.db.api_tokens.get_raw("fjmeme", default={"token": None})
        hed = {'Authorization': 'Bearer ' + auth_token['token']}

        url = 'https://fjme.me/api/fjmeme/funnyJunkToDiscord/' + fjusername
        response = requests.get(url, headers=hed)
        data = response.json()
        disc_id = data['user']['discord_id']
        # Your code will go here
        await ctx.send('Yo %s, %s <=> <@%s>' % (ctx.message.author.mention, fjusername, disc_id))

    @commands.command()
    async def reverse(self, ctx, fjusername):
        """Discord mention to FunnyJunk username"""
        auth_token = await self.bot.db.api_tokens.get_raw("fjmeme", default={"token": None})
        hed = {'Authorization': 'Bearer ' + auth_token['token']}

        for mention in ctx.message.mentions:
            disc_id = mention.id
            url = 'https://fjme.me/api/fjmeme/discordToFunnyJunk/' + str(disc_id)
            response = requests.get(url, headers=hed)
            data = response.json()
            username = data['fjuser']['username']
            await ctx.send('Yo %s, <@%s> <=> https://funnyjunk.com/u/%s' % (ctx.message.author.mention, disc_id, username))
  
