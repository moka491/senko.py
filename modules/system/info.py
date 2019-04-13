import discord, platform
from discord.ext import commands
from uptime import uptime, boottime
from util.globals import app_version


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stats')
    async def show_stats(self, ctx):

        appinfo = await self.bot.application_info()

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
                        appinfo.owner.name,
                        appinfo.owner.discriminator,
                        appinfo.owner.id),
                    "inline": True
                },
                {
                    "name": "Versions",
                    "value": "Senko-san v{}\ndiscord.py v{}\npython {}".format(
                        app_version,
                        discord.__version__,
                        platform.python_version()),
                    "inline": True
                },
                {
                    "name": "System Info",
                    "value": "OS: {}\nUptime: {}\nBoottime: {}".format(
                        platform.platform(),
                        self.seconds_to_time_str(uptime()),
                        boottime().strftime('%B %d %Y %H:%M:%S'))
                }
            ]
        }

        await ctx.send(embed=discord.Embed.from_dict(em))

    def seconds_to_time_str(self, sec):

        if not sec:
            return ''

        total_seconds = float(sec)

        # Helper vars:
        MINUTE = 60
        HOUR = MINUTE * 60
        DAY = HOUR * 24

        # Get the days, hours, etc:
        days = int(total_seconds / DAY)
        hours = int((total_seconds % DAY) / HOUR)
        minutes = int((total_seconds % HOUR) / MINUTE)
        seconds = int(total_seconds % MINUTE)

        # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
        string = ""
        if days > 0:
            string += str(days) + " " + (days == 1 and "day" or "days") + ", "
        if len(string) > 0 or hours > 0:
            string += str(hours) + " " + (hours == 1 and "hour" or "hours") + ", "
        if len(string) > 0 or minutes > 0:
            string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes") + ", "
        string += str(seconds) + " " + (seconds == 1 and "second" or "seconds")

        return string


def setup(bot):
    bot.add_cog(Info(bot))
