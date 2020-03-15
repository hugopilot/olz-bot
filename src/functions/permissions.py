import discord

docentRoleName = "Docent"
rectorRoleName = "Rector"
adminRoleName = "admin"
docentRole = None
rectorRole = None
adminRole = None
guild = None

async def initRoles(g):
    global docentRole
    global rectorRole 
    global adminRole
    docentRole = discord.utils.get(g.roles, name=docentRoleName)
    rectorRole = discord.utils.get(g.roles, name=rectorRoleName)
    adminRole = discord.utils.get(g.roles, name=adminRoleName)
    guild = g


