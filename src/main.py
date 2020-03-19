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
from modules import roles
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
    embed.add_field(name="Straf commando's (alleen voor Rector en Admin)", value="""`!mute` <user> - Voorkomt dat gebruikers kunnen praten in alle kanalen
    !unmute <user>- Laat gebruikers weer praten""", inline=False)
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
    embed.set_footer(text="OLZBot v0.5;")
    msg = await ctx.author.send(embed=embed)

"""Creates a Lokaal-catagory with their mandatory channels. Then returns the name. Only for Docent, Rector and Admins"""
@bot.command()
# Checks if mandatory roles are present
@commands.has_any_role(permissions.docentRoleName, permissions.rectorRoleName, permissions.adminRoleName)
async def lokaal(ctx, name, scope=None):
    try:
        await channels.CreateLokaal(ctx, name, scope)
        await log._log(bot, "{} created new lokaal: {}".format(ctx.author, name))
    except:
        await ctx.send("🚫 Mist een scope. Inputs: `Naam: {}`; `Scope: {}`".format(name, str(scope)))


"""Deletes a Lokaal-category"""
@bot.command()
@commands.has_any_role(permissions.docentRoleName, permissions.rectorRoleName, permissions.adminRoleName)
async def verwijder(ctx, name:str, scope=None):
    if(scope == None):
        await ctx.send("🚫 Mist een scope. Inputs: `Naam: {}`; `Scope: {}`".format(name, str(scope)))
    try:
        await channels.DeleteLokaal(ctx, name, scope)
    except errors.NotFound:
        await ctx.send("_🚫 Kon niet {} verwijderen: Categorie niet gevonden_".format(name))
        return
    await log._log(bot, "{} deleted lokaal: {}".format(ctx.author, name))
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
    except KeyError:
        await ctx.send("_🚫 Kon niet de klas herkennen (Klassen zijn hoofdlettergevoelig!)_")
        return

    # Add to database
    sqldb.updaterecord(musr.id, ra)
    await roles.assignrole(musr, bot.get_guild(config.guild), ra, "Assigned by {}".format(ctx.author))
    await log._log(bot, "{} assigned {} role {}".format(ctx.author, musr, str(ra)))
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
@commands.has_any_role(permissions.rectorRoleName, permissions.adminRoleName)
async def mute(ctx, musr: typing.Union[discord.Member, str], reason: str = None):
    if (isinstance(musr, str)):
        await ctx.send("_🚫 Kon niet gebruiker vinden_")
        return

    r = sqldb.getuser(musr.id)
    if(not r):
        rr = musr.roles
        rrr = None
        for i in rr:
            # Try to parse into Rank
            try:
                rrr = rank.Rank[str(i)]
                break
            except KeyError:
                continue
        if(rrr == None):
            # Just die inside
            rrr = rank.Rank.MUTED
        sqldb.updaterecord(musr.id, rrr)

    await roles.assignrole(musr, bot.get_guild(config.guild), rank.Rank.MUTED, reason)
    sqldb.assignMute(musr.id)
    await musr.move_to(None)
    await log._log(bot, "{} muted {}".format(ctx.author, musr))
    await ctx.send("_{} muted!_".format(musr))

@bot.command()
@commands.has_any_role(permissions.rectorRoleName, permissions.adminRoleName)
async def unmute(ctx, musr: typing.Union[discord.Member, str]):
    if (isinstance(musr, str)):
        await ctx.send("_🚫 Kon niet gebruiker vinden_")
        return

    r = sqldb.getuser(musr.id)

    if (not r):
        await ctx.send("_🚫 Geen data gevonden!_")
    else:
        await roles.removeRole(musr, bot.get_guild(config.guild), rank.Rank.MUTED, 'Unmuted')
        sqldb.removeMute(r[0][0])
        await log._log(bot, "{} unmuted {}".format(ctx.author, musr))
        await ctx.send("_{}'s muted rol verwijderd!_".format(musr))

@bot.command()
@commands.has_any_role(permissions.docentRoleName, permissions.rectorRoleName, permissions.adminRoleName)
async def purge(ctx, amount=50):
    await ctx.channel.purge(limit=amount)
    await log._log(bot, "{} deleted {} messages using purge command on {}".format(ctx.author, ctx.channel.name), "Member ID: {}".format(ctx.author.id))

@bot.event
async def on_member_join(member):
    await log._log(bot, "Member {} joined".format(member), "Member ID: {}".format(member.id))
    await usrmanagement.setup(bot, member)

@bot.event
async def on_member_remove(member):
    await log._log(bot, "Member {} left".format(member), "Member ID: {}".format(member.id))

@bot.event
async def on_message_delete(message):
    await log._log(bot, "{} deleted message with content: _{}_".format(message.author, message.content), "Message ID: {}; Created at: {}".format(message.id, message.created_at))

@bot.event
async def on_message_edit(before, after):
    # Prevent bot loop
    if(before.author == bot.user):
        return

    await log._log(bot, """{} edited message:
    
    **Before**:
    {}
    
    **After**:
    {}""".format(after.author, before.content, after.content), "Message ID: {}; Created at: {}; Edited at: {}".format(after.id, before.created_at, after.edited_at))
# Start running the bot
bot.run(config.token)
