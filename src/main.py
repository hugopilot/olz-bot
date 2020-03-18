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
from models import errors


# Initialize the bot
bot = commands.Bot(command_prefix=config.prefix)
bot.remove_command('help')
g = None

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Help page", description="Hoe ik werk?")
    embed.set_author(name="OLZ Bot")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/688016785051615234/fe16c6e01261201f6c7db801053635ca.png?size=256")
    embed.add_field(name="Lokaalcommando's", value="""`!lokaal <naam> <scope>` - Maakt een lokaal aan. Als je spaties gebruikt in je naam, gebruik dan aanhalingstekens. Voorbeeld: `!cl "Les van Bot" KLAS1`
    `!verwijder <naam>` - Verwijdert een lokaal.""", inline=False)
    embed.add_field(name="Help commando's", value="""`!help` - Print dit""", inline=False)
    embed.add_field(name="Lijst van scopes", value="""De mogelijke scopes zijn:
    - KLAS1
    - KLAS2
    - VWO3
    - HAVO3
    - VWO4
    - HAVO4
    - HAVO5
    - VWO5
    - VWO6""", inline=False)
    embed.set_footer(text="OLZBot v0.1;")
    msg = await ctx.author.send(embed=embed)

"""Creates a Lokaal-catagory with their mandatory channels. Then returns the name. Only for Docent, Rector and Admins"""
@bot.command()
# Checks if mandatory roles are present
@commands.has_any_role(permissions.docentRoleName, permissions.rectorRoleName, permissions.adminRoleName)
async def lokaal(ctx, name, scope=None):
    try:
        await channels.CreateLokaal(ctx, name, scope)
    except:
        await ctx.send("🚫 Mist een scope. Inputs: `Naam: {}`; `Scope: {}`".format(name, str(scope)))


"""Deletes a Lokaal-category"""
@bot.command()
@commands.has_any_role(permissions.docentRoleName, permissions.rectorRoleName, permissions.adminRoleName)
async def verwijder(ctx, name:str):
    try:
        await channels.DeleteLokaal(ctx, name)
    except errors.NotFound:
        await ctx.send("_Kon niet {} verwijderen: Categorie niet gevonden_".format(name))
    log._log("{} deleted lokaal: {}".format(ctx.author, name))
    await ctx.send("_✅ {} verwijderd!_".format(name))


"""Assigns a rank to a pupil/staff member"""
@bot.command()
@commands.has_any_role(permissions.rectorRoleName, permissions.adminRoleName)
async def assignpup(ctx, musr: typing.Union[discord.User, str], role:str):
    # Try to convert to objects or die
    if(isinstance(musr, str)):
        await ctx.send("_🚫 Kon niet gebruiker vinden_")
        return
    try:
        ra = rank.Rank[role]
        print(ra)
        print(str(ra))
    except KeyError:
        await ctx.send("_🚫 Kon niet de klas herkennen (Klassen zijn hoofdlettergevoelig!)_")
        return

    # Add to database
    sqldb.updaterecord(musr.id, ra)
    log._log("{} assigned {} role {}".format(ctx.author, musr, str(ra)))
    # Give confirmation
    await ctx.send("_Toegewezen!_")

"""Debug command: get rank"""
@bot.command()
@commands.has_any_role(permissions.rectorRoleName, permissions.adminRoleName)
async def getpup(ctx, musr: typing.Union[discord.User, str]):
    # Try to convert to objects or die
    if(isinstance(musr, str)):
        await ctx.send("_🚫 Kon niet gebruiker vinden_")
        return
    r = sqldb.getuser(musr.id)
    if(not r):
        await ctx.send("_🚫 Geen data gevonden!_")
    else:
        await ctx.send("_{} is rank {}_".format(musr, r[0][1]))

"""Remove current rank and save it in the db, wait a bit and give user the rank back"""
@bot.command()
@commands.has_any_role(permissions.docentRoleName, permssions.adminRoleName)
async def stuureruit(ctx, musr: typing.Union[discord.User, str], reason: str):
    if (isinstance(musr, str)):
        await ctx.send("_🚫 Kon niet gebruiker vinden_")
        return

    r = sqldb.getuser(musr.id)

    if (not r):
        await ctx.send("_🚫 Geen data gevonden!_")
    else:
        userRank = r[0][1]
        await roles.assignrole(ctx, bot.get_guild(config.guild), rank.Rank.MUTED)
        await ctx.send("_{} is eruitgestuurd!".format(musr))

@bot.event
async def on_member_join(member):
    await usrmanagement.setup(bot, member)

# Start running the bot
bot.run(config.token)
