import discord
from discord.ext import tasks
from helper_functions import *
import env

class MyClient(discord.Client):

    def __init__(self, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.counter = 0

    # Bot is ready
    async def on_ready(self):
        print('Logged on as', self.user)

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

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    @tasks.loop(seconds=10)  # task runs every 10 seconds
    async def my_background_task(self):
        channel = self.get_channel(998764665364566038)  # channel ID goes here
        self.counter += 1
        await channel.send(self.counter)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

        

intents = discord.Intents.default()

client = MyClient(intents=intents)
client.run(env.botkey)

#print(vars(self.commandHandler))
#print(self.commandHandler.__dict__)
# from pprint import pprint; # pprint(self.commandHandler)