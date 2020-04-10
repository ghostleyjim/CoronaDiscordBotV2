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


def inputparser(split_msg):
    request_value = 0
    msglength = len(split_msg)
    municipality_value = [ ]
    for x in range(msglength):
        if split_msg[ x ].startswith("-"):
            if split_msg[ x ][ 1: ].isdigit():
                request_value = split_msg[ x ][ 1: ]
        elif split_msg[ x ].isdigit():
            request_value = split_msg[ x ]

        else:
            municipality_value.append(split_msg[ x ])

    length = len(municipality_value)
    if length > 0:
        location = ' '.join(municipality_value).lower()
        send_ready = scraper.returnmunicipality(location, request_value)
        return send_ready
    else:
        send_ready = "Error, municipality is unknown"
        return send_ready


@client.event
async def on_ready():  # if script connects to Discord
    print(f'{client.user.name} has connected to Discord!')  # show I am connected with username


@client.event
async def on_message(message):  # if I reveive a message
    incomming = message.content

    if incomming.startswith("<"):
        split_msg = incomming.split(' ')
        if split_msg[ 1 ] == trigger:
            del (split_msg[ 0:2 ])
            if split_msg[ 0 ] == "graph":
                try:
                    graphs = plotNiceValues.createGraphs()
                    graph1 = graphs[ 1 ]
                    graph2 = graphs[ 2 ]

                    my_files = [ discord.File(graph1, 'graph1.png'), discord.File(graph2, 'graph2.png') ]

                    await message.channel.send('Graphs created by Diver', files=my_files)
                except:
                    errormsg = "Error in creating graphs"
                    await message.channel.send(errormsg)
            else:
                send_ready = inputparser(split_msg)
                await message.channel.send(send_ready)




    elif incomming.startswith(trigger):
        split_msg = incomming.split(' ')
        del (split_msg[ 0 ])
        if split_msg[ 0 ] == "graph":
            try:
                graphs = plotNiceValues.createGraphs()
                graph1 = graphs[ 1 ]
                graph2 = graphs[ 2 ]

                my_files = [ discord.File(graph1, 'graph1.png'), discord.File(graph2, 'graph2.png') ]

                await message.channel.send('Graphs created by Diver', files=my_files)
            except:
                errormsg = "Error in creating graphs"
                await message.channel.send(errormsg)

        else:
            send_ready = inputparser(split_msg)
            await message.channel.send(send_ready)


scraper.database_scrape()
timedevents.timer()

client.run(TOKEN)  # run the client and login with secret
