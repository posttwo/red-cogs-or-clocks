import discord
from redbot.core import Config, commands, checks, bot

BaseCog = getattr(commands, "Cog", object)

class PunishCog(BaseCog):

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
        await self.config.member(member).forced_nickname.set(member.nick)
        await ctx.send('{0} is now unable to change his username'.format(member))
    
    
    @punish.command(pass_context=True, no_pm=True, name='remove')
    @checks.mod_or_permissions(manage_messages=True)
    async def punish_remove(self, ctx, member: discord.Member):
        """Allows user to have nickname changed"""
        await self.config.member(member).forced_nickname.set("")
        await ctx.send('{0} is now able to change his username'.format(member))
    
    @punish.command(pass_context=True, no_pm=True, name='list')
    async def punish_list(self, ctx):
        """Lists users that are blocked from changing their nickname"""
        await ctx.send("Yeah this is fucked sorry.")
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            print("Member changed nickname")
            member_data = await self.config.member(before).forced_nickname()
            print("Punished into name: %s" % (member_data))
            if member_data == "":
                return

        if before.nick != after.nick and after.nick != member_data:
            print("Trying to undo the name change")
            await after.edit(nick=member_data, reason="Punished user")
            await after.send(content='{0} youre not allowed to change your nickname'.format(after.mention))
