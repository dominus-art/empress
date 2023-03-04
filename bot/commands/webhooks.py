from typing import Dict, List, Optional

from discord.ext.commands import Context, Cog, Bot, Greedy
from discord.ext import commands as cmd
from discord import TextChannel, Embed, EmbedField, Colour, ApplicationContext, Webhook


class Webhooks(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.webhooks: Dict[str, Webhook] = {}
        self.webhooks_channel_names: List[str] = []

    def _embed_channel_names(self) -> List[EmbedField]:
        channels_str = ""
        for channel in self.webhooks_channel_names:
            channels_str += f"{channel}\n"
        return Embed(
            title="Webhooks:",
            fields=[EmbedField("Channels:", channels_str)],
            colour=Colour.dark_blue(),
        )

    @cmd.group(name="webhooks")
    @cmd.has_any_role("Admin", "Technician", "Staff")
    async def webhooks(self, ctx: Context):
        pass

    @webhooks.commands(name="sync")
    @cmd.has_any_role("Admin", "Technician", "Staff")
    async def sync(self, ctx: Context):
        webhooks: List[Webhook] = await ctx.guild.webhooks()
        self.webhooks = {webhook.channel_id: webhook for webhook in webhooks}
        await ctx.reply(self._embed_channel_names())

    @webhooks.command(name="addchannels")
    @cmd.has_any_role("Admin", "Technician", "Staff")
    async def addchannels(self, ctx: Context, channels: Greedy[TextChannel]):
        self.webhooks.update(
            {
                channel.id: await channel.create_webhook(name=f"webhook{channel.id}")
                for channel in channels
            }
        )
        self.webhooks_channel_names.extend([channel.name for channel in channels])
        await ctx.reply(embed=self._embed_channel_names())

    @webhooks.command(name="removechannels")
    @cmd.has_any_role("Admin", "Technician", "Staff")
    async def removechannel(
        self, ctx: Context, channels: Greedy[TextChannel], reason: Optional[str]
    ):
        reason = reason if reason else "No reason provided."
        for channel in channels:
            await self.webhooks[channel.id].delete()
            del self.webhooks[channel.id]
            self.webhooks_channel_names.remove(channel.name)

        await ctx.reply(embed=self._embed_channel_names())

    @webhooks.command(name="ls")
    @cmd.has_any_role("Admin", "Technician", "Staff")
    async def ls(self, ctx: Context):
        await ctx.reply(embed=self._embed_channel_names())

    async def get_webhooks(self) -> Dict[str, TextChannel]:
        return self.webhooks.copy()

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)


def setup(bot: Bot):
    bot.add_cog(Webhooks(bot))
