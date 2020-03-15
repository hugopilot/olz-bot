import discord
from functions import permissions

async def CreateLokaal(ctx, name, scope):
    # Create initial PermissionOverwrite
    t = discord.utils.get(ctx.guild.roles, name=permissions.docentRoleName)
    t2 = discord.utils.get(ctx.guild.roles, name=permissions.rectorRoleName)
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
        t: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
        t2: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True)
    }
    # Switch scope and update PermissionOverwrite
    overwrites[discord.utils.get(ctx.guild.roles, name=scope)] = discord.PermissionOverwrite(read_messages=True, connect=True, speak=True)

    c = await ctx.guild.create_category(name, overwrites=overwrites)
    await ctx.guild.create_text_channel('chat', category=c)
    await ctx.guild.create_voice_channel('voice', category=c)
