import aiohttp
import discord
import logging

from discord.ext import commands

from utils.translator import CommandTranslator, Translator


log = logging.getLogger(__name__)


INITIAL_EXTENSIONS = (
    'cogs.weather',
    'cogs.error_handler',
    'cogs.misc',
)


Translator.load_locales('./locales')


class BotCore(commands.Bot):
    def __init__(self, test_guild_id: int | None = None) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned,
            help_command=None,
            intents=discord.Intents.default()
        )
        self.test_guild_id: int | None = None

        if test_guild_id:
            self.test_guild_id = int(test_guild_id)
            log.setLevel(logging.DEBUG)
            log.debug('Running in the development version')

    async def on_ready(self) -> None:
        assert self.user is not None
        log.info(f'Connected in: {self.user} ({self.user.id})')

    async def setup_hook(self) -> None:
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()

        await self.tree.set_translator(CommandTranslator())

        for ext in INITIAL_EXTENSIONS:
            await self.load_extension(ext)
            log.info(f'Extension {ext} loaded successfully')

        if self.test_guild_id:
            test_guild = discord.Object(id=self.test_guild_id)
            self.tree.copy_global_to(guild=test_guild)
            log.debug(f'Syncing commands on: {test_guild.id}')
            await self.tree.sync(guild=test_guild)
        else:
            await self.tree.sync()
        log.info('Synchronized commands')

    async def close(self) -> None:
        await self.session.close()
        return await super().close()
