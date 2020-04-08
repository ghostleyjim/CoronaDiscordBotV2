#!usr/bin/env python3

import wget
import os
import datetime
from threading import Timer

remove_list = {}
clock = datetime.datetime.today().day
last_update = 0


#
# #todo dit afmaken!
# def timecheck():
#     print(last_update)
#     clock = datetime.datetime.today().day
#     if last_update != clock:
#         database_scrape()
#     Timer(14400, timecheck).start()

def database_scrape():
    # open file with the file locations and add them to a list
    with open('directories.txt', 'r') as directorylist:
        directories = [ ]
        read = (line for line in directorylist)
        for lines in read:
            directories.append(lines.strip('\n'))

    # remove old files from list (if available)
    try:
        for x in directories:
            os.remove(x)
    except:
        pass

    #todo check voor meer links
    #list for raw repositories add , + <url> when new repo's used
    page = [ 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_hosp_municipality.csv',
             'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_national.csv',
             'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/nice_ic_by_day.csv' ]

    # download new files
    directory = [ ]
    for x in range(len(page)):
        directory.append(wget.download(page[ x ], out='./data'))

    with open('directories.txt', 'w') as directorylist:
        save_file = ''
        length = len(directory)
        for x in range(length):
            if x != length:
                save_file += directory[ x ] + '\n'
            else:
                save_file += directory[ x ]
        print(save_file, file=directorylist, end='')

    with open('config.txt', 'r+') as config:
        pass


database_scrape()
