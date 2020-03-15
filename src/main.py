import discord
import config
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from functions import channels
from functions import permissions

# Initialize the bot
bot = commands.Bot(command_prefix=config.prefix)
bot.remove_command('help')
g = bot.get_guild(688009472949485600)
permissions.initRoles(g)


"""Creates a Lokaal-catagory with their mandatory channels. Then returns the name. Only for Docent, Rector and Admins"""
@bot.command()
# Checks if mandatory roles are present
@commands.has_any_role(permissions.docentRole, permissions.rectorRole, permissions.adminRole)
async def cl(ctx, name):
    await channels.CreateLokaal(ctx, name, None)
    await ctx.send("OK created {}".format(name))




# Start running the bot
bot.run(config.token)
