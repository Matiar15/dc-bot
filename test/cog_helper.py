from discord import User, Member


def user_to_str(author: User | Member) -> tuple[str]:
    r'''Gets the author of the message and changes it into a tuple.
    
        Parameters
        -----------
        author: :class:`discord.User` | :class:`discord.Member`
            Author of the message.
        
        Returns
        -----------
        author_tpl: :class:`tuple[str]`
            One-element tuple contating author str.
        '''
    author_str: str = str(author)
    author_tpl: tuple[str] = (author_str,)
    return author_tpl
