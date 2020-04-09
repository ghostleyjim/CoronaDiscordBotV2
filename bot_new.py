#!usr/bin/.env python3

import discord
from dotenv import load_dotenv
import os
import datetime
from threading import Timer
# import Corona
import scraper, plotNiceValues

trigger = '!corona'

load_dotenv()  # load the secret from the ..env file
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
            if len(split_msg) < 2:
                split_msg.append('0')

            try:
                send_ready = scraper.returnmunicipality(split_msg[ 0 ], split_msg[ 1 ])

            except:
                send_ready = "Error, municipality is unknown"

            await message.channel.send(send_ready)

    elif incomming.startswith(trigger):
        split_msg = incomming.split(' ')
        del(split_msg[0])
        if len(split_msg) < 2:
            split_msg.append('0')

        if split_msg[0].lower() == "graph":
            try:
                done = False
                graph1 = ""
                graph2 = ""
                while not done:
                    graph1 = plotNiceValues.createGraphs()[1]
                    graph2 = plotNiceValues.createGraphs()[2]
                    done = plotNiceValues.createGraphs()[0]

                my_files = [
                    discord.File(graph1, 'graph1.png'),
                    discord.File(graph2, 'graph2.png'),
                ]

                await message.channel.send('Graphs created', files=my_files)

            except:
                await message.channel.send("Error in creating graphs")

        else:
            try:
                send_ready = scraper.returnmunicipality(split_msg[0], split_msg[1])
            except:
                send_ready = "Error, municipality is unknown"

            await message.channel.send(send_ready)

client.run(TOKEN)  # run the client and login with secret

