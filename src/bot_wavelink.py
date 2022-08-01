import wavelink
from discord.ext import commands
import async_spotify

# https://wavelink.readthedocs.io/en/latest/wavelink.html
class BotWavelink(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.player: wavelink.Player = None
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host='localhost',
            port=2333,
            password='youshallnotpass'
        )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        """Track started playing"""
        print(f'Playing: <{track.title}> - <{track.author}> (<{track.duration}>). stream? <{track.is_stream()}> ')
        # guild = ctx.guild
        # voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        # await channel.send('Voice event no canal ' + voiceStateAfter.channel.name)
        # await voiceStateAfter.channel.send('Voice event aqui')

    @commands.command(aliases=['tocar'])
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        """Play a song with the given search query. If not connected, connect to our voice channel."""
        if not ctx.voice_client:
            self.player: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            self.player: wavelink.Player = ctx.voice_client

        await self.player.play(search)

    @commands.command(aliases=['pare', 'pausar', 'parar'])
    async def pause(self, ctx):
        """Pausa o que está sendo tocado"""
        if self.player.is_playing():
            await self.player.pause()

    @commands.command(aliases=['continue', 'continuar'])
    async def resume(self, ctx):
        """Despausa o que está sendo tocado"""
        if self.player.is_paused():
            await self.player.resume()

    @commands.command(aliases=['jumpto','pularpara', 'irpara'])
    async def seek(self, ctx, position: int):
        """Seek to the given position in the song."""
        if self.player.is_connected():
            await self.player.seek(position*1000)

    @commands.command()
    async def stop(self, ctx):
        """Para o que está sendo tocado"""
        if self.player.is_playing() or self.player.is_paused():
            await self.player.stop()

    @commands.command(aliases=['disconnect', 'leave', 'sai'])
    async def dc(self, ctx):
        """Para e disconecta o bot do voice chat"""
        await self.player.disconnect()
        self.player = None

    # https://pypi.org/project/async-spotify/
    @commands.command()
    async def spotify(self, ctx: commands.Context, url: str):
        vc: wavelink.Player = (
            ctx.voice_client
            or await ctx.author.voice.channel.connect(cls=wavelink.Player)
        )

        if decoded := async_spotify.decode_url(url):

            if decoded["type"] is async_spotify.SpotifySearchType.unusable:
                return await ctx.reply(
                    "This Spotify URL is not usable.", ephemeral=True
                )
            elif decoded["type"] in (
                async_spotify.SpotifySearchType.playlist,
                async_spotify.SpotifySearchType.album,
            ):
                async for partial in async_spotify.SpotifyTrack.iterator(
                    query=decoded["id"], partial_tracks=True, type=decoded["type"]
                ):
                    vc.queue.put(partial)
                await vc.play(vc.queue[0])

                return await ctx.reply("Added songs to the queue. (Playlist)")
            else:
                track = await async_spotify.SpotifyTrack.search(
                    query=decoded["id"], return_first=True
                )
                await vc.play(track)


async def setup(bot):
    await bot.add_cog(BotWavelink(bot))