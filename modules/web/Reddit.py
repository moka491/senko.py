import re, discord
from discord.ext import commands

class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.regex_sub = re.compile(r'(^|\s)/?(r/\w+)/?')
        self.regex_user = re.compile(r'(^|\s)/?(u/\w+)/?')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            sub_matches = self.regex_sub.findall(message.content)
            user_matches = self.regex_user.findall(message.content)

            if sub_matches:
                sub_set = unique(map(lambda match: match[1], sub_matches))
                msg = '\n'.join(map(lambda sub: "[/{0}](https://reddit.com/{0})".format(sub), sub_set))

                em = {
                    "color": 0x3498db,
                    "title": 'Mentioned Subreddits',
                    "description": msg
                }

                await message.channel.send(embed=discord.Embed.from_dict(em))

            if user_matches:
                user_set = unique(map(lambda match: match[1], user_matches))
                msg =  '\n'.join(map(lambda user: "[/{0}](https://reddit.com/{0})".format(user), user_set))

                em = {
                    "color": 0x3498db,
                    "title": 'Mentioned Users',
                    "description": msg
                }

                await message.channel.send(embed=discord.Embed.from_dict(em))


def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def setup(bot):
    bot.add_cog(Reddit(bot))


