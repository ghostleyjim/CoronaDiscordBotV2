#!/usr/bin/env python3
import csv
import wget
import os
import datetime
import timedevents

municipalities = []
provinces = []

remove_list = {}
clock = datetime.datetime.today().day
last_update = 0

class municipality:
    def __init__(self, date, name, code, province, hospitalised):
        self.date = date
        self.name = name
        self.code = code
        self.province = province
        self.hospitalised = hospitalised

class province:
    def __init__(self, name, hospitalised):
        self.name = name
        self.hospitalised = hospitalised

#database file directories
with open('directories.txt', 'r') as directorylist:
    directories = [ ]
    read = (line for line in directorylist)
    for lines in read:
        directories.append(lines.strip('\n'))

mun_data = directories[0]
NL_data = directories[1]
nice_data = directories[2]


#
#todo dit afmaken!
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

    #list for raw repositories add , + <url> when new repo's used
    page = [ 'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_hosp_municipality.csv',
             'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_national.csv',
             'https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/nice_ic_by_day.csv']

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

        timedevents.timer()

def dataextract():
    global municipalities, provinces

    with open(mun_data, 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))   # Check if there is a header present
        csvfile.seek(0)                                             # Go back to line 0 in CSV file
        readCSV = csv.reader(csvfile, delimiter=',')                # Read .CSV file

        if has_header:
            next(readCSV)

        for row in readCSV:
            readDate = row[0].split("-")
            rowYear = int(readDate[0])
            rowMonth = int(readDate[1])
            rowDay = int(readDate[2])
            rowDate = datetime.date(rowYear, rowMonth, rowDay)

            municipalities.append(municipality(rowDate, row[1].lower(),row[2],row[3].lower(),row[4]))

            provinceExist = False
            for i in range(len(provinces)):
                if provinces[i].name == row[3]:
                    provinceExist = True
                    provinces[i].hospitalised += int(row[4])

            if provinceExist == False:
                provinces.append(province(row[3], int(row[4])))

def returnmunicipality(municipality, days):
    global municipalities

    dataextract()

    arrMunici = [ ]
    municipality = municipality.lower()
    days = int(days)

    for i in range(len(municipalities)):
        if municipalities[ i ].name == municipality:
            arrMunici.append([ municipalities[ i ].date, municipalities[ i ].name, municipalities[ i ].hospitalised ])

    arrSorted = sorted(arrMunici, key=lambda arrMunici: arrMunici[ 0 ], reverse=True)

    # for x in range(len(arrSorted)):
    #     print(arrSorted[x][0], arrSorted[x][1], arrSorted[x][2])

    if days != 0:
        try:
            difference = int(arrSorted[ 0 ][ 2 ]) - int(arrSorted[ days ][ 2 ])
            if difference > 0:
                return (f"{municipality.capitalize()}, {days} days ago:\nToday there have been {abs(difference)} more people hospitalized as on {arrSorted[ days ][ 0 ]} in {arrSorted[ days ][ 1 ].capitalize()}.\nToday there has been {arrSorted[ 0 ][ 2 ]} people hospitalized.")
            else:
                return (f"{municipality.capitalize()}, {days} days ago:\nToday there have been {abs(difference)} less people hospitalized as on {arrSorted[ days ][ 0 ]} in {arrSorted[ days ][ 1 ].capitalize()}.\nToday there has been {arrSorted[ 0 ][ 2 ]} people hospitalized.")

        except:
            if days == 1:
                return (f"No data available from {days} day ago for {arrSorted[ 0 ][ 1 ]}.")
            else:
                return (f"No data available from {days} days ago for {arrSorted[ 0 ][ 1 ]}.")
    else:
        return (f"{municipality.capitalize()}, {arrSorted[ 0 ][ 0 ]}:\nThere has been {arrSorted[ 0 ][ 2 ]} hospitalized in {arrSorted[ 0 ][ 1 ].capitalize()} on {arrSorted[ 0 ][ 0 ]}.")

# todo probleem als municipality niet bestaat maar wel een dagwaarde heeft array error
# print(returnmunicipality("rOtTerdam","1"))
