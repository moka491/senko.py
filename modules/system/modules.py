import traceback
from discord.ext import commands
from discord.ext.commands import ExtensionError

class Modules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='module')
    @commands.is_owner()
    async def module_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Module command.')

    @module_group.command(name='load')
    async def module_load(self, ctx, name: str):
        try:
            self.bot.load_extension("modules."+name)

            await ctx.send(f'Loaded module {name}')
            print(f'Loaded module {name}')
        except ExtensionError:

            await ctx.send(f'Failed to load module {name}')
            print(f'Failed to load module {name}')
            traceback.print_exc()

    @module_group.command(name='unload')
    async def module_unload(self, ctx, name: str):
        try:
            self.bot.unload_extension("modules."+name)

            await ctx.send(f'Unloaded module {name}')
            print(f'Loaded module {name}')
        except ExtensionError:
            await ctx.send(f'Failed to unload module {name}')
            print(f'Failed to unload module {name}')

            traceback.print_exc()

    @module_group.command(name='reload')
    async def module_reload(self, ctx, name: str):
        try:
            self.bot.reload_extension("modules."+name)

            await ctx.send(f'Reloaded module {name}')
            print(f'Reloaded module {name}')
        except ExtensionError:

            await ctx.send(f'Failed to reload module {name}')
            print(f'Failed to reload module {name}')
            traceback.print_exc()


def setup(bot):
    bot.add_cog(Modules(bot))
