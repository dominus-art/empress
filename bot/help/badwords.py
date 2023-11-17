from config import get_settings

prefix = get_settings().PREFIX

ADD = f"""
            Add forbidden words to the list.
            Command arguments:
            - <user>: user id or @user
            - lives: optional number, defaults to 3 if not specified. If user had lives set already this is ignored.
            - words: words separated by a space, case sensitive
            
            Example usage:
            `{prefix}badword add @user 5 Napoleon napoleon Milk nun`"""
REMOVE = f"""
            Remove forbiden word(s) from the list.
            Command arguments:
            - <user>: user id or @user
            - <words>: words separated by a space, case sensitive
            
            Example usage:
            `{prefix}badword remove @user Napoleon`
            """
CLEAR = f"""
            Remove all forbidden words from the list.
            Command arguments:
            - <user>: user id or @user

            Example usage:
            `{prefix}badwords clear @user`
            """
LIST = f"""
        Lists all forbidden words for a user. If user is not specified lists all forbidden words for the callee(you)."""
