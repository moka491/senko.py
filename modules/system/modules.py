from discord.ext import commands


class Modules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def module(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Invalid Module command.')

    @module.command()
    async def load(self, ctx, name: str):
        self.bot.loader.load_module(name)
        await ctx.send(f'Loaded module {name}')

    @module.command()
    async def unload(self, ctx, name: str):
        self.bot.loader.unload_module(name)
        await ctx.send(f'Unloaded module {name}')

    @module.command()
    async def reload(self, ctx, name: str):
        self.bot.loader.reload_module(name)
        await ctx.send(f'Reloaded module {name}')


def setup(bot):
    bot.add_cog(Modules(bot))