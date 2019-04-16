import re, discord
from discord.ext import commands


class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regex_sub = re.compile(r'(?:^|[^\w])(/r/[^\s/]+)/?(?:$|\s)')
        self.regex_user = re.compile(r'(?:^|[^\w])(/u/[^\s/]+)/?(?:$|\s)')

    @commands.Cog.listener()
    async def on_message(self, message):

        if '/r/' in message.content:
            subs = self.regex_sub.findall(message.content)

            em = {
                "color": 0x519cff,
                "description": '\n'.join("[{0}](https://reddit.com{0})".format(sub) for sub in subs)
            }

            await message.channel.send(embed=discord.Embed.from_dict(em))

        if '/u/' in message.content:
            users = self.regex_user.findall(message.content)

            em = {
                "color": 0x519cff,
                "description": '\n'.join("[{0}](https://reddit.com{0})".format(user) for user in users)
            }

            await message.channel.send(embed=discord.Embed.from_dict(em))


def setup(bot):
    bot.add_cog(Reddit(bot))
