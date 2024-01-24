from config import get_settings

prefix = get_settings().PREFIX


UWU: str = f"""
        Apply uwufing gag to the user.
        Example usage:
        `{prefix}gag uwu @user`"""
BALL: str = f"""
        Apply ball gag to the user.
        Example usage:
        `{prefix}gag ball @user`"""
UNGAG: str = f"""
        Remove gag from the user."""

GAG = f"""Invoke `{prefix}help gag uwu` or `{prefix}help gag ball` for more information."""

NEW_UWU: str = f"""
        Apply uwufing gag to the user.
        Example usage:
        `{prefix}uwu @user`
        `{prefix}gag-uwu @user`"""

NEW_BALL: str = f"""
        Apply ball gag to the user.
        Example usage:
        `{prefix}ball @user`
        `{prefix}gag-ball @user`"""

NEW_KITTY: str = f"""
        Apply ball gag to the user.
        Example usage:
        `{prefix}kitty @user`
        `{prefix}gag-kitty @user`"""
