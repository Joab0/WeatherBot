import logging
import discord
from discord.ext import commands
from discord.app_commands.errors import (
    AppCommandError,
    CommandOnCooldown
)

from bot import BotCore


from utils.translator import Translator
from utils.embed import Embed


log = logging.getLogger(__name__)


class ErrorHandler(commands.Cog):
    def __init__(self, bot: BotCore) -> None:
        self.bot: BotCore = bot
        self.bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: AppCommandError
    ) -> None:
        t = Translator(interaction.locale)
        match error:
            case CommandOnCooldown():
                embed = Embed.error(
                    t('errors.command_on_cooldown', retry_after=f'{error.retry_after:.2f}')
                )
            case _:
                log.error('Command error', exc_info=error)
                embed = Embed.error(
                    t('errors.exec_error', error=error)
                )
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot:  BotCore) -> None:
    await bot.add_cog(ErrorHandler(bot))
