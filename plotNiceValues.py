#!/usr/bin/env python3
import matplotlib.pyplot as plt
import csv
import datetime
import numpy as np
import config

def createGraphs():
    #Get name of .csv file from database
    with open('directories.txt', 'r') as directorylist:
        directories = [ ]
        read = (line for line in directorylist)
        for lines in read:
            directories.append(lines.strip('\n'))

    # Create arrays
    totals = np.array([[None,None]])
    hospital = np.array([[None,None]])
    deaths = np.array([[None,None]])
    dailyTotals = np.array([[None,None]])
    dailyHospital = np.array([[None,None]])
    dailyDeaths = np.array([[None,None]])

    # Open .csv file
    with open(directories[1], 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))  # Check if there is a header present
        csvfile.seek(0)
        plots = csv.reader(csvfile, delimiter=',')

        if has_header:
            next(plots)

        # Fill arrays with data from .csv file
        for row in plots:
            readDate = row[0].split("-")
            rowYear = int(readDate[0])
            rowMonth = int(readDate[1])
            rowDay = int(readDate[2])
            rowDate = datetime.date(rowYear, rowMonth, rowDay)

            if row[1] == "Totaal" and row[2] != '':                                 # "and row[2] != ''" is added to remove empty entries
                totals = np.append(totals, [[rowDate,int(row[2])]], axis=0)
            elif row[1] == "Ziekenhuisopname" and row[2] != '':
                hospital = np.append(hospital, [[rowDate,int(row[2])]], axis=0)
            elif row[1] == "Overleden" and row[2] != '':
                deaths = np.append(deaths, [[rowDate,int(row[2])]], axis=0)

        # Remove first entry which contains [0, 0]
        totals = np.delete(totals, 0, 0)
        hospital = np.delete(hospital, 0, 0)
        deaths = np.delete(deaths, 0, 0)

        # Calculate daily numbers
        for i in range(len(totals)):
            temp = int(totals[i, 1]) - int(totals[i-1, 1])
            dailyTotals = np.append(dailyTotals, [[totals[i, 0], temp]], axis=0)

        for i in range(len(hospital)):
            temp = int(hospital[i, 1]) - int(hospital[i-1, 1])
            dailyHospital = np.append(dailyHospital, [[hospital[i, 0], temp]], axis=0)

        for i in range(len(deaths)):
            temp = int(deaths[i, 1]) - int(deaths[i-1, 1])
            dailyDeaths = np.append(dailyDeaths, [[deaths[i, 0], temp]], axis=0)

        # Remove first two entries because they are worthless
        dailyTotals = np.delete(dailyTotals, [0,1], 0)
        dailyHospital = np.delete(dailyHospital, [0, 1], 0)
        dailyDeaths = np.delete(dailyDeaths, [0, 1], 0)

        # Find max values
        maxTotal = max(totals[:, 1])  # Find highest number
        tempDaily = np.where(totals[:, 1] == maxTotal)  # Find location of highest number
        whenTot = totals[tempDaily[int(len(tempDaily)) - 1][0], 0]

        maxDeath = max(deaths[:, 1])  # Find highest number
        tempDaily = np.where(deaths[:, 1] == maxDeath)  # Find location of highest number
        whenDeath = deaths[tempDaily[int(len(tempDaily)) - 1][0], 0]

        maxHospital = max(hospital[:, 1])  # Find highest number
        tempDaily = np.where(hospital[:, 1] == maxHospital)  # Find location of highest number
        whenHospital = hospital[tempDaily[int(len(tempDaily)) - 1][0], 0]

        maxDailyTotal = max(dailyTotals[:, 1])  # Find highest number
        tempDaily = np.where(dailyTotals[:, 1] == maxDailyTotal)  # Find location of highest number
        whenDailyTot = dailyTotals[tempDaily[int(len(tempDaily))-1][0], 0]

        maxDailyHospital = max(dailyHospital[:, 1])  # Find highest number
        tempDaily = np.where(dailyHospital[:, 1] == maxDailyHospital)  # Find location of highest number
        whenDailyHos = dailyHospital[tempDaily[int(len(tempDaily))-1][0], 0]

        maxDailyDeath = max(dailyDeaths[:, 1])  # Find highest number
        tempDaily = np.where(dailyDeaths[:, 1] == maxDailyDeath)  # Find location of highest number
        whenDailyDeath = dailyDeaths[tempDaily[int(len(tempDaily))-1][0], 0]

        #Find last values
        totalNow = totals[int(len(totals)) - 1][1]
        deathNow = deaths[int(len(deaths)) - 1][1]
        hospitalNow = hospital[int(len(hospital)) - 1][1]
        totalDailyNow = dailyTotals[int(len(dailyTotals)) - 1][1]
        deathsDailyNow = dailyDeaths[int(len(dailyDeaths)) - 1][1]
        hospitalDailyNow = dailyHospital[int(len(dailyHospital)) - 1][1]

        # Plot data
        fig1 = plt.gcf()
        plt.plot(totals[:, 0], totals[:, 1], label='Total of sick people (%.0f)' %totalNow, color='tab:blue')
        plt.plot(hospital[:, 0], hospital[:, 1], label='People in hospitals (%.0f)' %hospitalNow, color='tab:green')
        plt.plot(deaths[:, 0], deaths[:, 1], label='People who died (%.0f)' %deathNow, color='tab:red')
        plt.text(whenTot, maxTotal, maxTotal, color='tab:blue')
        plt.text(whenHospital, maxHospital, maxHospital, color='tab:green')
        plt.text(whenDeath, maxDeath, maxDeath, color='tab:red')
        plt.title('Cumulative corona numbers nation wide')
        plt.xticks(rotation=45)
        plt.legend()
        fileName1 = "./graphs/NumbersCumulative.png"
        fig1.savefig(fileName1, dpi=100, bbox_inches='tight')

        plt.clf()

        fig2 = plt.gcf()
        plt.plot(dailyTotals[:, 0], dailyTotals[:, 1], label='New amount of sick people (%.0f)' %totalDailyNow, color='tab:blue')
        plt.plot(dailyHospital[:, 0], dailyHospital[:, 1], label='New people in hospitals (%.0f)' %hospitalDailyNow, color='tab:green')
        plt.plot(dailyDeaths[:, 0], dailyDeaths[:, 1], label='New people who died (%.0f)' %deathsDailyNow, color='tab:red')
        plt.text(whenDailyTot, maxDailyTotal, maxDailyTotal, color='tab:blue')
        plt.text(whenDailyHos, maxDailyHospital, maxDailyHospital, color='tab:green')
        plt.text(whenDailyDeath, maxDailyDeath, maxDailyDeath, color='tab:red')
        plt.title('Daily corona numbers nation wide')
        plt.xticks(rotation=45)
        plt.legend()
        fileName2 = "./graphs/NumbersDaily.png"
        fig2.savefig(fileName2, dpi=100, bbox_inches='tight')

        plt.clf()

        return (fileName1, fileName2)


