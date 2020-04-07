#!usr/bin/env python3
# Testje of het werkt
import discord
from dotenv import load_dotenv
import os
import Corona

trigger = '!corona'

load_dotenv()  # load the secret from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')  # variable token stores the secret
PASTEAPI = os.getenv('PASTEBIN_TOKEN')
PASTEUSERKEY = os.getenv('PASTEBIN_USERKEY')
client = discord.Client()  # variable to store client info

@client.event
async def on_ready():  # if script connects to Discord
    print(f'{client.user.name} has connected to Discord!')  # show I am connected with username


@client.event
async def on_message(message):  # if I reveive a message
    incomming = message.content

    if incomming.startswith("<"):
        split_msg = incomming.split(' ')
        if split_msg[1] == trigger:
            del(split_msg[0:2])
            #print(split_msg)

    elif incomming.startswith(trigger):
        split_msg = incomming.split(' ')
        del(split_msg[0])
        print(split_msg)
        x = find.input(split_msg)






client.run(TOKEN)  # run the client and login with secret
