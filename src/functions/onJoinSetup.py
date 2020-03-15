import discord
import asyncio
from dbhandler import dbCursor

emojis = ["✅", "🚫"]

async def onJoinSetup(member):
	msg = await member.send('Select')

	for emoji in emojis:
		await msg.add_reaction(emoji)


	try:
		reaction, user await 
	except asyncio.TimeoutError:
		# Delete the message
		await msg.delete()
		return None

	else:
		if (str(reaction.))