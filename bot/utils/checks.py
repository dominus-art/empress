from typing import Callable, TypeVar

from discord.ext import commands as cmd
from discord.ext.commands import Context, CheckFailure

from config import get_settings

T = TypeVar("T")


def is_techpriest() -> Callable[[T], T]:
    async def predicate(cxt: Context) -> bool:
        if not get_settings().TECH_ROLE in [role.id for role in cxt.author.roles]:
            raise CheckFailure("You're not permitted to perform this action")

        return True

    return cmd.check(predicate)


def is_mod() -> Callable[[T], T]:
    async def predicate(ctx: Context) -> bool:
        admin_roles = set(get_settings().ADMIN_ROLES)
        author_roles = set([role.id for role in ctx.author.roles])
        if author_roles.isdisjoint(admin_roles):
            raise CheckFailure("You're not permitted to perform this action")

        return True

    return cmd.check(predicate)


def is_maintainer() -> Callable[[T], T]:
    async def predicate(ctx: Context) -> bool:
        admin_roles = set([*get_settings().ADMIN_ROLES, get_settings().TECH_ROLE])
        author_roles = set([role.id for role in ctx.author.roles])
        if author_roles.isdisjoint(admin_roles):
            raise CheckFailure("You're not permitted to perform this action")
        return True

    return cmd.check(predicate)


def can_have_fun() -> Callable[[T], T]:
    async def predicate(ctx: Context) -> bool:
        fun_roles = set([get_settings().DOM_ROLE])
        author_roles = set([role.id for role in ctx.author.roles])
        if author_roles.isdisjoint(fun_roles):
            raise CheckFailure("No.")
        return True

    return cmd.check(predicate)


def is_trusted_member() -> Callable[[T], T]:
    async def predicate(ctx: Context) -> bool:
        trusted_member_roles = set(
            [*get_settings().ADMIN_ROLES, get_settings().TECH_ROLE]
        )
        author_roles = set([role.id for role in ctx.author.roles])
        if author_roles.isdisjoint(trusted_member_roles):
            raise CheckFailure(
                "You're not a trusted member and thus cannot use this command."
            )
        return True

    return cmd.check(predicate)


def can_ungag() -> Callable[[T], T]:
    async def predicate(ctx: Context) -> bool:
        ungag_roles = set(*get_settings().ADMIN_ROLES, get_settings().DOM_ROLE)
        author_roles = set(role.id for role in ctx.author.roles)
        if author_roles.isdisjoint(ungag_roles):
            raise CheckFailure("You're not allowed to ungag anyone.")
        return True

    return cmd.check(predicate)
