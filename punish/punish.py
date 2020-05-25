import discord
from redbot.core import Config, commands, checks, bot

class PunishCog:

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=487948989)
        self.config.register_member(
            forced_nickname=""
        )
    
    
    @commands.group(pass_context=True, invoke_without_command=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def punish(self, ctx, member: discord.Member):
        """Stops user from having his nickname changed by ANYONE"""
        await self.config.member(ctx.author).forced_nickname.set_raw(member.nick)
        await self.bot.say('{0} is now unable to change his username'.format(member))
    
    
    @punish.command(pass_context=True, no_pm=True, name='remove')
    @checks.mod_or_permissions(manage_messages=True)
    async def punish_remove(self, ctx, member: discord.Member):
        """Allows user to have nickname changed"""
        await self.config.member(ctx.author).forced_nickname.set_raw("")
        await self.bot.say('{0} is now able to change his username'.format(member))
    
    @punish.command(pass_context=True, no_pm=True, name='list')
    async def punish_list(self, ctx):
        """Lists users that are blocked from changing their nickname"""
        await self.bot.say("Yeah this is fucked sorry.")
        
        
    async def on_member_update(self, before, after):
        sid = before.server.id
        member_data = await self.config.member(before).forced_nickname
        if member_data is "":
            return

        if before.nick != after.nick and after.nick != member_data:
            await self.bot.change_nickname(after, member_data['nickname'])
            await self.bot.send_message(after, '{0} youre not allowed to change your nickname'.format(after.mention))