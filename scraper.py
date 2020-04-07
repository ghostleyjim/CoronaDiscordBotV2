#!usr/bin/env python3

import wget
import os
import datetime
from threading import Timer

remove_list = {}
clock = datetime.datetime.today().day
print(type(clock))

#todo
# def timecheck():
#     Timer(14400, timecheck).start()
#     if day_previous
#
#
# def database_scrape():
    # #open file with the file location
    # with open('config.txt', 'r') as config:
    #     input = config.readline().split(',')
    #     for x in input:
    #         #extract data for dictionary
    #         total = x.split('=')
    #         keyname = total[ 0 ].strip(' ')
    #         varname = total[ 1 ].strip(' ')
    #         #make dictionary from file
    #         remove_list[ keyname ] = varname
    #
    # # remove old files
    # os.remove(remove_list[ 'dir_hosp_municipality' ])
    # os.remove(remove_list[ 'dir_NL_total' ])
    # os.remove(remove_list[ 'dir_nice' ])
    #
    # # links for raw repositories
    # page1 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_hosp_municipality.csv'
    # page2 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_national.csv'
    # page3 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/nice_ic_by_day.csv'
    #
    # # download new files
    # dir_hosp_municipality = wget.download(page1)
    # dir_NL_total = wget.download(page2)
    # dir_nice = wget.download(page3)
    #
    # with open('config.txt', 'w') as config:
    #     print(f'dir_hosp_municipality = {dir_hosp_municipality}, dir_NL_total = {dir_NL_total}, dir_nice = {dir_nice}', file=config, end='')