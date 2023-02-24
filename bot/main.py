import os

from discord import Embed, Colour, EmbedField
from discord.ext.commands import Context
from discord.ext import commands as cmd

# from crud import get_user_by_discord_id, create_user
# import schemas
# from db import get_db
from config import get_settings

from botinit import bot


@bot.group(name="service")
async def service(ctx: Context):
    pass


@service.command(name="load")
@cmd.has_role("Technician")
async def load(ctx: Context, cog: str):
    try:
        bot.unload_extension(f"commands.{cog}")
    except Exception as e:
        pass
    bot.load_extension(f"commands.{cog}")
    e = Embed(title=f"Loaded {cog}.", color=Colour.dark_green())
    await ctx.reply(embed=e)


@service.command(name="reload")
@cmd.has_role("Technician")
async def reload(ctx: Context, cog: str):
    try:
        bot.reload_extension(f"commands.{cog}")
        embed=Embed(
            title=f"Reloaded {cog}",
            colour=Colour.dark_green()
        )
        await ctx.reply(embed=embed)
    except Exception as e:
        await ctx.reply(e)


@service.command(name="loadall")
@cmd.has_role("Technician")
async def load_all(ctx: Context):
    try:
        for file in os.listdir("./commands"):
            if file.endswith(".py"):
                cog = file[:-3]
                try:
                    bot.unload_extension(f"commands.{cog}")
                except Exception as e:                    
                    bot.load_extension(f"commands.{cog}")
    except Exception as e:
        embed = Embed(
            title=f"Failed to load cog. ({e})",
            color=Colour.dark_red(),
        )
        await ctx.reply(embed=embed)


@service.command(name="modules")
@cmd.has_role("Technician")
async def list_cogs(ctx: Context):
    embed = Embed(
        title="Loaded modules:",
        fields=[EmbedField(name=name, value="") for name in bot.cogs.keys()],
        colour=Colour.dark_blue()
    )
    await ctx.reply(embed=embed)


bot.run(get_settings().DISCORD_TOKEN)
