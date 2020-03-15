import discord

docentRoleName = "Docent"
rectorRoleName = "Rector"
adminRoleName = "admin"
docentRole = None
rectorRole = None
adminRole = None

async def initRoles(guild):
    docentRole = discord.utils.get(guild.roles, name=docentRoleName)
    rectorRole = discord.utils.get(guild.roles, name=rectorRoleName)
    adminRole = discord.utils.get(guild.roles, name=adminRoleName)

lokaaloverwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, read_message_history=False),
        guild.get_role(docentRole): discord.PermissionOverwrite(read_mes) 
    }