import discord
import config
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

# Initialize the bot
bot = command.Bot(command_prefix=config.prefix)
bot.remove_command('help')

