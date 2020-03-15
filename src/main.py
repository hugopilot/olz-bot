import discord
import config
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from functions import channels
from functions import permissions

# Initialize the bot
bot = commands.Bot(command_prefix=config.prefix)
bot.remove_command('help')
g = None



"""Creates a Lokaal-catagory with their mandatory channels. Then returns the name. Only for Docent, Rector and Admins"""
@bot.command()
# Checks if mandatory roles are present
@commands.has_any_role(permissions.docentRoleName, permissions.rectorRoleName, permissions.adminRoleName)
async def cl(ctx, name, scope):
    await channels.CreateLokaal(ctx, name, scope)
    await ctx.send("OK created {}".format(name))


# Create role objects after startup
@bot.event
async def on_ready():
    pass
    #global g
    #g = bot.get_guild(688009472949485600)
    #await permissions.initRoles(g)

# Start running the bot
bot.run(config.token)
