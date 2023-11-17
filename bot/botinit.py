from discord import Intents
from discord.ext.commands import Bot

from config import get_settings
from myhelp import MyHelp

intents = Intents(
    webhooks=True, message_content=True, messages=True, members=True, guilds=True
)

bot = Bot(command_prefix=get_settings().PREFIX, intents=intents)
bot.help_command = MyHelp()
