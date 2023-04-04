import discord
from discord.ext import commands, tasks
import random
import asyncio
import bot_http_requests
import helper_functions

class BotCommands(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.canal_atual = 0
        self.counter_agua = 0

    @commands.command()
    async def alundra(self,ctx):
        """That's me!"""
        await helper_functions.replyWithMyImage(ctx.message)

    @commands.command()
    async def google(self, ctx, query: str = None):
        """Google something."""
        if (not query):
            return await ctx.message.reply('Type "!google <something interesting>" to search it')
        async with ctx.message.channel.typing():
            await asyncio.sleep(1)
        result = bot_http_requests.google_search(query)
        await ctx.message.reply('\n'.join(str(link) for link in result))

    @commands.command(aliases=['gato', 'gatinho', 'kitty'])
    async def cat(self,ctx):
        """Get a random cat image."""
        async with ctx.typing():
            await asyncio.sleep(1)
        jsn = await bot_http_requests.cat_search()
        await ctx.send(jsn['file'])
    
    @commands.command(aliases=['cachorro'])
    async def dog(self, ctx, raca: str = None):
        """Get a random dog image."""
        async with ctx.typing():
            await asyncio.sleep(1)
        jsn = await bot_http_requests.dog_search(raca)
        await ctx.send(jsn['message'])

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send(left + right)

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))


    @commands.command()
    async def repeat(self, ctx, times: int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times):
            await ctx.send(content)


    @commands.command()
    async def joined(self, ctx, member: discord.Member = None):
        """Says when a member joined."""
        if member is None:
            member = ctx.author
        await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

    @commands.command()
    async def meme(self, ctx):
        """Get a random meme from a subreddit of your choice."""
        (command, arguments) = helper_functions.splitCommandFromArguments(ctx.message)
        async with ctx.message.channel.typing():
            await asyncio.sleep(1)
        jsn = await bot_http_requests.meme_search(1,arguments[0])
        await ctx.message.reply(jsn['url'])

    @commands.command()
    async def elo(self, ctx):
        """Check someone's elo in League of legends."""
        (command, arguments) = helper_functions.splitCommandFromArguments(ctx.message)
        async with ctx.message.channel.typing():
            await asyncio.sleep(1)
        if (len(arguments) >= 2):
            jsn = await bot_http_requests.elo(summoner_name=arguments[0],region=arguments[1])
        elif (len(arguments) == 1):
            jsn = await bot_http_requests.elo(summoner_name=arguments[0])
        else:
            await ctx.message.reply("Use !elo <summoner_name> <region>")
        laugh = ""
        if (jsn[0]["tier"] == "Bronze" or jsn[0]["tier"] == "Iron"):
            laugh = " KKKKKKKKKKK"
        await ctx.message.reply(jsn[0]['tier'] + " " + jsn[0]["rank"] + laugh)

    @commands.group()
    async def cool(self, ctx):
        """Says if a user is cool.In reality this just checks if a subcommand is being invoked."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

    @cool.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')

    @commands.command(description='Ativa o lembrete para beber água a cada 20 minutos')
    async def agua(self, ctx):
        """Turns on a reminder to drink water every 20 minutes."""
        await ctx.send('Reminder set to every 20 minutes.')
        self.canal_atual = ctx.channel.id
        self.bebam_agua.start()

    @tasks.loop(seconds=1200)
    async def bebam_agua(self):
        channel = self.bot.get_channel(self.canal_atual)
        self.counter_agua += 1
        await channel.send("Drink water! (" + str(self.counter_agua) + ")")


async def setup(bot):
    await bot.add_cog(BotCommands(bot))