import discord
from discord.ext import commands
import asyncio
import env

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix='!',
    description="Alundra Bot",
    intents=intents
)

extensions = [
    'bot_events',
    'bot_tasks'
]

async def main():
    async with bot:
        for extension in extensions:
            await bot.load_extension(extension)
        await bot.start(env.botkey)

asyncio.run(main())
