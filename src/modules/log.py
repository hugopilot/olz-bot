import discord
import config
import datetime
from datetime import date

async def _log(bot, message):
    m = '[{}] {}'.format(datetime.datetime.now(), message)
    with open(config.logloc, 'a', encoding='utf-8') as log_f:
        log_f.write('{}\n'.format(m))
        log_f.close()
    print(m)
    ch = bot.get_guild(config.guild).get_channel(config.logch)
    embed=discord.Embed(title="Log", description=m)
    await ch.send(embed=embed)
