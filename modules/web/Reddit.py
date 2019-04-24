import re, discord
from discord.ext import commands


class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regex_sub = re.compile(r'(^|[^\w])(/r/[a-zA-Z0-9_]+)/?($|[\s.,!?])')
        self.regex_user = re.compile(r'(^|[^\w])(/u/[a-zA-Z0-9_]+)/?($|[\s.,!?])')

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content

        if message.author != self.bot.user:
            if self.regex_sub.search(msg):
                msg = self.regex_sub.sub(r'\1[\2](https://reddit.com\2)\3', msg)
            if self.regex_user.search(msg):
                msg = self.regex_user.sub(r'\1[\2](https://reddit.com\2)\3', msg)

            if msg != message.content:
                em = {
                    "color": 0x519cff,
                    "title": message.author.name + ' said:',
                    "description": msg
                }

                await message.channel.send(embed=discord.Embed.from_dict(em))
                await message.delete()

def setup(bot):
    bot.add_cog(Reddit(bot))
