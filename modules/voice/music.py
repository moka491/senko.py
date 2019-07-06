import random

from discord.ext import commands
from discord.ext.commands import Cog

from core.music.Mixer import Mixer
from core.music.Song import Song
from core.music.Source import Source

class Music(commands.Cog):
    songs = [
        Song('https://sync.moe/s/QQ8cjPgfNAF6445/download'),
        Song('https://sync.moe/s/AdwxpE49NbonSFD/download'),
        Song('https://sync.moe/s/gsT2Nnmdqg8kb5k/download'),
        Song(
            'https://r6---sn-4g5edne6.googlevideo.com/videoplayback?expire=1562293783&ei=t2EeXbntFY__gQfluYrIAQ&ip=37.201.225.174&id=o-AHFluL3RfF7n1ubKDjbby8liiIxJfITipUmwk4D0DBHW&itag=18&source=youtube&requiressl=yes&mm=31%2C26&mn=sn-4g5edne6%2Csn-h0jeened&ms=au%2Conr&mv=m&mvi=5&pl=17&initcwndbps=940000&mime=video%2Fmp4&gir=yes&clen=31669431&ratebypass=yes&dur=312.470&lmt=1540270903207451&mt=1562272125&fvip=4&c=WEB&txp=5531432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cmime%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=ALgxI2wwRQIhALrDGz780PxchqHJ--adLZd3iHBOzPmhVOF-pmaX5muiAiA-I0NanH48z1II2sV_aqyzHSRJC_FhoYuqBogwIPjm4A%3D%3D&lsparams=mm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AHylml4wRAIgexzybinDLdwtdMgVABxPgxlsO-vGAw5VolNvklzAhNoCIHO4LHMWNnvru19ts4291IOrRlHOIBJO7iWybh4ARGEb')
    ]

    def __init__(self, bot):
        self.bot = bot
        self.mixer = Mixer()

    def get_source(self):
        return self.mixer

    @commands.command()
    async def play(self, ctx):
        source = Source(random.choice(self.songs))
        self.mixer.set_source(source)

        await source.download_started()
        ctx.voice_client.play(self.mixer)

    @commands.command()
    async def pause(self, ctx):
        pass

    @commands.command()
    async def seek(self, ctx):
        pass

    @commands.command()
    async def stop(self, ctx):
        pass

    @commands.command()
    async def next(self, ctx):
        source = Source(random.choice(self.songs))
        await source.download_started()
        self.mixer.crossfade_to(source)

    @commands.command()
    async def previous(self, ctx):
        pass

    @commands.command()
    async def shuffle(self, ctx):
        """ Toggles shuffling on and off.
        'play' and 'next track' commands will then pick a random song,
        instead of the next one in the queue.
        """
        pass

    @commands.command()
    async def repeat(self, ctx):
        """ Toggles between repetition of one song, of the whole queue, and disabling repeat
        :param ctx: discord.py context
        """
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

def setup(bot):
    bot.add_cog(Music(bot))
