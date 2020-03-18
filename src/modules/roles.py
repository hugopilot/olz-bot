import discord
from models import rank

async def assignrole(ctx, guild, role: rank.Rank, reason: str = None):
    r = discord.utils.get(guild.roles, name=str(role))
    if(r == None):
        return
    if(reason == None):
        reason = "Auto-assiged by OLZBot"

    await ctx.add_roles(r, reason=reason)

async def removeRole(ctx, guild, role: rank.Rank, reason: str = None):
    r = discord.utils.get(guild.roles, name = str(role))

    if r == None:
        return

    if reason == None:
        reason = "Auto-removed by OLZBot"

    await ctx.remove_roles(r, reason = reason)
