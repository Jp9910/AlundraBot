from imaplib import Commands
import discord
from helper_functions import *
from discord.ext import commands
import env
import voice_bot
import bot_tasks

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix='!',
    description="Alundra Bot",
    intents=intents
)

# Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    #await setup_hook(self)

# New message typed
@bot.event
async def on_message(message: discord.Message):
    print(f'Message from {message.author}: {message.content}')

    if (message.author.bot):
        return

    firstLetter = message.content[0]

    match firstLetter:
        case '!':
            await handleCommand(message)
        case default:
            await handleMessage(message)
            #print(message.channel.id)

# Event in voice channel (Enter, leave, (un)mute, (un)deafen)
@bot.event
async def on_voice_state_update(member, voiceStateBefore, voiceStateAfter):
    print('voice event')
    channel = bot.get_channel(998764665364566038)
    await channel.send('Voice event no canal ' + voiceStateAfter.channel.name)
    await voiceStateAfter.channel.send('teste')

#print(vars(self.commandHandler))
#print(self.commandHandler.__dict__)
# from pprint import pprint; # pprint(self.commandHandler)


bot.run(env.botkey)