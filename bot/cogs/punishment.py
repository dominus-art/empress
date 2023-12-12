from discord import Member, ApplicationContext, Role
from discord.ext.commands import Context, Bot, Cog
from discord.ext import commands as cmd

from utils.checks import can_have_fun
import help.punishments as helpfor
from config import get_settings

config = get_settings()


class Punishments(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        guild = bot.get_guild(config.GUILD_ID)
        self.role_nospeech: Role = guild.get_role(config.NOSPEECH_ROLE)
        self.role_noreact: Role = guild.get_role(config.NOREACTIONS_ROLE)
        self.role_nonsfw: Role = guild.get_role(config.NONSFW_ROLE)
        self.role_nomedia: Role = guild.get_role(config.NOMEDIA_ROLE)

    @cmd.command(name="nospeech", aliases=["no-speech"], help=helpfor.NOSPEECH)
    @can_have_fun()
    async def nospeech(self, ctx: Context, user: Member):
        await self._add_role(self.role_nospeech, user)
        # await self._react(ctx)

    @cmd.command(name="speech", help=helpfor.SPEECH)
    @can_have_fun()
    async def speech(self, ctx: Context, user: Member):
        await self._remove_role(self.role_nospeech, user)
        # await self._react(ctx)

    @cmd.command(name="nomedia", help=helpfor.NOMEDIA, aliases=["no-media"])
    @can_have_fun()
    async def nomedia(self, ctx: Context, user: Member):
        await self._add_role(self.role_nomedia, user)
        # await self._react(ctx)

    @cmd.command(name="media", help=helpfor.MEDIA)
    @can_have_fun()
    async def media(self, ctx: Context, user: Member):
        await self._remove_role(self.role_nomedia, user)
        # await self._react(ctx)

    @cmd.command(name="noreactions", help=helpfor.NOREACTIONS, aliases=["no-reactions"])
    @can_have_fun()
    async def noreactions(self, ctx: Context, user: Member):
        await self._add_role(self.role_noreact, user)
        # await self._react(ctx)

    @cmd.command(name="reactions", help=helpfor.REACTIONS)
    @can_have_fun()
    async def reactions(self, ctx: Context, user: Member):
        await self._remove_role(self.role_noreact, user)
        # await self._react(ctx)

    @cmd.command(name="nonsfw", help=helpfor.NONSFW, aliases=["no-nsfw"])
    @can_have_fun()
    async def nonsfw(self, ctx: Context, user: Member):
        await self._add_role(self.role_nonsfw, user)
        # await self._react(ctx)

    @cmd.command(name="nsfw", help=helpfor.NSFW)
    @can_have_fun()
    async def nsfw(self, ctx: Context, user: Member):
        await self._add_role(self.role_nonsfw, user)
        # await self._react(ctx)

    async def _add_role(self, role: Role, user: Member):
        await user.add_roles(role)

    async def _remove_role(self, role: Role, user: Member):
        await user.remove_roles(role)

    async def _react(self, ctx: Context):
        await ctx.message.add_reaction(":ballot_box_with_check:")

    async def cog_command_error(self, ctx: ApplicationContext, err: Exception):
        await ctx.send(err)


def setup(bot: Bot):
    bot.add_cog(Punishments(bot))