def municipalitygraph(municipality):
    arrMunici = [ ]  # store objects in array from requested municipality

    arrMunici.clear()

    arrMunici = [ x for x in config.municipalities if x.name == municipality ]
    amount = [ int(x.hospitalised) for x in arrMunici ]
    hospital_difference = [ [ amount[ x + 1 ] - amount[ x ] ] for x in range(len(amount)) if x < len(amount) - 1 ]
    hospital_difference.insert(0, [ 0 ])
    hospital_difference = [ y for x in hospital_difference for y in x ]
    besmettingen = [ int(x.besmettingen) for x in arrMunici ]
    besmettingen_difference = [ [ besmettingen[ x + 1 ] - besmettingen[ x ] ] for x in range(len(besmettingen)) if x < len(besmettingen) - 1 ]
    besmettingen_difference.insert(0, [ 0 ])
    besmettingen_difference = [ y for x in besmettingen_difference for y in x ]
    besmettingen_difference[ 13 ] = 0
    doden = [ int(x.overleden) for x in arrMunici ]
    overleden_difference = [ [ doden[ x + 1 ] - doden[ x ] ] for x in range(len(doden)) if x < len(doden) - 1 ]
    overleden_difference.insert(0, [ 0 ])
    overleden_difference = [ y for x in overleden_difference for y in x ]
    overleden_difference[ 16 ] = 0

    dates = [ x.date for x in arrMunici ]
    ydates = [ x.strftime('%d-%m') for x in dates ]

    mungraph = plt.gcf()
    ax = mungraph.add_subplot()
    plt.plot_date(range(len(ydates)), amount, xdate=True, marker='x', label=f'People hospitalized in {municipality}', color='tab:blue', ls='solid')
    plt.plot_date(range(len(ydates)), besmettingen, xdate=True, marker='.', label=f'People infected in {municipality}', color='tab:red', ls='solid')
    plt.title(f'Corona figures for {municipality}', pad=13.0)
    plt.xticks(range(len(ydates)), ydates, rotation=45)

    plt.legend()
    for i, v in enumerate(amount):
        ax.text(i, v, v, ha="center")
    for i, v in enumerate(besmettingen):
        ax.text(i, v, v, ha="center")

    mungraph_filename = "./graphs/MunicDaily.png"
    mungraph.savefig(mungraph_filename, dpi=100, bbox_inches='tight')

    plt.clf()

    # grafiek met verschillen
    dailydif = plt.gcf()
    difax = mungraph.add_subplot()
    plt.plot_date(range(len(ydates)), hospital_difference, xdate=True, marker='x', label=f'daily difference people hospitalized in {municipality}', color='tab:blue', ls='solid')
    plt.plot_date(range(len(ydates)), besmettingen_difference, xdate=True, marker='.', label=f'daily difference people infected in {municipality}', color='tab:red', ls='solid')
    plt.plot_date(range(len(ydates)), overleden_difference, xdate=True, marker='+', label=f'daily difference corona fatalities in {municipality}', color='k', ls='solid')
    plt.title(f'Daily differences for {municipality}', pad=13.0)
    plt.xticks(range(len(ydates)), ydates, rotation=45)

    plt.legend()

    for i, v in enumerate(hospital_difference):
        difax.text(i, v + 0.5, v, ha="center", color='b')
    for i, v in enumerate(besmettingen_difference):
        difax.text(i, v + 0.5, v, ha="center", color='r')
    for i, v in enumerate(overleden_difference):
        difax.text(i, v + 0.5, v, ha="center", color='k')

    dailydif_filename = "./graphs/difDaily.png"
    dailydif.savefig(dailydif_filename, dpi=100, bbox_inches='tight')

    plt.clf()

    overleden = [ int(x.overleden) for x in arrMunici if int(x.overleden) != 0 ]
    not_zero_dates = [ x.date for x in arrMunici if int(x.overleden) != 0 ]
    ydates = [ x.strftime('%d-%m') for x in not_zero_dates ]
    dailygraph = plt.gcf()
    dayax = dailygraph.add_subplot()
    plt.plot_date(range(len(ydates)), overleden, xdate=True, marker='.', label=f'Corona fatalaties in {municipality}', color='tab:gray', ls='solid')
    plt.title(f'Corona fatality figures for {municipality}', pad=13.0)
    plt.xticks(range(len(ydates)), ydates, rotation=45)

    for i, v in enumerate(overleden):
        dayax.text(i, v, v, ha="center")

    dailygraph_filename = './graphs/MunDecDaily.png'
    dailygraph.savefig(dailygraph_filename, dpi=100, bbox_inches='tight')

    plt.clf()

    file_names = (mungraph_filename, dailydif_filename, dailygraph_filename)

    return file_names

# createGraphs()
