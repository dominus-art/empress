from discord import ApplicationContext

from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context


class Newbie(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cmd.command(name="newbie")
    async def newbie(self, ctx: Context):
        await ctx.reply(f"Hello there, {ctx.author.mention}!")

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)


def setup(bot: Bot):
    bot.add_cog(Newbie(bot))
