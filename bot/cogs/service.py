from pathlib import Path
from datetime import datetime

from discord import Embed, Color, ApplicationContext
from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context

from utils.checks import is_techpriest

cogs_dir = Path("cogs")


def fill_embed(ctx: Context) -> Embed:
    return Embed(color=Color.magenta(), timestamp=datetime.now()).set_author(
        name=ctx.author.name, icon_url=ctx.author.display_avatar
    )


class Service(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @cmd.group(name="service")
    @is_techpriest()
    async def service(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return

    @service.command(name="load")
    @is_techpriest()
    async def load(self, ctx: Context, *, cogs: str):
        embed = fill_embed(ctx)
        actions = []
        for cog in cogs.split():
            cog = cog.strip()
            cog_path = Path(cogs_dir, f"{cog}.py")
            if not cog_path.exists():
                actions.append(f"{cog} does not exist.")
            module_name = f"cogs.{cog}"
            try:
                self.bot.unload_extension(module_name)
                self.bot.load_extension(module_name)
                actions.append(f"{cog} reloaded.")
            except Exception:
                self.bot.load_extension(module_name)
                actions.append(f"{cog} loaded.")

        embed.add_field(name="Report:", value="\n".join(actions))
        await ctx.send(embed=embed)

    @service.command(name="list-cogs")
    @is_techpriest()
    async def list_cogs(self, ctx: Context):
        embed = fill_embed(ctx).add_field(
            name="Loaded cogs:", value="\n".join(self.bot.cogs.keys())
        )
        await ctx.send(embed=embed)

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        embed = Embed(title="ERROR", description=error)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Service(bot))
