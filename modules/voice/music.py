from enum import Enum

from discord.ext import commands

from core.music.MediaFile import MediaFile
from core.music.Mixer import Mixer
from core.music.Source import Source
from core.music.providers.direct import DirectProvider
from core.music.providers.nicovideo import NicovideoProvider
from core.music.providers.youtube import YoutubeProvider


class PlayStatus(Enum):
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2


class RepeatMode(Enum):
    NORMAL = 0
    REPEAT_ONE = 1
    REPEAT_ALL = 2

providers = {
    "youtube": YoutubeProvider(),
    "nicovideo": NicovideoProvider(),
    "direct": DirectProvider()
}

class Music(commands.Cog):
    # A List of MediaFile objects, initially empty
    song_queue = [
        MediaFile('https://www.youtube.com/watch?v=9SKA6PmcLuQ', provider=providers['youtube']),
    ]

    current_song_index = 0
    play_status = PlayStatus.STOPPED
    repeat_mode = RepeatMode.REPEAT_ALL

    prepare_task = None
    mixer = Mixer()

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx):
        self.play_status = PlayStatus.PLAYING

        source = Source(self.song_queue[self.current_song_index])
        await source.prepare()
        # todo: get song duration here and start task
        self.mixer.set_source(source)
        ctx.voice_client.play(self.mixer)

    @commands.command()
    async def pause(self, ctx):
        pass

    @commands.command()
    async def seek(self, ctx):
        pass

    @commands.command()
    async def stop(self, ctx):
        self._stop()
        ctx.voice_client.stop()

    @commands.command()
    async def next(self, ctx):
        await self._play_next()

    @commands.command()
    async def previous(self, ctx):
        pass

    @commands.command()
    async def remove(self, ctx):
        pass

    @commands.command()
    async def move(self, ctx):
        pass

    @commands.command()
    async def shuffle(self, ctx):
        """ Shuffles the queue and places the current song first, if one is playing"""
        pass

    @commands.command()
    async def repeat(self, ctx):
        """ Toggles between repetition of one song, of the whole queue, and disabling repeat
        :param ctx: discord.py context
        """
        pass

    @commands.command()
    async def queue(self, ctx):
        """ Shows the current queue"""
        pass

    @commands.command()
    async def search(self, ctx, provider_arg: str = None, *, arg):
        """ Searches the given search string on the platform of choice (default Youtube)"""

        # Select search provider
        if provider_arg in ['nnd', 'nv', 'nicovideo']:
            provider = providers['nicovideo']
        else:
            # Default: Youtube
            provider = providers['youtube']

        # Do actual search
        results = await provider.search("searchterm")

        # todo: show and paginate results
        pass

    # Command to leave voice
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    # Check if connected to voice
    async def cog_before_invoke(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")

    #####################################################################

    async def _play_next(self):
        """ Crossfades to the next song, or stops if there's no next song to play.
            This takes into account the RepeatMode, thus it could also switch to the same song again."""
        if self.repeat_mode is RepeatMode.REPEAT_ONE:
            next_song_index = self.current_song_index
        elif self.current_song_index == len(self.song_queue) - 1:
            next_song_index = 0

            if self.repeat_mode is not RepeatMode.REPEAT_ALL:
                await self._stop()
                return
        else:
            next_song_index = self.current_song_index + 1

        source = Source(self.song_queue[next_song_index])
        if await source.prepare():
            self.mixer.crossfade_to(source)
            self.current_song_index = next_song_index
        else:
            print("error changing to that file")
            await self._stop()
            return

    def _stop(self):
        self.play_status = PlayStatus.STOPPED
        self.current_song_index = 0
        self.mixer.set_source(None)

    """async def task_prepare_next_song(self, wait_duration):
        # Sleep for the time it takes for the song to finish
        await asyncio.sleep(wait_duration)

        print("preparing next song!")

        source = Source(random.choice(self.song_queue))
        if await source.download_started():
            self.mixer.crossfade_to(source)

        else:
            print("error changing to that file")

        self.prepare_task = asyncio.create_task(self.task_prepare_next_song(wait_duration))"""


def setup(bot):
    bot.add_cog(Music(bot))
