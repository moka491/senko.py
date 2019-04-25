from discord.ext import commands
import discord
from core.music.FFmpegPCMPipeStream import FFmpegPCMPipeStream


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stream = None

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        self.stream = FFmpegPCMPipeStream(query, self.bot)
        # todo: await aiohttp stream here

        source = discord.PCMVolumeTransformer(self.stream)
        ctx.voice_client.play(source)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):

        if self.stream is not None:
            self.stream.stop()
            self.stream = None

        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()

    @play.before_invoke
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
