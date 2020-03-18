import discord
from modules import permissions
from models import errors

async def CreateLokaal(ctx, name, scope=None):
    if(scope == None):
        raise TypeError("Missing Scope")
        return
    # Create initial PermissionOverwrite
    t = ctx.author
    t2 = discord.utils.get(ctx.guild.roles, name=permissions.rectorRoleName)
    t3 = discord.utils.get(ctx.guild.roles, name="MUTED")
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
        t: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True, stream=True),
        t2: discord.PermissionOverwrite(read_messages=True, connect=True, speak=True),
        t3: discord.PermissionOverwrite(send_messages=False, speak=False)
    }
    # Switch scope and update PermissionOverwrite
    overwrites[discord.utils.get(ctx.guild.roles, name=scope)] = discord.PermissionOverwrite(read_messages=True, connect=True, speak=True, stream=False)
    nname = "{} {} {}".format(name, str(scope), ctx.author.nick)
    # Create category and channels
    c = await ctx.guild.create_category(nname, overwrites=overwrites)
    await ctx.guild.create_text_channel('chat', category=c)
    await ctx.guild.create_voice_channel('voice', category=c)

    # Destroy the overwrites obj
    del overwrites
    # Log and send msg
    
    await ctx.send("✅ {} aangemaakt!".format(name))

async def DeleteLokaal(ctx, name):
    # Find the category
    nname = "{} {}".format(name, ctx.author.nick)
    for x in ctx.guild.by_category():
        if(not x[0] == None and x[0].name == str(nname)):
            # Loop through nested channels
            for c in x[1]:
                # Delete the channel
                await c.delete()

            # Finally, delete the category
            await x[0].delete()
            return
    # Give error if none were found
    raise errors.NotFound(message="No catagory found")
        
