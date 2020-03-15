import discord
import config
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from functions import channels
from functions import permissions
from functions import dbhandler
from functions import onjoinsetup

dbCursor = dbhandler.dbCursor

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
    await ctx.send("Created {}".format(name))

@bot.command()
@commands.has_any_role(permissions.docentRoleName, permissions.rectorRoleName, permissions.adminRoleName)
async def dl(ctx, name:str):
    await channels.DeleteLokaal(ctx, name)

# Create role objects after startup
@bot.event
async def on_ready():
    pass
    #global g
    #g = bot.get_guild(688009472949485600)
    #await permissions.initRoles(g)

@bot.event
async def on_member_join(member):
	# Check if the user is new and if so PM for setup
	uid = member.id
	dbCursor.execute('SELECT id FROM users WHERE id = ?', uid)
	result = dbCursor.fetchone()
	if result.id == None:
		# User is new
		# PM user and add DB entry
		onjoinsetup(member)
	else:
		# User is not new
		pass


# Start running the bot
bot.run(config.token)
