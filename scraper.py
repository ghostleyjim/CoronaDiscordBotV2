#!usr/bin/env python3

import wget
import os

remove_list = {}


def database_scrape():
    with open('config.txt', 'r') as config:
        input = config.readline().split(',')
        for x in input:
            total = x.split('=')
            keyname = total[ 0 ].strip(' ')
            varname = total[ 1 ].strip(' ')
            remove_list[ keyname ] = varname

    # remove old files
    os.remove(remove_list[ 'dir_hosp_municipality' ])
    os.remove(remove_list[ 'dir_NL_total' ])
    os.remove(remove_list[ 'dir_nice' ])

    # links for raw repositories
    page1 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_hosp_municipality.csv'
    page2 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_national.csv'
    page3 = 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/nice_ic_by_day.csv'

    # download new files
    dir_hosp_municipality = wget.download(page1)
    dir_NL_total = wget.download(page2)
    dir_nice = wget.download(page3)

    with open('config.txt', 'w') as config:
        print(f'dir_hosp_municipality = {dir_hosp_municipality}, dir_NL_total = {dir_NL_total}, dir_nice = {dir_nice}', file=config, end='')
