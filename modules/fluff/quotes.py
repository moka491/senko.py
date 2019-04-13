import discord, aiohttp
from discord.ext import commands


class Quotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='inspire')
    async def get_inspirobot_image(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://inspirobot.me/api?generate=true') as r:
                if r.status == 200:
                    url = await r.text()

                    em = {
                        "color": 0xf0c561,
                        "image": {
                            "url": url
                        }
                    }

                    await ctx.send(embed=discord.Embed.from_dict(em))


def setup(bot):
    bot.add_cog(Quotes(bot))
