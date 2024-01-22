import re
import random

import validators

from discord import Cog, Bot, Member, Message, Embed
from discord.ext import commands as cmd
from discord.ext.commands import Context

from utils.checks import can_have_fun
from cogs.gags_logic import GagsLogic
from config import get_settings
import help.gag as helpfor

emoji_regex = re.compile(r"<a?:(.+):(\d+)>")


class Ballgag(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        config = get_settings()
        guild = bot.get_guild(config.GUILD_ID)
        gag_role = guild.get_role(config.GAG_ROLES["ball"])
        collision_roles = {
            guild.get_role(config.GAG_ROLES["kitty"]),
            guild.get_role(config.GAG_ROLES["uwu"]),
        }

        self.logic = GagsLogic(bot, gag_role, collision_roles, config)

    @cmd.command(name="ballgag", aliases=["ball", "gag-ball"], help=helpfor.NEW_BALL)
    @can_have_fun()
    async def ballgag(self, ctx: Context, user: Member):
        await self.logic.apply_gag(ctx, user)
        await ctx.send(embed=Embed(description=f"{user.mention} ballgagged."))

    @cmd.command(
        name="unballgag", aliases=["deball", "de-ball", "un-ball", "un-ballgag"]
    )
    @can_have_fun()
    async def ungag(self, ctx: Context, user: Member):
        await self.logic.remove_gag(user)
        await ctx.send(embed=Embed(description=f"{user.mention} unballgagged."))

    def muffle(self, msg):
        letters = ["m", "m", "m", "m", "h", "ph"]
        ret = ""
        for word in msg.split():
            if validators.url(word):
                word = "link"
            if emoji_regex.search(word):
                word = "emoji"
            for i in word:
                ret += random.choice(letters)
            ret += " "

        return ret

    @Cog.listener()
    async def on_message(self, message: Message):
        await self.logic.gaggify(message, self.muffle)

def setup(bot: Bot):
    bot.add_cog(Ballgag(bot))