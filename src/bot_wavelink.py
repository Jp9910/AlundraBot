import wavelink
from discord.ext import commands
import async_spotify
import discord

# https://wavelink.readthedocs.io/en/latest/wavelink.html
class BotWavelink(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.player: wavelink.Player = None
        self.track: wavelink.Track = None
        self.spotify_player: wavelink.Player = None
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host='wavelink',
            port=2333,
            password='youshallnotpass'
        )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')
    
    @commands.Cog.listener()
    async def on_wavelink_websocket_closed(player: wavelink.Player, reason, code):
        """Called when the Node websocket has been closed by Lavalink."""
        print(f'Websocket closed. Reason: <{reason}>. Code: <{code}>')

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        """Track started playing"""
        self.track = track
        print(f'Playing: <{track.title}> - <{track.author}> (<{track.duration}>). stream? <{track.is_stream()}> ')
        # guild = ctx.guild
        # voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
        # await channel.send('Voice event no canal ' + voiceStateAfter.channel.name)
        # await voiceStateAfter.channel.send('Voice event aqui')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        if self.player is None:
            return await ctx.send("Not connected to a voice channel.")
        await self.player.set_volume(volume)
        await ctx.send(f"Changed volume to {volume}%/1000")

    @commands.command(aliases=['tocar'])
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        """Play a song with the given search query. (Connects to your voice channel)"""
        if not ctx.voice_client:
            self.player: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            self.player: wavelink.Player = ctx.voice_client

        await self.player.play(search)

    @commands.command(aliases=['pare', 'pausar', 'parar'])
    async def pause(self, ctx):
        """Pauses song being played"""
        if self.player.is_playing():
            await self.player.pause()

    @commands.command(aliases=['continue', 'continuar'])
    async def resume(self, ctx):
        """Unpauses song being played"""
        if self.player.is_paused():
            await self.player.resume()

    @commands.command(aliases=['jumpto','pularpara', 'irpara'])
    async def seek(self, ctx, position: int):
        """Seek to the given position in the song."""
        if self.player.is_connected():
            await self.player.seek(position*1000)

    @commands.command()
    async def stop(self, ctx):
        """Stops currently playing song"""
        if self.player.is_playing() or self.player.is_paused():
            await self.player.stop()

    @commands.command(aliases=['disconnect', 'leave', 'sai'])
    async def dc(self, ctx):
        """Stops and disconnects the bot from the voice chat"""
        await self.player.disconnect()
        self.player = None

    @commands.command(aliases=['mover', 'venhapara', 'vapara', 'moveto'])
    async def move_to(self, ctx, *, channel: discord.VoiceChannel = None):
        """Move bot to another channel"""
        if self.player:
            await self.player.move_to(channel)

    @commands.command(alises=['tocando'])
    async def playing(self, ctx):
        """Show currently playing song"""
        if self.track:
            await ctx.send(f'Playing: {self.track.title} - {self.track.author}. Duration: ({self.track.duration}) seconds. Source: <{self.track.uri}> Streaming? {self.track.is_stream()}')

    # https://pypi.org/project/async-spotify/
    @commands.command()
    async def spotify(self, ctx: commands.Context, url: str):
        """Plays from spotify (wip)"""
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