from datetime import datetime

from discord import Embed, Color
from discord.ext.commands import Context


def base_embed(ctx: Context) -> Embed:
    return Embed(timestamp=datetime.now()).set_author(
        name=ctx.author.display_name, icon_url=ctx.author.display_avatar
    )


def service_embed(ctx: Context) -> Embed:
    embed = base_embed(ctx)
    embed.color = Color.magenta()
    return embed


def gag_embed(ctx: Context) -> Embed:
    embed = base_embed(ctx)
    embed.color = Color.dark_green()
    return embed


def tandd_embed(ctx: Context) -> Embed:
    embed = base_embed(ctx)
    embed.color = Color.dark_teal()
    embed.set_author(name=f"Requested by {ctx.author.display_name}")
    return embed


def badword_embed(ctx: Context) -> Embed:
    embed = base_embed(ctx)
    embed.color = Color.dark_purple()
    return embed
