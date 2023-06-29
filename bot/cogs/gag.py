import random
import re

import validators
import uwuify

from discord import Member, Message, Webhook, Role, ApplicationContext, Embed, Color
from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context

from config import get_settings
from utils.checks import can_have_fun, can_ungag
from utils.embed import gag_embed

emoji_regex = re.compile(r"<:(.+):(\d+)>")


class Gag(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot: Bot = bot
        guild = self.bot.get_guild(get_settings().GUILD_ID)
        self.gag_role: Role = guild.get_role(get_settings().GAG_ROLES["ball"])
        self.uwu_role: Role = guild.get_role(get_settings().GAG_ROLES["uwu"])

    @cmd.group(name="gag", invoke_without_command=True)
    async def gag(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return

    @cmd.command(name="ungag")
    @can_ungag()
    async def ungag(self, ctx: Context, user: Member):
        embed = gag_embed(ctx)
        embed.description = f"{user.mention} is free to speak again!"
        if self.gag_role in user.roles:
            await user.remove_roles(self.gag_role)
        elif self.uwu_role in user.roles:
            await user.remove_roles(self.uwu_role)
        await ctx.send(embed=embed)

    @gag.command(name="uwu")
    @can_have_fun()
    async def gag_uwu(self, ctx: Context, user: Member):
        target_roles = set([role.id for role in user.roles])
        embed = gag_embed(ctx)
        if (
            get_settings().DOM_ROLE in target_roles
            and get_settings().SWITCH_ROLE not in target_roles
        ):
            embed.description = "Cannot apply gag to a Domme."
            await ctx.reply(embed=embed)
            return
        elif ctx.author.id == user.id:
            embed.description = f"Don't gag yourself..."
            await ctx.reply(embed=embed)
            return
        await user.add_roles(self.uwu_role)
        embed.description = f"{user.mention} {uwuify.uwu('will now speak like this!')}"
        embed.color = Color.dark_purple()
        await ctx.send(embed=embed)

    @gag.command(name="ball")
    @can_have_fun()
    async def gag_ball(self, ctx: Context, user: Member):
        target_roles = set([role.id for role in user.roles])
        embed = gag_embed(ctx)
        if (
            get_settings().DOM_ROLE in target_roles
            and get_settings().SWITCH_ROLE not in target_roles
        ):
            embed.description = "Cannot apply gag to a Domme."
            await ctx.reply(embed=embed)
            return
        elif ctx.author.id == user.id:
            embed.description = f"Don't gag yourself..."
            await ctx.reply(embed=embed)
            return

        await user.add_roles(self.gag_role)
        embed.color = Color.dark_purple()
        embed.description = f"{user.mention} now has ball gag in their mouth."
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

    @Cog.listener()
    async def on_message(self, message: Message):
        if (
            not self.gag_role in message.author.roles
            and not self.uwu_role in message.author.roles
        ):
            return

        webhooks = self.bot.get_cog("Webhooks").webhooks
        if not message.channel.id in webhooks:
            return

        await message.delete()
        webhook: Webhook = webhooks[message.channel.id]
        if self.gag_role in message.author.roles:
            new_msg = self.muffle(message.content)
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


def setup(bot: Bot):
    bot.add_cog(Gag(bot))
