#!/usr/bin/env python3
import csv
import wget
import os
import datetime
import config
import requests
from bs4 import BeautifulSoup

remove_list = {}
clock = datetime.datetime.today().day
last_update = 0

# database file directories
with open('directories.txt', 'r') as directorylist:
    directories = [ ]
    read = (line for line in directorylist)
    for lines in read:
        directories.append(lines.strip('\n'))

    mun_data = directories[ 0 ]
    NL_data = directories[ 1 ]
    nice_data = directories[ 2 ]


def database_scrape():
    # open file with the file locations and add them to a list
    with open('directories.txt', 'r') as directorylist:
        dirs = [ ]
        read = (line for line in directorylist)
        for lines in read:
            dirs.append(lines.strip('\n'))

    # remove old files from list (if available)
    try:
        for x in directories:
            os.remove(x)
    except:
        pass

    # list for raw repositories add , + <url> when new repo's used
    page = [ 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_hosp_municipality.csv', 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_national.csv',
             'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/nice_ic_by_day.csv' ]

    # RIVM website scraping
    # read file and check if date is already included today if not download and upload the file
    with open('data/RIVM.csv', 'r') as db:
        update_date = datetime.datetime.today().strftime('%Y-%m-%d;')
        check_date = datetime.datetime.today().strftime('%Y-%m-%d')
        firstline = db.readlines()
        firstline = [ x.rstrip('\n') for x in firstline ]
        firstline = [ x.split(',', 1)[ 0 ] for x in firstline ]
        # RIVM only updates their database at 1400 so check if data is already in list and only update after 1400
        check = (True if (check_date not in firstline) and int(datetime.datetime.now().hour) >= 14 else False)

    if check:
        rivm_db = requests.get('https://www.rivm.nl/coronavirus-kaart-van-nederland-per-gemeente')

        soup = BeautifulSoup(rivm_db.content, 'html.parser')

        results = soup.find(id="csvData")

        RIVM = results.get_text().rstrip('\n').replace(';', ',')

        RIVM = RIVM.lower().split('\n')

        # delete header and blank newline before appending
        del (RIVM[ 0:2 ])

        # Append data to csv file include date time stamp (string)
        with open("data/RIVM.csv", 'a') as db:
            inputdata = [ update_date + x for x in RIVM ]
            inputdata = '\n'.join(inputdata)
            db.write('\n')
            print(inputdata, file=db, end='')

    # download new files and add file directory to directory.txt (for deleting)
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

    dataextract()


def dataextract():
    config.municipalities.clear()
    config.provinces.clear()

    with open(mun_data, 'r') as csvfile, open(mun_data, 'r') as rivmdb:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))  # Check if there is a header present
        csvfile.seek(0)  # Go back to line 0 in CSV file
        readCSV = csv.reader(csvfile, delimiter=',')  # Read .CSV file
        also_has_header = csv.Sniffer().has_header(rivmdb.read(1024))
        rivmdb.seek(0)
        readRIVM = csv.reader(rivmdb, delimiter=';')
        if has_header:
            next(readCSV)
        if also_has_header:
            next(readRIVM)

        for row in readCSV:
            readDate = row[ 0 ].split("-")
            rowYear = int(readDate[ 0 ])
            rowMonth = int(readDate[ 1 ])
            rowDay = int(readDate[ 2 ])
            rowDate = datetime.date(rowYear, rowMonth, rowDay)

            # gemeentenaam = row[1].lower()
            # gemeentecode = row[2]
            # provincienaam = row[3].lower()
            # aantal = row[4]

            config.municipalities.append(config.municipality(rowDate, row[ 1 ].lower(), row[ 2 ], row[ 3 ].lower(), row[ 4 ]))

            provinceExist = False
            for i in range(len(config.provinces)):
                if config.provinces[ i ].name == row[ 3 ].lower() and config.provinces[ i ].date == rowDate:
                    provinceExist = True
                    config.provinces[ i ].hospitalised += int(row[ 4 ])

            if provinceExist == False:
                config.provinces.append(config.province(rowDate, row[ 3 ].lower(), int(row[ 4 ])))


def returnmunicipality(municipality, days):
    arrMunici = [ ]
    arrSorted = [ ]

    arrMunici.clear()
    arrSorted.clear()

    days = int(days)

    # fill temporary array when it's an municipality
    for i in range(len(config.municipalities)):
        if config.municipalities[ i ].name == municipality:
            arrMunici.append([ config.municipalities[ i ].date, config.municipalities[ i ].name, config.municipalities[ i ].hospitalised ])

    # fill temporary array when it's an province
    for i in range(len(config.provinces)):
        if config.provinces[ i ].name == municipality:
            arrMunici.append([ config.provinces[ i ].date, config.provinces[ i ].name, config.provinces[ i ].hospitalised ])

    if len(arrMunici) == 0:
        return (f"There is no municipality or province known called {municipality}\n"
                f"For help type '!corona help'")

    arrSorted = sorted(arrMunici, key=lambda arrMunici: arrMunici[ 0 ], reverse=True)

    if days != 0:
        try:
            difference = int(arrSorted[ 0 ][ 2 ]) - int(arrSorted[ days ][ 2 ])
            if difference > 0:
                return (f"{municipality.capitalize()}, {days} days ago:\n"
                        f"Today there have been {abs(difference)} more people hospitalized as on {arrSorted[ days ][ 0 ]} in {arrSorted[ days ][ 1 ].capitalize()}.\n"
                        f"Today there has been {arrSorted[ 0 ][ 2 ]} people hospitalized.")
            else:
                return (f"{municipality.capitalize()}, {days} days ago:\n"
                        f"Today there have been {abs(difference)} less people hospitalized as on {arrSorted[ days ][ 0 ]} in {arrSorted[ days ][ 1 ].capitalize()}.\n"
                        f"Today there has been {arrSorted[ 0 ][ 2 ]} people hospitalized.")

        except:
            if days == 1:
                return (f"No data available from {days} day ago for {arrSorted[ 0 ][ 1 ]}.")
            else:
                return (f"No data available from {days} days ago for {arrSorted[ 0 ][ 1 ]}.")
    else:
        return (f"{municipality.capitalize()}, {arrSorted[ 0 ][ 0 ]}:\n"
                f"There has been {arrSorted[ 0 ][ 2 ]} hospitalized in {arrSorted[ 0 ][ 1 ].capitalize()} on {arrSorted[ 0 ][ 0 ]}.")


def listProv():
    global provinces

    dataextract()
    tempArray = [ ]
    tempArray.clear()
    msg = ""

    for i in range(len(provinces)):
        if not provinces[ i ].name in tempArray:
            tempArray.append(provinces[ i ].name)

    tempArray = sorted(tempArray, key=lambda tempArray: tempArray[ 0 ], reverse=False)

    for i in range(len(tempArray)):
        msg += f"{str(tempArray[ i ]).capitalize()}\n"

    return (msg)

# todo probleem als municipality niet bestaat maar wel een dagwaarde heeft array error
