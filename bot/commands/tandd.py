from discord import Member, Message, Webhook, Role, ApplicationContext

from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context


class Tandd(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @cmd.group(name="truth")
    async def truth(self, ctx: Context):
        pass

    @truth.command(name="PG")
    async def PG(self, ctx: Context):
        pass

    @truth.command(name="R")
    async def R(self, ctx: Context):
        pass

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)

def setup(bot: Bot):
    bot.add_cog(Tandd(bot))