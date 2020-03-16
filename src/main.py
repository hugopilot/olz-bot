import discord
import config
import usrmanagement
import typing
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from modules import log
from modules import channels
from modules import permissions
from modules import sqldb
from models import rank


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
    log._log("{} created new lokaal: {}".format(ctx.author, name))
    await ctx.send("Created {}".format(name))


"""Deletes a Lokaal-category"""
@bot.command()
@commands.has_any_role(permissions.docentRoleName, permissions.rectorRoleName, permissions.adminRoleName)
async def dl(ctx, name:str):
    await channels.DeleteLokaal(ctx, name)
    log._log("{} deleted lokaal: {}".format(ctx.author, name))
    await ctx.send("Deleted category {}".format(name))


"""Assigns a rank to a pupil/staff member"""
@bot.command()
@commands.has_any_role(permissions.rectorRoleName, permissions.adminRoleName)
async def assignpup(ctx, musr: typing.Union[discord.User, str], role:str):
    # Try to convert to objects or die
    if(isinstance(musr, str)):
        await ctx.send("_Kon niet gebruiker vinden_")
        return
    try:
        ra = rank.Rank[role]
        print(ra)
        print(str(ra))
    except KeyError:
        await ctx.send("_Kon niet de klas herkennen (Klassen zijn hoofdlettergevoelig!)_")
        return

    # Add to database
    sqldb.updaterecord(musr.id, ra)
    log._log("{} assigned {} role {}".format(ctx.author, musr, str(ra)))
    # Give confirmation
    await ctx.send("_Assigned!_")

"""Debug command: get rank"""
@bot.command()
@commands.has_any_role(permissions.rectorRoleName, permissions.adminRoleName)
async def getpup(ctx, musr: typing.Union[discord.User, str]):
    # Try to convert to objects or die
    if(isinstance(musr, str)):
        await ctx.send("_Kon niet gebruiker vinden_")
        return
    r = sqldb.getuser(musr.id)
    if(not r):
        await ctx.send("_Geen data gevonden!_")
    else:
        await ctx.send("_{} is rank {}_".format(musr, r[0][1]))
@bot.event
async def on_member_join(member):
    await usrmanagement.setup(bot, member)

# Start running the bot
bot.run(config.token)
