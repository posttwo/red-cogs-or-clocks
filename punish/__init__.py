from .punish import PunishCog

def setup(bot):
    bot.add_cog(PunishCog(bot))
