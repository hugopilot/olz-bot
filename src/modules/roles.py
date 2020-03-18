import discord
from models import rank

async def assignrole(ctx, guild, role: rank.Rank):
    r = discord.utils.get(guild.roles, name=str(role))
    if(r == None):
        return
    await ctx.add_roles(r, reason="Auto-assiged by OLZBot")

async def removeRole(ctx, guild, role: rank.Rank, reason):
	r = discord.utils.get(guild.roles, name = str(role))
	if (r == None):
		return

	await ctx.remove_roles(r, reason = reason)
