from discord.ext import commands
import discord

from core.music.Mixer import Mixer
from core.music.Player import Player


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stream = None

    @commands.command()
    async def playtest(self, ctx):
        player = Player("https://sync.moe/s/QQ8cjPgfNAF6445/download")
        self.mixer = Mixer()
        self.mixer.setPlayer(player)

        async with ctx.typing():
            await player.await_download()
            ctx.voice_client.play(self.mixer)

    @commands.command()
    async def next(self, ctx):
        newplayer = Player("https://sync.moe/s/QQ8cjPgfNAF6445/download")
        await newplayer.await_download()
        self.mixer.crossfadeTo(newplayer)

    @commands.command()
    async def stop(self, ctx):
        if self.stream is not None:
            self.stream.stop()
            self.stream = None

    @playtest.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))
