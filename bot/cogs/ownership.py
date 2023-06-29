from discord import Member, ApplicationContext
from discord.ext.commands import Context, Bot, Cog
from discord.ext import commands as cmd


class Ownership(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot: Bot = bot

    @cmd.command(name="claim")
    @cmd.has_any_role("Domme Punishment Perms")
    async def claim(ctx: Context, user: Member):
        pass

    @cmd.command(name="accept")
    @cmd.has_any_role()
    async def accept(ctx: Context):
        pass

    @cmd.command(name="decline")
    @cmd.has_any_role()
    async def decline(ctx: Context):
        pass

    @cmd.command(name="disown")
    @cmd.has_any_role("Domme Punishment Perms")
    async def disown(ctx: Context, user: Member):
        pass

    @cmd.group(name="my")
    async def my(self, ctx: Context):
        pass

    @my.command(name="subs")
    async def subs(self, ctx: Context):
        pass

    @my.command(name="owner")
    async def owner(self, ctx: Context):
        pass

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)


def setup(bot: Bot):
    bot.add_cog(Ownership(bot))
