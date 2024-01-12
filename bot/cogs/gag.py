import random
import re
from enum import Enum

import validators
import uwuify

from discord import Member, Message, Webhook, Role, ApplicationContext, Embed, Color
from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context

from config import get_settings
from utils.checks import can_have_fun, can_ungag
from utils.embed import gag_embed
import help.gag as helpfor
import crud.gag

emoji_regex = re.compile(r"<a?:(.+):(\d+)>")
user_regex = re.compile(r"<@\d+>")

kitty_messages = [
    "I just spit out a huge hair ball",
    "I just pooped under the couch",
    "I puked under the bed",
    "I left a dookie on the bed",
    "I pooped outside the litterbox",
    "I'm in heat, please breed me",
    "Cuddle with me",
    "I want strangers to pet me",
    "Please, rub my belly"
]

kitty_sounds = [
    "*mrrp*",
    "*meow*",
    "*nya*",
    "*rawr*",
    "*purrr*",
    "*mrawr*"
]

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


class Gag(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot: Bot = bot
        guild = self.bot.get_guild(get_settings().GUILD_ID)
        self.gag_role: Role = guild.get_role(get_settings().GAG_ROLES["ball"])
        self.uwu_role: Role = guild.get_role(get_settings().GAG_ROLES["uwu"])
        self.kitty_role: Role = guild.get_role(get_settings().GAG_ROLES["kitty"])
        self.roles = {self.gag_role, self.uwu_role, self.kitty_role}

        self.kitty_regex = {sub: re.compile(pattern) for pattern, sub in kitty_map.items()}
        self.kitty_sanitize = {sub: re.compile(pattern) for pattern, sub in kitty_sanitize.items()}
        self.db_ungag = crud.gag.ungag
        self.db_gag = crud.gag.gag

    @cmd.group(name="gag", invoke_without_command=True)
    @can_have_fun()
    async def gag(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return

    @cmd.command(name="ungag", help=helpfor.UNGAG)
    @can_ungag()
    async def ungag(self, ctx: Context, user: Member):
        embed = gag_embed(ctx)
        embed.description = f"{user.mention} is free to speak again!"
        # await self.db_ungag(user.id)
        if self.gag_role in user.roles:
            await user.remove_roles(self.gag_role)
        elif self.uwu_role in user.roles:
            await user.remove_roles(self.uwu_role)
        elif self.kitty_role in user.roles:
            await user.remove_roles(self.kitty_role)
        await ctx.send(embed=embed)

    async def _check_if_not_gaggable(self, ctx: Context, user: Member):
        target_roles = set([role.id for role in user.roles])
        if (
            get_settings().DOM_ROLE in target_roles
            and get_settings().SWITCH_ROLE not in target_roles
        ):
            embed.description = "Cannot apply gag to a Domme."
            await ctx.reply(embed=embed)
            return True
        elif ctx.author.id == user.id:
            embed.description = "Don't gag yourself..."
            await ctx.reply(embed=embed)
            return True
        False

    @gag.command(name="uwu", help=helpfor.UWU)
    @can_have_fun()
    async def gag_uwu(self, ctx: Context, user: Member):
        if await self._check_if_not_gaggable(ctx, user):
            return
        embed = gag_embed(ctx)
        await user.add_roles(self.uwu_role)
        # await self.db_gag(user.id)
        embed.description = f"{user.mention} {uwuify.uwu('will now speak like this!')}"
        embed.color = Color.dark_purple()
        await ctx.send(embed=embed)

    @gag.command(name="ball", help=helpfor.BALL)
    @can_have_fun()
    async def gag_ball(self, ctx: Context, user: Member):
        if await self._check_if_not_gaggable(ctx, user):
            return
        await user.add_roles(self.gag_role)
        # await self.db_gag(user.id)
        embed = gag_embed(ctx)
        embed.color = Color.dark_purple()
        embed.description = f"{user.mention} now has ball gag in their mouth."
        await ctx.send(embed=embed)

    @gag.command(name="kitty")
    @can_have_fun()
    async def kitty_gag(self, ctx: Context, user: Member):
        if await self._check_if_not_gaggable(ctx, user):
            return
        await user.add_roles(self.kitty_role)
        embed = gag_embed(ctx)
        embed.color = Color.dark_purple()
        embed.description = f"{user.mention} is a kitten now."
        await ctx.send(embed=embed)

    def muffle(self, msg: str) -> str:
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

    def uwu(self, msg: str) -> str:
        flags = [uwuify.SMILEY, uwuify.STUTTER, uwuify.YU]
        return uwuify.uwu(msg, flags=random.choice(flags))

    def _kittify(self, msg: str) -> str:
        for repl, regex in self.kitty_sanitize.items():
            msg = regex.sub(repl, msg)
        for repl, regex in self.kitty_regex.items():
            msg = regex.sub(repl, msg)
        return msg

    def _kittify_more(self, msg: str) -> str:
        ret = f"{random.choice(kitty_sounds)} "
        for word in msg.split():
            if random.randint(0, 6) > 5:
                ret += f"{word} {random.choice(kitty_sounds)}"
            else:
                ret += word
        return ret

    def kitty(self, msg: str) -> str:
        if random.randint(0, 100) > 98:
            msg = random.choice(kitty_messages)
        msg = self._kittify(msg)
        return self._kittify_more(msg)
        

    def _check_if_gagged(self, message: Message):
        target_roles = {role for role in message.author.roles}
        return target_roles.isdisjoint(self.roles)


    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        if self._check_if_gagged(message):
            return

        webhooks = self.bot.get_cog("Webhooks").webhooks
        if message.channel.id not in webhooks:
            return

        await message.delete()

        webhook: Webhook = webhooks[message.channel.id]
        
        if self.gag_role in message.author.roles:
            new_msg = self.muffle(message.content)
        elif self.kitty_role in message.author.roles:
            new_msg = self.kitty(message.content)
        else:
            new_msg = self.uwu(message.content)
        
        await webhook.send(
            content=new_msg,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar,
        )

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        embed = Embed(description=error)
        await ctx.send(embed=embed)

    # @Cog.listener()
    # async def on_member_update(self, before: Member, after: Member):
    #     db_user = await crud.user.get_user(before.id)
    #     if not db_user:
    #         return
    #     if not db_user.role_lock:
    #         return
    #     before_roles_set = {role for role in before.roles if role in self.roles}
    #     after_roles_set = {role for role in after.roles if role in self.roles}
    #     if not before_roles_set.isdisjoint(after_roles_set):
    #         return
    #     else:
    #         for role in before_roles_set:
    #             await after.add_roles(role)

        


def setup(bot: Bot):
    bot.add_cog(Gag(bot))
