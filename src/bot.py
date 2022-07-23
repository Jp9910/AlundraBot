import discord
from discord.ext import tasks
from helper_functions import *
import env
#import voice_bot_example

class MyClient(discord.Client):

    def __init__(self, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.counter = 0

    # Bot is ready
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        #await self.setup_hook()

    # New message typed
    async def on_message(self, message):
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
    async def on_voice_state_update(self, member, voiceStateBefore, voiceStateAfter):
        print('voice event')
        channel = self.get_channel(998764665364566038)
        await channel.send('Voice event no canal ' + voiceStateAfter.channel.name)
        await voiceStateAfter.channel.send('teste')


    # A new setup_hook() method has also been added to the Client class. 
    # This method is called after login but before connecting to the discord gateway.
    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    @tasks.loop(seconds=2.0, count=1)  # task runs every 2.0 seconds, 3 times
    async def my_background_task(self):
        channel = self.get_channel(998764665364566038)  # channel ID goes here
        self.counter += 1
        await channel.send(self.counter)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(env.botkey)

#print(vars(self.commandHandler))
#print(self.commandHandler.__dict__)
# from pprint import pprint; # pprint(self.commandHandler)