from typing import List
from datetime import datetime

from discord import Role, Embed
from discord.ext.commands import Context, Cog, Bot
from discord.ext import commands as cmd

from config import get_settings


class Safeword(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot: Bot = bot
        guild = bot.get_guild(get_settings().GUILD_ID)
        self.bad_roles: List[Role] = [
            guild.get_role(role) for _, role in get_settings().GAG_ROLES.items()
        ]
        self.bad_roles.append(guild.get_role(get_settings().BADWORDS_ROLE))
        self.peace_role: Role = guild.get_role(get_settings().PEACE_ROLE)

    @cmd.command(name="RED", aliases=["red", "R", "r"])
    async def RED(self, ctx: Context):
        for role in self.bad_roles:
            await ctx.author.remove_roles(role)
        await ctx.author.add_roles(self.peace_role)
        await ctx.reply(
            "You're now in peace mode. Take some time to calm down. Use `&peaceoff` when You're ready."
        )

    @cmd.command(name="PEACE", aliases=["peace"])
    async def PEACE(self, ctx: Context):
        await ctx.author.add_roles(self.peace_role)
        embed = Embed(
            description=f"{ctx.author.mention} you're now in peace mode. Hope to see you soon!",
            timestamp=datetime.now(),
        )
        await ctx.send(embed=embed)

    @cmd.command(name="PEACEOFF", aliases=["peaceoff", "peace-off", "PEACE-OFF"])
    async def PEACEOFF(self, ctx: Context):
        await ctx.author.remove_roles(self.peace_role)
        embed = Embed(
            description=f"Welcome back {ctx.author.mention}!", timestamp=datetime.now()
        )
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Safeword(bot))
