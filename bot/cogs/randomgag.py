import aiohttp
import random

from discord import Cog, Bot, Member, Message, Embed
from discord.ext import commands as cmd
from discord.ext.commands import Context

from utils.checks import can_have_fun
from cogs.gags_logic import GagsLogic
from config import get_settings


class Randomgag(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

        config = get_settings()
        guild = bot.get_guild(config.GUILD_ID)
        gag_role = guild.get_role(config.GAG_ROLES["random"])
        collision_roles = {
            guild.get_role(config.GAG_ROLES["kitty"]),
            guild.get_role(config.GAG_ROLES["uwu"]),
            guild.get_role(config.GAG_ROLES["ball"]),
        }

        self.logic = GagsLogic(bot, gag_role, collision_roles, config)

    @cmd.command(name="gag-random")
    @can_have_fun()
    async def ballgag(self, ctx: Context, user: Member):
        await self.logic.apply_gag(ctx, user)
        await ctx.send(embed=Embed(description=f"{user.mention} ballgagged."))

    @cmd.command(name="unrandom")
    @can_have_fun()
    async def ungag(self, ctx: Context, user: Member):
        await self.logic.remove_gag(user)
        await ctx.send(embed=Embed(description=f"{user.mention} unballgagged."))

    async def muffle(self, msg: str) -> str:
        url = "https://random-word-api.vercel.app/api?words="
        words: list[str] = msg.split()
        words_num = len(words)
        rands: list[str]
        ret: list[str] = []
        req = f"{url}{words_num}"
        async with self.session.get(req) as r:
            if not r.ok:
                return r.reason
            else:
                rands = await r.json()
        
        word: str
        for i, word in enumerate(words):
            if random.randint(1, 5) > 3:
                word = rands[i]
            ret.append(word)

        return " ".join(ret)

    @Cog.listener()
    async def on_message(self, message: Message):
        await self.logic.async_gaggify(message, self.muffle)


def setup(bot: Bot):
    bot.add_cog(Randomgag(bot))
