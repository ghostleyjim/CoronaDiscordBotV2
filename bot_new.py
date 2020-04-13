#!/usr/bin/env python3

import discord
from dotenv import load_dotenv
import os
import datetime
import scraper, plotNiceValues, config

trigger = '!corona'

config._init()
scraper.database_scrape()


load_dotenv()  # load the secret from the ..env file
TOKEN = os.getenv('DISCORD_TOKEN')  # variable token stores the secret
PASTEAPI = os.getenv('PASTEBIN_TOKEN')
PASTEUSERKEY = os.getenv('PASTEBIN_USERKEY')
client = discord.Client()  # variable to store client info


def inputparser(split_msg):
    request_value = 0
    msglength = len(split_msg)
    municipality_value = [ ]

    if split_msg[ 0 ] == 'help':
        helpmsg = ("Hello, I'm your personal Covid-19 assistent, here is what I can do for you\n"
                   "'!corona graph' - graphs with national information from the Netherlands\n"
                   "'!corona graph <municipality>' - graph with municipality hospitalized patients information from the Netherlands\n"
                   "'!corona help' - shows you this page again\n"
                   "'!corona <municipality>' - information from the requested municipality\n"
                   "'!corona <municipality> <number>' - historical data from <number> days ago\n"
                   "'!corona listProv' - gives a list with all Provinces\n"
                   "'!corona listMun' - gives a list with all municipalities")
        return helpmsg

    elif split_msg[ 0 ] == "graph":
        try:
            if len(split_msg) == 1:
                graphs = plotNiceValues.createGraphs()

            else:
                munic_request = ' '.join(split_msg[ 1: ])

                for x in config.municipalities:
                    if x.name == munic_request:
                        graphs = plotNiceValues.municipalitygraph(munic_request)
                        return graphs
                else:
                    errormsg = 'municipality not found \n check https://www.cbs.nl/-/media/_excel/2020/03/gemeenten-alfabetisch-2020.xlsx for more information'
                    return errormsg

            return graphs

        except:
            errormsg = 'not able to create graphs!'
            return errormsg



    elif split_msg[ 0 ] == "listmun":
        listmunmsg = (f"The list of all municipalities is too long to print here.\n"
                      f"check https://www.cbs.nl/-/media/_excel/2020/03/gemeenten-alfabetisch-2020.xlsx for more information")
        return listmunmsg

    elif split_msg[ 0 ] == "listprov":
        provmsg = (f"Sorry, my devs are working on this at the moment")
        try:
            provmsg = scraper.listProv()
        except:
            pass
        return provmsg

    else:
        for x in range(msglength):
            if (split_msg[ x ].startswith("-") or split_msg[ x ].startswith("+")):
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
            split_msg = 'help'
            helpmessage = inputparser(split_msg)
            return (helpmessage)


@client.event
async def on_ready():  # if script connects to Discord
    print(f'{client.user.name} has connected to Discord!')  # show I am connected with username


@client.event
async def on_message(message):  # if I reveive a message
    incomming = message.content.lower()

    # update data once a day after 16:00
    if config.dateLastUpdate != datetime.date.today() and int(datetime.datetime.now().hour) >= 16:
        scraper.database_scrape()
        config.dateLastUpdate = datetime.date.today()

    if incomming.startswith("<"):
        split_msg = incomming.split(' ')
        if split_msg[ 1 ] == trigger:
            del (split_msg[ 0:2 ])
            if len(split_msg) == 0:
                split_msg.append("help")
            send_ready = inputparser(split_msg)
            if type(send_ready) == tuple:
                send_ready = [ discord.File(x, f'{x}graph.png') for x in send_ready ]
                await message.channel.send(files=send_ready)
            elif send_ready.startswith('./'):
                file = discord.File(send_ready, 'municgraph.png')
                await message.channel.send(file=file)
            else:
                await message.channel.send(send_ready)

    elif incomming.startswith(trigger):
        split_msg = incomming.split(' ')
        del (split_msg[ 0 ])
        if len(split_msg) == 0:
            split_msg.append("help")
        send_ready = inputparser(split_msg)
        if type(send_ready) == tuple:
            send_ready = [ discord.File(x, f'{x}graph.png') for x in send_ready ]
            await message.channel.send(files=send_ready)
        elif send_ready.startswith('./'):
            file = discord.File(send_ready, 'municgraph.png')
            await message.channel.send(file=file)
        else:
            await message.channel.send(send_ready)

client.run(TOKEN)  # run the client and login with secret
