from typing import Set, Callable
import logging

from discord import Message, Member, Bot, Role, TextChannel, Webhook
from discord.ext.commands import Context

from cogs.exceptions import *
from config import Settings


class GagsLogic:
    def __init__(
        self, bot: Bot, gag_role: Role, collision_roles: Set[Role], config: Settings
    ):
        self.config = config
        self.bot = bot
        self.gag_role = gag_role
        self.collision_roles = collision_roles

    async def remove_gag(self, user: Member):
        await user.remove_roles(self.gag_role)

    async def apply_gag(self, ctx: Context, user: Member):
        self._is_gaggable(ctx, user)
        self._is_gagged_precheck(user)
        await user.add_roles(self.gag_role)

    async def async_gaggify(self, message: Message, gag_method):
        if not self._is_gagged(message):
            return

        await message.delete()
        await self._send_with_webhook(
            message.channel, message.author, await gag_method(message.content)
        )

    async def gaggify(self, message: Message, gag_method: Callable[[str], str]):
        if not self._is_gagged(message):
            return
        await message.delete()
        await self._send_with_webhook(
            message.channel, message.author, gag_method(message.content)
        )

    def _is_gagged(self, message: Message) -> bool:
        return (
            not message.author.bot
            and self.gag_role in message.author.roles
            and self._is_channel_watched(message.channel)
        )

    def _is_gagged_precheck(self, user: Member):
        if not self.collision_roles.isdisjoint(set(user.roles)):
            raise UserGaggedAlreadyError(f"{user.mention} 's mouth is already full.")

    def _is_gaggable(self, ctx: Context, user: Member):
        target_roles = {role.id for role in user.roles}
        if (
            self.config.DOM_ROLE in target_roles
            and self.config.SWITCH_ROLE not in target_roles
        ):
            raise InferiorUsingGagError("Trying to gag a superior, are we?")
        elif ctx.author.id == user.id:
            raise SelfGagError("Don't gag yourself...")

    def _get_webhook(self, channel: TextChannel) -> Webhook:
        return self.bot.get_cog("Webhooks").webhooks.get(channel.id)

    def _is_channel_watched(self, channel: TextChannel) -> bool:
        return channel.id in self.bot.get_cog("Webhooks").webhooks

    async def _send_with_webhook(
        self, channel: TextChannel, user: Member, content: str
    ):
        await self._get_webhook(channel).send(
            content=content, username=user.display_name, avatar_url=user.display_avatar
        )
