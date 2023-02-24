import random
import re
import validators

from discord import Member, Message, Webhook, Role, ApplicationContext

from discord.ext import commands as cmd
from discord.ext.commands import Cog, Bot, Context


emoji_regex = re.compile(r"<:(.+):(\d+)>")


class Gag(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot: Bot = bot
        self.gag_role: Role

    @cmd.group(name="gag", invoke_without_command=True)
    @cmd.has_any_role("Domme Punishment Perms")
    async def gag(self, ctx: Context, user: Member):
        if not ctx.invoked_subcommand is None:
            return
        try:
            await user.add_roles(self.gag_role)
            await ctx.send(f"Gagged {user.display_name}", delete_after=2)
        except Exception as e:
            await ctx.send(f"Failed to gag {user}: {e}")

    @gag.command(name="addrole")
    @cmd.has_any_role("Admin", "Staff", "Technician")
    async def list(self, ctx: Context, role: Role):
        self.gag_role = role
        await ctx.reply(f"Gag role set: {role}.")

    @cmd.command(name="ungag")
    @cmd.has_any_role("Domme Punishment Perms", "Staff", "Moderator")
    async def ungag(self, ctx: Context, user: Member):
        try:
            await user.remove_roles(self.gag_role)
            await ctx.send(f"Ungaged {user.display_name}", delete_after=2)
        except Exception as e:
            await ctx.send(f"Failed to ungag {user}: {e}")

    async def muffle(self, msg: str) -> str:
        letters = ["m", "m", "m", "m", "h", "ph"]
        ret = ""
        for word in msg.split():
            if validators.url(word):
                word = "link"
            if emoji_regex.search(word):
                word = "emoji"
            for i in word:
                ret += random.choice(letters)
            ret += " "

        return ret

    @Cog.listener()
    async def on_message(self, message: Message):
        if not self.gag_role in message.author.roles:
            return

        webhooks = self.bot.get_cog("Webhooks")
        webhooks = await webhooks.get_webhooks()
        if not message.channel.id in webhooks:
            return

        await message.delete()
        webhook: Webhook = webhooks[message.channel.id]
        await webhook.send(
            content=await self.muffle(message.content),
            username=message.author.display_name,
            avatar_url=message.author.display_avatar,
        )

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)


def setup(bot: Bot):
    bot.add_cog(Gag(bot))
