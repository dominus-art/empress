import re
import random

from discord import Cog, Bot, Member, Message, Embed
from discord.ext.commands import Context
from discord.ext import commands as cmd

from utils.checks import can_have_fun
from config import get_settings
from cogs.gags_logic import GagsLogic
import help.gag as helpfor

kitty_messages = [
    "I just spit out a huge hair ball",
    "I just pooped under the couch",
    "I puked under the bed",
    "I left a dookie on the bed",
    "I pooped outside the litterbox",
    "I'm in heat, please breed me",
    "Cuddle with me",
    "I want strangers to pet me",
    "Please, rub my belly",
]

kitty_sounds = ["*mrrp*", "*meow*", "*nya*", "*rawr*", "*purrr*", "*mrawr*"]

kitty_sanitize = {
    r"won't": "will not",
    r"can't": "can not",
}

kitty_map = {
    r"n't": "nyan't",
    r"not": "nyan't",
    r"now": "nyaw",
    r"owner": "meowner",
    r"know": "kneow",
    r"mention": "meowntion",
    r"opinion": "opinyan",
}


class Kitty(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        config = get_settings()
        guild = bot.get_guild(config.GUILD_ID)
        gag_role = guild.get_role(config.GAG_ROLES["kitty"])
        collision_roles = {
            guild.get_role(config.GAG_ROLES["ball"]),
            guild.get_role(config.GAG_ROLES["uwu"]),
        }

        self.logic = GagsLogic(bot, gag_role, collision_roles, config)
        self.kitty_regex = {
            sub: re.compile(pattern) for pattern, sub in kitty_map.items()
        }
        self.kitty_sanitize = {
            sub: re.compile(pattern) for pattern, sub in kitty_sanitize.items()
        }

    @cmd.command(name="kitty", aliases=["kittify", "gag-kitty"], help=helpfor.NEW_KITTY)
    @can_have_fun()
    async def gag(self, ctx: Context, user: Member):
        await self.logic.apply_gag(ctx, user)
        await ctx.send(embed=Embed(description=f"{user.mention} is now a kitten :3"))

    @cmd.command(name="unkitty", aliases=["kitty-off", "un-kitty", "kittyoff"])
    @can_have_fun()
    async def ungag(self, ctx: Context, user: Member):
        await self.logic.remove_gag(user)
        await ctx.send(
            embed=Embed(description=f"{user.mention} is back to human form.")
        )

    def _kittify_stage_one(self, message: str) -> str:
        for repl, regex in self.kitty_sanitize.items():
            message = regex.sub(repl, message)
        for repl, regex in self.kitty_regex.items():
            message = regex.sub(repl, message)
        return message

    def _kittify_stage_two(self, message: str) -> str:
        ret = f"{random.choice(kitty_sounds)} "
        for word in message.split(" "):
            if random.randint(0, 6) > 5:
                ret += f"{word} {random.choice(kitty_sounds)} "
            else:
                ret += f"{word} "
        if random.randint(0, 1) == 1:
            ret += ":3"
        return ret

    def kittify(self, message: str) -> str:
        message = self._kittify_stage_one(message)
        return self._kittify_stage_two(message)

    @Cog.listener()
    async def on_message(self, message: Message):
        await self.logic.gaggify(message, self.kittify)

    async def cog_command_error(self, ctx, error: Exception):
        embed = Embed()
        embed.description = f"{error}"
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Kitty(bot))
