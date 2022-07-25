import discord
from discord.ext import commands
from discord.ext import tasks

class BotTasks(commands.Cog):

    def __init__(self, bot) -> None:
        bot.setup_hook = self.setup_hook
        self.bot = bot
        self.counter = 0

    # A new setup_hook() method has also been added to the Client class. 
    # This method is called after login but before connecting to the discord gateway.
    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    @tasks.loop(seconds=1200)  # task runs every 2.0 seconds, 3 times @tasks.loop(seconds=2.0, count=3)
    async def my_background_task(self): #testar self.bot.guilds
        return
        guilds = self.bot.guilds
        all_channels = self.bot.get_all_channels()
        channel = discord.utils.get(all_channels, name='general')
        #channel = self.bot.get_channel(998764665364566038)  # channel ID goes here
        self.counter += 1
        await channel.send("Bebam água! (" + str(self.counter) + ")")

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()  # wait until the bot logs in

async def setup(bot):
    await bot.add_cog(BotTasks(bot))