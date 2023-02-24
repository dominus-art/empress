from discord.ext.commands import Context, Cog, Bot
from discord.ext import commands as cmd


class Safeword(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot: Bot = bot

    @cmd.command(name="RED")
    async def RED(self, ctx: Context):
        pass

    @cmd.command(name="PEACE")
    async def PEACE(self, ctx: Context):
        pass

    @cmd.command(name="PEACEOFF")
    async def PEACEOFF(self, ctx: Context):
        pass


def setup(bot: Bot):
    bot.add_cog(Safeword(bot))
