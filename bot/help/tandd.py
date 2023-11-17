from config import get_settings

prefix = get_settings().PREFIX

CREATE: str = f"""
        Create new truth or dare.
        Command arguments:
        - rating: can be PG for sfw or R for nsfw
        - content: text for truth or dare you're creating
        
        Example usage:
        `{prefix}truth create PG Have you ever stolen something?`
        `{prefix}truth create R Did you ever participated in an orgy?`
        `{prefix}dare create PG Call your mom, she misses you."""