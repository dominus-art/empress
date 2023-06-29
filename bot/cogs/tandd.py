from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from discord import ApplicationContext
from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context

from crud.tandd import (
    create_dare,
    create_truth,
    get_random_pg_dare,
    get_random_pg_question,
    get_random_r_dare,
    get_random_r_question,
)
from database import get_session
from utils.checks import is_trusted_member
from utils.embed import tandd_embed


RATE_MAPPING_IN = {"R": 0, "PG": 1}
RATE_MAPPING_OUT = {0: "R", 1: "PG"}


class Tandd(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @cmd.group(name="truth")
    async def truth(self, ctx: Context):
        if not ctx.invoked_subcommand:
            return

    @truth.command(name="PG", aliases=["pg", "sfw", "SFW"])
    async def PG_t(self, ctx: Context):
        question = await get_random_pg_question()
        embed = tandd_embed(ctx).add_field(name=question.question, value="")
        embed.set_footer(text="TRUTH | Rating: PG")
        await ctx.reply(embed=embed)

    @truth.command(name="R", aliases=["r", "nsfw", "NSFW"])
    async def R_t(self, ctx: Context):
        question = await get_random_r_question()
        embed = tandd_embed(ctx).add_field(name=question.question, value="")
        embed.set_footer(text="TRUTH | Rating: R")
        await ctx.reply(embed=embed)

    @truth.command(name="create")
    @is_trusted_member()
    async def create_t(self, ctx: Context, rating: str, *, content: str):
        new_truth = await create_truth(RATE_MAPPING_IN[rating.upper()], content)
        embed = tandd_embed(ctx)
        embed.title = "New dare created."
        embed.timestamp = datetime.now()
        embed.add_field(name="Rating:", value=RATE_MAPPING_OUT[new_truth.rating])
        embed.add_field(name="Question:", value=new_truth.question)
        await ctx.reply(embed=embed)

    @cmd.group(name="dare")
    async def dare(self, ctx: Context):
        if not ctx.invoked_subcommand:
            return

    @dare.command(name="PG", aliases=["pg", "sfw", "SFW"])
    async def PG_d(self, ctx: Context):
        dare = await get_random_pg_dare()
        embed = tandd_embed(ctx)
        embed.add_field(name=dare.dare, value="")
        embed.set_footer(text="DARE | Rating: PG")
        await ctx.reply(embed=embed)

    @dare.command(name="R", aliases=["r", "nsfw", "NSFW"])
    async def R_d(self, ctx: Context):
        dare = await get_random_r_dare()
        embed = tandd_embed(ctx)
        embed.add_field(name=dare.dare, value="")
        embed.set_footer(text=f"DARE | Rating: R")
        await ctx.reply(embed=embed)

    @dare.command(name="create")
    @is_trusted_member()
    async def create_d(self, ctx: Context, rating: str, *, content: str):
        new_dare = await create_dare(RATE_MAPPING_IN[rating.upper()], content)
        embed = tandd_embed(ctx)
        embed.title = "New dare created."
        embed.timestamp = datetime.now()
        embed.add_field(name="Rating:", value=RATE_MAPPING_OUT[new_dare.rating])
        embed.add_field(name="Dare:", value=new_dare.dare)
        await ctx.reply(embed=embed)

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)


def setup(bot: Bot):
    bot.add_cog(Tandd(bot))
