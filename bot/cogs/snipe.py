from datetime import datetime
from collections import deque
from typing import Optional

from discord import Embed, Color, Message, TextChannel
from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context, Greedy

from config import get_settings
from utils.checks import is_maintainer


class Snipe(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot
        self.cache = deque(maxlen=get_settings().SNIPE_CACHE_SIZE)
        self.snipe_channels = set()
        self.snipe_channel_names = set()

    @cmd.group(name="s", invoke_without_command=True, aliases=["snipe", "sniper"])
    async def snipe(self, ctx: Context, index: Optional[int] = 1):
        i = index - 1
        cached_msg = self.cache[i]
        embed = Embed()
        embed.add_field(name="", value=cached_msg["content"])
        embed.timestamp = cached_msg["date"]
        embed.set_author(name=cached_msg["author"], icon_url=cached_msg["icon"])
        await ctx.send(embed=embed)

    @snipe.command(name="add")
    @is_maintainer()
    async def add(self, ctx: Context, channels: Greedy[TextChannel]):
        embed = Embed(color=Color.dark_gold()).set_author(
            name=ctx.author.mention, icon_url=ctx.author.display_avatar
        )
        for channel in channels:
            self.snipe_channels.add(channel.id)
            self.snipe_channel_names.add(channel.name)
        embed.add_field(
            name="Watching channels:", value="\n".join(self.snipe_channel_names)
        )
        await ctx.reply(embed=embed)

    @snipe.command(name="remove")
    @is_maintainer()
    async def remove(self, ctx: Context, channels: Greedy[TextChannel]):
        embed = Embed().set_author(
            name=ctx.author.mention, icon_url=ctx.author.display_avatar
        )
        actions = []
        for channel in channels:
            self.snipe_channels.remove(channel.id)
            self.snipe_channel_names.remove(channel.name)
            actions.append(f"removed {channel.name}")

        embed.add_field(name="Report:", value="\n".join(actions))
        await ctx.reply(embed=embed)

    @snipe.command(name="dbg")
    @is_maintainer()
    async def dbg(self, ctx: Context):
        embed = (
            Embed()
            .set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar
            )
            .add_field(name="channels", value="\n".join(self.snipe_channel_names))
        )
        await ctx.reply(embed=embed)

    @Cog.listener()
    async def on_message(self, message: Message):
        if (
            message.author.bot
            or not message.channel.id in self.snipe_channels
            or message.content.startswith(get_settings().PREFIX)
        ):
            return

        self.cache.appendleft(
            {
                "author": f"{message.author.display_name}\n({message.author.id})",
                "icon": message.author.display_avatar,
                "content": message.content,
                "date": datetime.now(),
            }
        )


def setup(bot: Bot):
    bot.add_cog(Snipe(bot))
