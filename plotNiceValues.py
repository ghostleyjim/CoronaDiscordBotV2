#!/usr/bin/env python3
import matplotlib.pyplot as plt
import csv
import datetime

def createGraphs():
    x = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []

    with open('data/nice_ic_by_day.csv', 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))  # Check if there is a header present
        csvfile.seek(0)
        plots = csv.reader(csvfile, delimiter=',')

        if has_header:
            next(plots)

        for row in plots:
            readDate = row[0].split("-")
            rowYear = int(readDate[0])
            rowMonth = int(readDate[1])
            rowDay = int(readDate[2])
            rowDate = datetime.date(rowYear, rowMonth, rowDay)
            x.append(rowDate)
            y1.append(int(row[3]))
            y2.append(int(row[1]))
            y3.append(int(row[5]))
            y4.append(int(row[6]))

    # Create graph one
    fileName1 = "./graphs/IntensiveCare.png"
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_xlabel('date')
    ax1.set_ylabel('# of beds occupied', color=color)
    ax1.plot(x, y1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='x', rotation=45)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('new patients', color=color)
    ax2.plot(x, y2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title('Intensive Care')
    # plt.show()
    plt.savefig(fileName1)

    # Create graph two
    fileName2 = "./graphs/LeavingIntensiveCare.png"
    plt.plot(x, y1, color='tab:red', label='Intake (Cumulative)')
    plt.plot(x, y3, color='tab:blue', label='Deaths (Cumulative)')
    plt.plot(x, y4, color='tab:green', label='Recovered (Cumulative)')
    plt.tick_params(axis='x', rotation=45)
    plt.title('Leaving Intensive Care')
    plt.legend()
    # plt.show()
    plt.savefig(fileName2)
    return (True, fileName1, fileName2)

#createGraphs()
