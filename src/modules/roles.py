import discord
from models import rank

async def assignrole(ctx, guild, role: rank.Rank):
    r = discord.utils.get(guild.roles, name=str(role))
    if(r == None):
        return
    await ctx.add_roles(r, reason="Auto-assiged by OLZBot")
