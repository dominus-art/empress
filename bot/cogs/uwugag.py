import random

from discord import Cog, Bot, Message, Member, Embed
from discord.ext import commands as cmd
from discord.ext.commands import Context

import uwuify

from utils.checks import can_have_fun
from cogs.gags_logic import GagsLogic
from config import get_settings
import help.gag as helpfor


class Uwu(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        config = get_settings()
        guild = bot.get_guild(config.GUILD_ID)
        gag_role = guild.get_role(config.GAG_ROLES["uwu"])
        collision_roles = {
            guild.get_role(config.GAG_ROLES["ball"]),
            guild.get_role(config.GAG_ROLES["kitty"]),
        }

        self.logic = GagsLogic(bot, gag_role, collision_roles, config)

    @cmd.command(name="uwu", aliases=["uwuify", "gag-uwu"], help=helpfor.NEW_UWU)
    @can_have_fun()
    async def uwu(self, ctx: Context, user: Member):
        await self.logic.apply_gag(ctx, user)
        await ctx.send(embed=Embed(description=f"OwO {user.mention} UwU"))

    @cmd.command(name="deuwu", aliases=["unuwu"])
    @can_have_fun()
    async def unuwu(self, ctx: Context, user: Member):
        await self.logic.remove_gag(user)
        await ctx.send(embed=Embed(description=f"TwT {user.mention} TwT"))

    def uwu_msg(self, message: str) -> str:
        flags = uwuify.NOUWU
        for flag in random.choices(
            [uwuify.SMILEY, uwuify.STUTTER, uwuify.YU], k=random.randint(1, 3)
        ):
            flags = flags | flag
        return uwuify.uwu(message, flags=flags)

    @Cog.listener()
    async def on_message(self, message: Message):
        await self.logic.gaggify(message, self.uwu_msg)

def setup(bot: Bot):
    bot.add_cog(Uwu(bot))