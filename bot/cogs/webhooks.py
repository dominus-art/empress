from typing import Dict

from discord.ext.commands import Context, Cog, Bot, Greedy
from discord.ext import commands as cmd
from discord import TextChannel, Embed, Color, ApplicationContext, Webhook

from utils.checks import is_maintainer, is_techpriest


def filled_embed(ctx: Context) -> Embed:
    return Embed(
        description=ctx.author.name, url=ctx.author.avatar, color=Color.dark_blue()
    )


class Webhooks(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.webhooks: Dict[str, Webhook] = {}

    @cmd.group(name="webhooks")
    @is_maintainer()
    async def webhooks(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return

    @webhooks.command(name="add")
    @is_maintainer()
    async def add(self, ctx: Context, channels: Greedy[TextChannel]):
        embed = Embed(description=ctx.author.name, color=Color.dark_blue())

        tmp: Dict[str, Webhook] = {}
        actions = []
        for channel in channels:
            try:
                tmp[channel.id] = await channel.create_webhook(
                    name=f"empress{channel.id}"
                )
                actions.append(f"created {channel.name}")
            except Exception as e:
                actions.append(f"{channel.name} failed: {e}")

        if tmp:
            self.webhooks.update(tmp)
            actions.append("updated webhooks object")

        embed.add_field(name="Action log:", value="\n".join(actions))
        await ctx.reply(embed=embed)

    @webhooks.command(name="delete")
    @is_maintainer()
    async def delete(self, ctx: Context, channels: Greedy[TextChannel]):
        embed = Embed(description=ctx.author.name, color=Color.dark_blue())
        actions = []
        for channel in channels:
            for webhook in await ctx.guild.get_channel(channel.id).webhooks():
                try:
                    actions.append(f"{webhook.channel.name} deleted")
                    del self.webhooks[channel.id]
                    await webhook.delete()
                except Exception as e:
                    actions.append(f"{webhook.channel.name} failed: {e}")

        embed.add_field(name="Action log:", value="\n".join(actions))
        await ctx.send(embed=embed)

    @webhooks.command(name="ls")
    @is_maintainer()
    async def ls(self, ctx: Context):
        embed = Embed(description=ctx.author.name, color=Color.dark_blue()).add_field(
            name="Channels with webhooks:",
            value="\n".join(
                webhook.channel.name for _, webhook in self.webhooks.items()
            ),
        )
        await ctx.reply(embed=embed)

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)

    @webhooks.command(name="sync")
    @is_techpriest()
    async def sync_wh(self, ctx: Context):
        embed = Embed(description=ctx.author.name, color=Color.dark_blue())
        self.webhooks = {
            webhook.channel.id: webhook
            for webhook in await ctx.guild.webhooks()
            if webhook.name.startswith("empress")
        }
        embed.add_field(
            name="Synced webhooks:",
            value="\n".join(
                webhook.channel.name for _, webhook in self.webhooks.items()
            ),
        )
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Webhooks(bot))
