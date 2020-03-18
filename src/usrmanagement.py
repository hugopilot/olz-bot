import discord
import asyncio
from modules import sqldb
from models import rank
from modules import roles
from modules import log
import config
klaselist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

async def setup(bot, ctx):
    # Check if user already exists
    r = sqldb.getuser(ctx.id)
    if(r):
        # Assign role if already exists
        ra = rank.Rank[r[0][1]]
        await roles.assignrole(ctx, bot.get_guild(config.guild), ra)
        return

    ra = None
    # Prepare and send msg
    embed=discord.Embed(title="User Setup", description="Hallo! Ik ben een bot. Voordat je de server kan gebruiken, wil ik eerst graag het één en ander van je weten")
    embed.set_author(name="OLZ Bot")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/688016785051615234/fe16c6e01261201f6c7db801053635ca.png?size=256")
    embed.add_field(name="Druk op één van de knoppen hieronder", value="""In welke jaarlaag zit je?
    1️⃣ - 1e klas
    2️⃣ - 2e klas
    3️⃣ - HAVO 3
    4️⃣ - HAVO 4
    5️⃣ - HAVO 5
    6️⃣ - VWO 3
    7️⃣ - VWO 4
    8️⃣ - VWO 5
    9️⃣ - VWO 6
    """, inline=False)
    embed.set_footer(text="OLZBot v0.1; Medewerkers horen zich te melden bij de admins of rector")
    msg = await ctx.send(embed=embed)

    for emoji in klaselist:
        await msg.add_reaction(emoji)
    # User should be the mentioned one
    def check(reaction, user):
        return user == ctx and reaction.message.id == msg.id

    # Wait till the mentioned user reacts, or timeout
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=120.0, check=check)
    except asyncio.TimeoutError:
        # Delete the message
        await msg.delete()
        await ctx.send("Geen rollen toegewezen. Vraag een admin voor assistentie als dat nodig is.")
        return
    else:
        # r/badcode
        if(str(reaction.emoji) == klaselist[0]):
            ra = rank.Rank(1)
        elif(str(reaction.emoji) == klaselist[1]):
            ra = rank.Rank(2)
        elif(str(reaction.emoji) == klaselist[2]):
            ra = rank.Rank(3)
        elif(str(reaction.emoji) == klaselist[3]):
            ra = rank.Rank(4)
        elif(str(reaction.emoji) == klaselist[4]):
            ra = rank.Rank(5)
        elif(str(reaction.emoji) == klaselist[5]):
            ra = rank.Rank(6)
        elif(str(reaction.emoji) == klaselist[6]):
            ra = rank.Rank(7)
        elif(str(reaction.emoji) == klaselist[7]):
            ra = rank.Rank(8)
        elif(str(reaction.emoji) == klaselist[8]):
            ra = rank.Rank(9)
        await msg.delete()
    
    # If this passes, something went really wrong...
    if(ra == None):
        await ctx.send("_:thinking: Er is iets fout gegaan. Contacteer een admin (foutcode: 04)_")
        log._log("ra passed none. USR: {}".format(ctx))
        return

    # Save db 
    sqldb.updaterecord(ctx.id, ra)
    await roles.assignrole(ctx, bot.get_guild(config.guild), ra)
    log._log("Role {} assigned to {}".format(str(ra), ctx))
    await ctx.send("_Thanks! Roles assigned!_")

