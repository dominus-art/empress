from discord.ext.commands import CommandError


class SelfGagError(CommandError):
    pass


class InferiorUsingGagError(CommandError):
    pass


class UserGaggedAlreadyError(CommandError):
    pass
