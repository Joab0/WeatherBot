import logging
import discord

from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands

from bot import BotCore


from utils.translator import Translator


log = logging.getLogger(__name__)


class Misc(commands.Cog):
    def __init__(self, bot: BotCore) -> None:
        self.bot: BotCore = bot

    def _get_latency_emoji(self, latency: int) -> str:
        return '🟢' if latency < 100 else '🟡' if latency < 200 else '🔴'

    def _get_latency_color(self, latency: int) -> discord.Colour:
        if latency < 100:
            return discord.Colour.green()
        elif latency < 200:
            return discord.Colour.yellow()
        else:
            return discord.Colour.red()

    @app_commands.command(
        name=_T('ping', id='commands.ping.name'),
        description=_T('...', id='commands.ping.description')
    )
    async def ping(self, interaction: discord.Interaction):
        t = Translator(interaction.locale)

        latency = round(self.bot.latency * 1000)

        e = self._get_latency_emoji(latency) + ' '

        embed = discord.Embed(
            title='🏓 ' + t('commands.ping.pong'),
            description=e + t('commands.ping.response', latency=f'`{latency}ms`'),
            color=self._get_latency_color(latency)
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot:  BotCore) -> None:
    await bot.add_cog(Misc(bot))
