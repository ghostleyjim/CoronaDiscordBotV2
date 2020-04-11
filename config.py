# store global vars in here

def _init():
    global municipalities
    global provinces
    municipalities = [ ]
    provinces = [ ]


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
