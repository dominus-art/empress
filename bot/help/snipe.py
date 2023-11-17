from config import get_settings
prefix = get_settings().PREFIX
cache = get_settings().SNIPE_CACHE_SIZE
SNIPE = f"""
        Bring back deleted or edited message. Last {cache} messages are kept.
        Command arguments:
        - index: how far back to look in saved messages
        
        Example usage:
        `{prefix}s 3`
        `{prefix}snipe`"""
ADD = """
        Add channels where sniping should work."""
REMOVE = """
        Remove channels where sniping should no longer work."""
