import config
from discord.ext import commands
from util.moduleLoader import ModuleLoader

bot = commands.Bot(command_prefix='~', description='Divine messenger fox! To your service!')
bot.loader = ModuleLoader(bot)


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} - {bot.user.id}')
    bot.loader.init_modules()

bot.run(config.token, bot=True, reconnect=True)
