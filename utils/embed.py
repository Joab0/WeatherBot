import discord


SUCCESS_EMOJI = '✅'
ERROR_EMOJI = '❌'


class Embed:
    def __init__(self) -> None:
        pass

    @staticmethod
    def success(msg: str, **kwargs) -> discord.Embed:
        return discord.Embed(
            description=SUCCESS_EMOJI + ' ' + msg,
            color=discord.Colour.brand_green(),
            **kwargs
        )

    @staticmethod
    def error(msg: str, **kwargs) -> discord.Embed:
        return discord.Embed(
            description=ERROR_EMOJI + ' ' + msg,
            color=discord.Colour.brand_red(),
            **kwargs
        )
