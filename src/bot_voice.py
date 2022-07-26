import asyncio
import discord
import youtube_dl
from discord import FFmpegPCMAudio
from discord.ext import commands
import wavelink

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

# @TODO: Upgrade to Wavelink (https://github.com/PythonistaGuild/Wavelink)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class BotVoice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['entre', 'cheguemais'])
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Joins a voice channel"""
        # ctx.voice_client é o nome do canal do bot

        if ((ctx.message.author.voice is not None) and (channel is None)): #"!join"
            channel = ctx.message.author.voice.channel
            if (ctx.voice_client is not None):
                return await ctx.voice_client.move_to(channel) #se o bot já está em um canal, ele move para outro
            else:
                await channel.connect() #se o bot ainda não está um canal, conecta

        #autor não está em um canal de voz ou especificou um canal de voz
        else:
            if ((ctx.voice_client is not None) and (channel is not None)):
                return await ctx.voice_client.move_to(channel) #se o bot já está em um canal, ele move para outro
            elif (channel is not None):
                await channel.connect() #se o bot ainda não está um canal, conecta
            else:
                await ctx.message.reply("Entre em um canal de voz ou especifique o nome do canal.") # não especificou o canal e não está em nenhum canal
        

    # @commands.command()
    # async def play(self, ctx, *, query):
    #     """Plays a file from the local filesystem"""
    #
    #     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #     ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
    #
    #     await ctx.send(f'Now playing: {query}')

    # @commands.command()
    # async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    #     """Play a song with the given search query.
    #
    #     If not connected, connect to our voice channel.
    #     """
    #     if not ctx.voice_client:
    #         vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    #     else:
    #         vc: wavelink.Player = ctx.voice_client
    #
    #     await vc.play(search)
    #     await ctx.send(f'Now playing: {search}')


    @commands.command()
    async def chaves(self, ctx):
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        audio_source = discord.FFmpegPCMAudio('chaves.wav')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            await ctx.send(f'Now playing: chaves')
            voice_client.pause()
            await asyncio.sleep(2)
            voice_client.resume()
        # if (ctx.author.voice):
        #     channel = ctx.message.author.voice.channel
        #     voice = await channel.connect()
        #     source = FFmpegPCMAudio('chaves.wav')
        #     player = voice.play(source)
        # else:
        #     await ctx.send("enter a channel first")

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

async def setup(bot):
    await bot.add_cog(BotVoice(bot))