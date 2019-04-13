import traceback
from discord.ext import commands
from discord.ext.commands import ExtensionError
from util.globals import module_dir


class Modules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def module(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Module command.')

    @module.command()
    async def load(self, ctx, name: str):
        try:
            self.bot.load_extension(module_dir+"."+name)

            await ctx.send(f'Loaded module {name}')
            print(f'Loaded module {name}')
        except ExtensionError:

            await ctx.send(f'Failed to load module {name}')
            print(f'Failed to load module {name}')
            traceback.print_exc()

    @module.command()
    async def unload(self, ctx, name: str):
        try:
            self.bot.unload_extension(module_dir+"."+name)

            await ctx.send(f'Unloaded module {name}')
            print(f'Loaded module {name}')
        except ExtensionError:
            await ctx.send(f'Failed to unload module {name}')
            print(f'Failed to unload module {name}')

            traceback.print_exc()

    @module.command()
    async def reload(self, ctx, name: str):
        try:
            self.bot.reload_extension(module_dir+"."+name)

            await ctx.send(f'Reloaded module {name}')
            print(f'Reloaded module {name}')
        except ExtensionError:

            await ctx.send(f'Failed to reload module {name}')
            print(f'Failed to reload module {name}')
            traceback.print_exc()


def setup(bot):
    bot.add_cog(Modules(bot))
