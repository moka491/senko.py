import traceback, glob, os

from discord.ext.commands import ExtensionError


class ModuleLoader:

    module_dir = "modules"

    def __init__(self, bot):
        self.bot = bot

    def init_modules(self):
        """ Iterates through module_dir and loads all found modules """
        os.chdir(self.module_dir)
        for filename in glob.iglob('**/*.py', recursive=True):
            module = filename.replace('.py', '').replace(os.sep, '.')
            self.load_module(module)

    def load_module(self, name):
        """ Tries to load the module specified """
        try:
            self.bot.load_extension(self.module_dir+"."+name)
            print(f'Loaded module {name}')
        except ExtensionError:
            print(f'Failed to load module {name}')
            traceback.print_exc()

    def unload_module(self, name):
        """ Tries to unload the module specified """
        try:
            self.bot.unload_extension(self.module_dir+"."+name)
            print(f'Unloaded module {name}')
        except ExtensionError:
            print(f'Failed to unload module {name}')
            traceback.print_exc()

    def reload_module(self, name):
        """ Tries to reload the module specified """
        try:
            self.bot.reload_extension(self.module_dir+"."+name)
            print(f'Reloaded module {name}')
        except ExtensionError:
            print(f'Failed to unload module {name}')
            traceback.print_exc()