import csv
import datetime
import scraper

municipalities = []
provinces = []

#database file directories
with open('directories.txt', 'r') as directorylist:
    directories = [ ]
    read = (line for line in directorylist)
    for lines in read:
        directories.append(lines.strip('\n'))

mun_data = directories[0]
NL_data = directories[1]
nice_data = directories[3]

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

def dataextract():
    global municipalities, provinces
    with open('testcsv.csv', 'r') as csvfile:
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

            # print(dateRow - datetime.timedelta(days=4))

            municipalities.append(municipality(rowDate, row[1],row[2],row[3],row[4]))

            provinceExist = False
            for i in range(len(provinces)):
                if provinces[i].name == row[3]:
                    provinceExist = True
                    provinces[i].hospitalised += int(row[4])

            if provinceExist == False:
                provinces.append(province(row[3], int(row[4])))

def returnmunicipality(municipality, days):
    global municipalities
    arrMunici = []
    municipality = municipality
    days = days

    today = datetime.date.today()   # Uiteindelijk deze regel gaan gebruiken

    for i in range(len(municipalities)):
        if municipalities[i].name == municipality:
            arrMunici.append([municipalities[i].date, municipalities[i].name])

    arrSorted = sorted(arrMunici, key=lambda arrMunici: arrMunici[0], reverse=True)

    for i in range(len(municipalities)):
        if municipalities[i].name == municipality and municipalities[i].date == arrSorted[0][0]:
            arrMunici.append([municipalities[i].date, municipalities[i].name])
            return(municipalities[i].date, municipalities[i].name, municipalities[i].hospitalised)

dataextract()

#todo controle toevoegen of een gemeente in de database voorkomt
#todo als er geen aantal dagen wordt meegegeven dan "0" ipv aantal dagen gebruiken
#todo in bericht naar gebruiker aangeven van wanneer de gegeven data is
print(returnmunicipality("Almere", "0"))