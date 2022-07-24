import discord
from discord.ext import commands
import asyncio
import env

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix='!',
    description="Alundra Bot",
    intents=intents
)

extensions = [
    'bot_events',
    'bot_tasks',
    'bot_commands',
    'bot_voice'
]

async def main():
    async with bot:
        for extension in extensions:
            await bot.load_extension(extension)
        await bot.start(env.botkey)

asyncio.run(main())
