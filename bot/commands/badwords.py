from discord import Member, Message, Role, ApplicationContext
from discord.ext import commands as cmd
from discord.ext.commands import Context, Cog, Bot


class Badwords(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot: Bot = bot
        self.badword_role: Role

    @cmd.group(name="badword")
    async def badword(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("ERROR")

    @badword.command(name="addrole")
    @cmd.has_any_role("Staff", "Technician", "Admin")
    async def addrole(self, ctx: Context, role: Role):
        self.badword_role = role
        await ctx.send(f"Badword role set [{role}]")

    @badword.command(name="add")
    @cmd.has_any_role("Domme Punishment Perms", "Staff", "Admin")
    async def add(self, ctx: Context, user: Member, *, words: str):
        badwords = [word.strip().replace(",", "") for word in words.split()]
        await ctx.send(f"{user} | {badwords}")

    @badword.command(name="remove")
    @cmd.has_any_role("Domme Punishment Perms", "Staff", "Admin")
    async def remove(self, ctx: Context, user: Member, *, words: str):
        pass

    @badword.command(name="clear")
    @cmd.has_any_role("Domme Punishment Perms", "Staff", "Admin")
    async def clear(self, ctx: Context, user: Member):
        pass

    @badword.command(name="list")
    async def list(self, ctx: Context, user: Member):
        pass

    @Cog.listener()
    async def on_message(self, message: Message):
        if self.badword_role in message.author.roles:
            return
        webhooks = self.bot.get_cog("Webhooks")
        webhooks = await webhooks.get_webhooks()
        if message.channel not in webhooks:
            return

    async def cog_command_error(
        self, ctx: ApplicationContext, error: Exception
    ) -> None:
        await ctx.send(error)


def setup(bot: Bot):
    bot.add_cog(Badwords(bot))
