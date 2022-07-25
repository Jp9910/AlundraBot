# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands, tasks
import random

class BotCommands(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.canal_atual = 0
        self.counter_agua = 0

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
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


    @commands.group()
    async def cool(self, ctx):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


    @cool.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')

    @commands.command(description='Ativa o lembrete para beber água a cada 20 minutos')
    async def agua(self, ctx):
        await ctx.send('Lembrete definido para cada 20 minutos.')
        self.canal_atual = ctx.channel.id
        self.bebam_agua.start()

    @tasks.loop(seconds=1200)
    async def bebam_agua(self):
        channel = self.bot.get_channel(self.canal_atual)
        self.counter_agua += 1
        await channel.send("Bebam água! (" + str(self.counter_agua) + ")")
        


async def setup(bot):
    await bot.add_cog(BotCommands(bot))