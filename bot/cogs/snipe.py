from datetime import datetime
from collections import deque
from typing import Optional, Dict, Any

from discord import Embed, Color, Message, TextChannel, ApplicationContext
from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context, Greedy

from config import get_settings
from utils.checks import is_maintainer

import help.snipe as helpfor


class Snipe(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot
        self.cache: Dict[
            Any, deque
        ] = {}  # deque(maxlen=get_settings().SNIPE_CACHE_SIZE)
        # self.snipe_channels = set()
        self.snipe_channel_names = set()

    @cmd.group(
        name="s",
        invoke_without_command=True,
        aliases=["snipe", "sniper"],
        help=helpfor.SNIPE,
    )
    async def snipe(self, ctx: Context, index: Optional[int] = 1):
        i = index - 1
        cached_msg = self.cache[ctx.channel.id][i]
        embed = Embed()
        embed.add_field(name="", value=cached_msg["content"])
        embed.timestamp = cached_msg["date"]
        embed.set_author(name=cached_msg["author"], icon_url=cached_msg["icon"])
        # embed.set_image(cached_msg["attachments"])
        await ctx.send(embed=embed)

    @snipe.command(name="add", help=helpfor.ADD)
    @is_maintainer()
    async def add(self, ctx: Context, channels: Greedy[TextChannel]):
        embed = Embed(color=Color.dark_gold()).set_author(
            name=ctx.author.mention, icon_url=ctx.author.display_avatar
        )
        for channel in channels:
            self.cache[channel.id] = deque(maxlen=get_settings().SNIPE_CACHE_SIZE)
            self.snipe_channel_names.add(channel.name)
        embed.add_field(
            name="Watching channels:", value="\n".join(self.snipe_channel_names)
        )
        await ctx.reply(embed=embed)

    @snipe.command(name="remove", help=helpfor.REMOVE)
    @is_maintainer()
    async def remove(self, ctx: Context, channels: Greedy[TextChannel]):
        embed = Embed().set_author(
            name=ctx.author.mention, icon_url=ctx.author.display_avatar
        )
        actions = []
        for channel in channels:
            del self.cache[channel.id]
            self.snipe_channel_names.remove(channel.name)
            actions.append(f"removed {channel.name}")

        embed.add_field(name="Report:", value="\n".join(actions))
        await ctx.reply(embed=embed)

    def cache_msg(self, message: Message):
        if (
            message.author.bot
            or message.channel.id not in self.cache
            or message.content.startswith(get_settings().PREFIX)
        ):
            return
        self.cache[message.channel.id].appendleft(
            {
                "author": f"{message.author.display_name}\n({message.author.id})",
                "icon": message.author.display_avatar,
                "content": message.content,
                "attachments": message.attachments if message.attachments else None,
                "date": datetime.now(),
            }
        )

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        self.cache_msg(message)

    @Cog.listener()
    async def on_message_edit(self, before: Message, message: Message):
        self.cache_msg(before)

    async def cog_command_error(self, ctx: ApplicationContext, err: Exception):
        embed = Embed()
        embed.description = "Nothing to snipe."
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Snipe(bot))
