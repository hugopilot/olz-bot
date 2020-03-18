import discord
from models import rank

async def assignrole(usr, guild, role: rank.Rank, reason: str = None):
    r = discord.utils.get(guild.roles, name=str(role))
    if(r == None):
        return
    if(reason == None):
        reason = "Auto-assiged by OLZBot"

    await usr.add_roles(r, reason=reason)

async def removeRole(usr, guild, role: rank.Rank, reason: str = None):
    r = discord.utils.get(guild.roles, name = str(role))

    if r == None:
        return

    if(reason == None):
        reason = "Auto-removed by OLZBot"

    await usr.remove_roles(r, reason = reason)
