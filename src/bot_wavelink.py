import wavelink
from discord.ext import commands
import async_spotify

# https://wavelink.readthedocs.io/en/latest/wavelink.html
class BotWavelink(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='localhost',
                                            port=2333,
                                            password='youshallnotpass')

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        """Play a song with the given search query.

        If not connected, connect to our voice channel.
        """
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.play(search)

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