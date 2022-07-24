import discord
import helper_functions
from discord.ext import commands

class BotEvents(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    # Bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        print('------')
        #await setup_hook(self)

    # New message typed
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f'Message from {message.author}: {message.content}')

        if (message.author.bot):
            return

        firstLetter = message.content[0]

        match firstLetter:
            case '!':
                await helper_functions.handleCommand(message)
            case default:
                await helper_functions.handleMessage(message)
                #print(message.channel.id)

    # Event in voice channel (Enter, leave, (un)mute, (un)deafen)
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, voiceStateBefore, voiceStateAfter):
        print('voice event')
        channel = self.bot.get_channel(998764665364566038)
        await channel.send('Voice event no canal ' + voiceStateAfter.channel.name)
        await voiceStateAfter.channel.send('teste')

async def setup(bot):
    await bot.add_cog(BotEvents(bot))