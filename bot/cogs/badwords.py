import json
from datetime import datetime
from typing import List, Optional, Union
import random

from sqlalchemy.ext.asyncio import AsyncSession

from discord import Member, Message, Role, ApplicationContext, Embed, Color
from discord.ext import commands as cmd
from discord.ext.commands import Context, Cog, Bot

import crud.user
import crud.badwords
from models.user import User as DbUser
from database import get_session
from config import get_settings
from utils.embed import badword_embed
from utils.checks import can_have_fun


class Badwords(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot: Bot = bot
        guild = bot.get_guild(get_settings().GUILD_ID)
        self.badword_role: Role = guild.get_role(get_settings().BADWORDS_ROLE)
        self.gag_roles: List[Role] = [
            guild.get_role(role) for _, role in get_settings().GAG_ROLES.items()
        ]

    @cmd.group(name="badword")
    async def badword(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return

    @badword.command(
        name="add",
        help="""Command arguments:
            - user: user id or @user
            - lives: optional number, defaults to 3 if not supplied
            - words: words separated by a space, case sensitive
            
            Example usage:
            &badword add @user 5 Napoleon napoleon Milk nun""",
    )
    @can_have_fun()
    async def add(
        self, ctx: Context, user: Member, lives: Optional[int] = 3, *, words: str
    ):
        embed = badword_embed(ctx)
        target_roles = set([role.id for role in user.roles])
        if user.id == ctx.author.id:
            embed.description = f"Don't play with yourself... weirdo"
            await ctx.reply(embed=embed)
            return
        if (
            get_settings().DOM_ROLE in target_roles
            and get_settings().SWITCH_ROLE not in target_roles
        ):
            await ctx.reply("Cannot apply rules to a Domme.")
            return

        embed.description = f"{user.mention} new speech rules."
        db_user = await crud.user.get_user(user.id)
        if not db_user:
            db_user = await crud.user.create_user(user.id)

        words_to_add = [word.strip().replace(",", "") for word in words.split()]
        await crud.badwords.add_badwords(user.id, words_to_add)
        had_previous_lives = False
        if not db_user.lives > 0:
            await crud.badwords.set_lives(user.id, lives)
        else:
            had_previous_lives = True

        await user.add_roles(self.badword_role)
        # TODO: Debug why the updated object doesn't get returned from crud operations
        # should use the returned sqlalchemy object but for some reasons I cannot understand it doesn't get updated
        # the database gets updated so we use params passed to the command directly instead to give user some feedback
        # can't be bothered to debug it now
        embed.add_field(
            name="Forbidden Words:",
            value=", ".join([*words_to_add, *json.loads(db_user.bad_words)]),
        )
        embed.add_field(
            name="Lives:",
            value=lives
            if had_previous_lives
            else f"Lives not updated. User already had lives set.\nCurrent lives: {db_user.lives}",
        )
        await ctx.send(embed=embed)

    @badword.command(name="remove")
    @can_have_fun()
    async def remove(self, ctx: Context, user: Member, *, words: str):
        embed = badword_embed(ctx)
        if not self.badword_role in user.roles:
            embed.description = f"{user.mention} has no badwords to remove."
            await ctx.reply(embed=embed)
            return

        words_to_remove = set([word.strip().strip(",") for word in words.split()])
        db_user, action_result = await crud.badwords.remove_badwords(
            user.id, words_to_remove
        )
        if isinstance(action_result, str):
            embed.description = f"{user.mention} {action_result}"
            await ctx.reply(embed=embed)
            return

        embed.add_field(
            name="Current forbidden words:", value=", ".join(db_user.bad_words)
        )
        embed.add_field(name="Raport:", value=", ".join(action_result))
        await ctx.send(embed=embed)

    @badword.command(name="clear")
    async def clear(self, ctx: Context, user: Member):
        embed = badword_embed(ctx)
        if not self.badword_role in user.roles:
            embed.description = f"{user.display_name} has no badwords to clear."
            await ctx.reply(embed=embed)
            return

        await crud.badwords.clear_badwords(user.id)
        await user.remove_roles(self.badword_role)
        embed.description = f"{user.display_name} cleared."
        await ctx.send(embed=embed)

    @badword.command(name="list")
    async def list(self, ctx: Context, user: Optional[Union[Member, None]] = None):
        embed = badword_embed(ctx)
        if not user:
            user = ctx.author
        if not self.badword_role in user.roles:
            embed.description = f"{user.display_name} has no badwords."
            await ctx.send(embed=embed)
            return
        db_user = await crud.user.get_user(user.id)
        embed.description = f"{user.display_name}"
        embed.add_field(
            name="Forbidden Words:", value=", ".join(json.loads(db_user.bad_words))
        )
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        if self.badword_role not in message.author.roles:
            return
        user = await crud.user.get_user(message.author.id)
        user_badwords = set(json.loads(user.bad_words))
        lives = user.lives
        if user_badwords.isdisjoint(
            set([word.strip(".,?;:'\"-_=+") for word in message.content.split()])
        ):
            return
        lives -= 1
        if lives <= 0:
            gag_role = random.choice(self.gag_roles)
            embed = Embed(
                description=f"{message.author.mention} run out of lives and is now gagged.",
                timestamp=datetime.now(),
            ).set_footer(text=f"Gag Type: {gag_role.name}")
            await crud.badwords.clear_badwords(message.author.id)
            await message.author.add_roles(gag_role)
            await message.author.remove_roles(self.badword_role)
            await message.channel.send(embed=embed)
            return
        user = await crud.badwords.set_lives(message.author.id, lives)
        embed = Embed(
            description=f"{message.author.mention} said a frobidden word!\nTheir live count: {user.lives}",
            timestamp=datetime.now(),
        )
        await message.channel.send(embed=embed)

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)


def setup(bot: Bot):
    bot.add_cog(Badwords(bot))
