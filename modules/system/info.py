import subprocess
import time

import discord, platform
from discord.ext import commands
from uptime import uptime

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stats')
    async def show_stats(self, ctx):

        app_info = await self.bot.application_info()

        try:
            app_version = subprocess.check_output(["git", "describe", "--tags"]).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            app_version = 'n/a'

        em = {
            "title": "About Senko-san",
            "description": "Hey, I'm the divine messenger fox, Senko-san!~\n"
                           "Your fluffy helpful bot written in [python](https://www.python.org) using [discord.py](https://github.com/Rapptz/discord.py)!",
            "color": 0xf0c561,
            "thumbnail": {
                "url": str(self.bot.user.avatar_url)
            },
            "fields": [
                {
                    "name": "Owner",
                    "value": "User: {}#{}\nId: {}".format(
                        app_info.owner.name,
                        app_info.owner.discriminator,
                        app_info.owner.id),
                    "inline": True
                },
                {
                    "name": "Versions",
                    "value": "Senko-san {}\ndiscord.py v{}\npython {}".format(
                        app_version,
                        discord.__version__,
                        platform.python_version()),
                    "inline": True
                },
                {
                    "name": "System Info",
                    "value": "OS: {}\nUptime: {}".format(
                        platform.platform(),
                        time.strftime("%H:%M:%S", time.gmtime(uptime()))
                    )
                }
            ]
        }

        await ctx.send(embed=discord.Embed.from_dict(em))

def setup(bot):
    bot.add_cog(Info(bot))
