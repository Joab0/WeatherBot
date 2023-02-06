import os
import asyncio
import discord

from bot import BotCore

from dotenv import load_dotenv


load_dotenv()

discord.utils.setup_logging()


async def main():
    async with BotCore(
        test_guild_id=os.getenv('TEST_GUILD_ID')
    ) as bot:
        await bot.start(os.getenv('DISCORD_BOT_TOKEN'))

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
