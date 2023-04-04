import discord
from discord.ext import commands
import asyncio
import env

class Bot(commands.Bot):

    def __init__(self, intents):
        super().__init__(
            command_prefix='!',
            description="Alundra Bot",
            intents=intents
        )

    # Eventos acumulam, não sobreescrevem,
    async def on_ready(self):
        print('Bot is ready!')

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

extensions = [
    'bot_events',
    'bot_tasks',
    'bot_commands',
    'bot_voice',
    'bot_wavelink'
]

bot = Bot(intents=intents)
async def main():
    async with bot:
        for extension in extensions:
            await bot.load_extension(extension)
        await bot.start(env.botkey)

asyncio.run(main())

# TODO: Avisar sobre evento de saída do servidor