#!/usr/bin/env python3

import discord
from dotenv import load_dotenv
import os
# import Corona
import scraper, plotNiceValues, timedevents

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
        send_ready = "Doe eens lekker normaal joh!"
        await message.channel.send(send_ready)
        # split_msg = incomming.split(' ')
        # if split_msg[1] == trigger:
        #     del(split_msg[0:2])
        #     if len(split_msg) < 2:
        #         split_msg.append('0')
        #
        #     try:
        #         send_ready = scraper.returnmunicipality(split_msg[0], split_msg[1])
        #
        #     except:
        #         send_ready = "Error, municipality is unknown"
        #
        #     await message.channel.send(send_ready)

    elif incomming.startswith(trigger):
        municipality_value = []
        request_value = 0

        split_msg = incomming.split(' ')
        del (split_msg[0])
        msglength = len(split_msg)

        if split_msg[0] == "graph":
            try:
                graphs = plotNiceValues.createGraphs()
                graph1 = graphs[1]
                graph2 = graphs[2]

                my_files = [discord.File(graph1, 'graph1.png'), discord.File(graph2, 'graph2.png')]

                await message.channel.send('Graphs created:', files=my_files)

            except:
                await message.channel.send("Error in creating graphs")

        else:
            for x in range(msglength):
                if split_msg[x].startswith("-"):
                    if split_msg[x][1:].isdigit():
                        request_value = split_msg[x][1:]
                elif split_msg[x].isdigit():
                    request_value = split_msg[x]

                else:
                    municipality_value.append(split_msg[x])

            length = len(municipality_value)
            if length > 0:
                location = ' '.join(municipality_value).lower()
                send_ready = scraper.returnmunicipality(location, request_value)
            else:
                send_ready = "Error, municipality is unknown"

            await message.channel.send(send_ready)  # todo: dit stuk ook bij < maken misschien een def?? <-- Gefixt, zie regel 27 en 28 ;-)


scraper.database_scrape()
timedevents.timer()

client.run(TOKEN)  # run the client and login with secret
