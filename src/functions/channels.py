import discord


async def CreateLokaal(ctx, name, scope):
    await ctx.guild.create_category(name)
