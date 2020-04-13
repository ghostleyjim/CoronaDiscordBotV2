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
    def __init__(self, date, name, code, province, hospitalised):
        self.date = date
        self.name = name
        self.code = code
        self.province = province
        self.hospitalised = hospitalised


class province:
    def __init__(self, date, name, hospitalised):
        self.date = date
        self.name = name
        self.hospitalised = hospitalised

_init()