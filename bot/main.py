from pathlib import Path
from datetime import datetime
import logging

from discord import Embed, Color

from config import get_settings
from botinit import bot


logger = logging.getLogger("empress")
logger.setLevel(logging.DEBUG)


@bot.event
async def on_ready():
    load_results = []
    for cog in get_settings().DEFAULT_COGS:
        cog_path = Path("cogs", f"{cog}.py")
        if not cog_path.exists():
            continue
        module_name = f"cogs.{cog}"
        load_result = bot.load_extension(module_name, store=True)
        load_results.append(f"{cog.capitalize()}: {load_result[module_name]}")
    embed = Embed(title="Empress started", timestamp=datetime.now())
    embed.color = Color.fuchsia()
    embed.add_field(name="Loaded modules:", value="\n".join(load_results))
    channel = bot.get_channel(get_settings().TECH_CHANNEL)
    await channel.send(embed=embed)


bot.run(get_settings().DISCORD_TOKEN)
