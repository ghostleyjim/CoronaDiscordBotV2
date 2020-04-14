# store global vars in here
import datetime

def _init():
    global municipalities
    global provinces
    global dateLastUpdate
    municipalities = [ ]
    provinces = [ ]
    dateLastUpdate = datetime.date.today() - datetime.timedelta(days=1)

class municipality:
    def __init__(self, date, name, code, province, hospitalised, bevolkingsaantal=0, besmettingen=0):
        self.date = date
        self.name = name
        self.code = code
        self.province = province
        self.hospitalised = hospitalised
        self.besmettingen = besmettingen
        self.bevolkingsaantal = bevolkingsaantal


class province:
    def __init__(self, date, name, hospitalised):
        self.date = date
        self.name = name
        self.hospitalised = hospitalised