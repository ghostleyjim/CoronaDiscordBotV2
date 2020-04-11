#!/usr/bin/env python3
import matplotlib.pyplot as plt
import csv
import datetime
import numpy as np

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

createGraphs()