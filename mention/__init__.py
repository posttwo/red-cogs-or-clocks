from .mention import Mention

def setup(bot):
    bot.add_cog(Mention(bot))
