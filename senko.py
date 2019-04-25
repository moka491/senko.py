import discord

import config, glob, os
from discord.ext import commands
from core.util.globals import module_dir

# Initialize bot
bot = commands.Bot(command_prefix='$', description='Divine messenger fox! To your service!')

# Load up modules from modules folder
for filename in glob.iglob(module_dir+'/**/*.py', recursive=True):
    module = filename.replace('.py', '').replace(os.sep, '.')
    print(f'Loaded module {module}')
    bot.load_extension(module)


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    await bot.change_presence(activity=discord.Activity(name=bot.command_prefix+'help', type=discord.ActivityType.listening))


@bot.event
async def on_message_edit(old, new):
    await bot.process_commands(new)

bot.run(config.token, bot=True, reconnect=True)
