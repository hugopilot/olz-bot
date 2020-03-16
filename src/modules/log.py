import discord
from datetime import date

def _log(message):
    m = '[{}] {}'.format(datetime.datetime.now(), message)
    with open(config.logloc, 'a', encoding='utf-8') as log_f:
        log_f.write('{}\n'.format(m))
        log_f.close()
    print(m)
