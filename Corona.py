def dataextract():
    with open('rivm_NL_covid19_hosp_municipality.csv', 'r') as database:

        seperate = (line for line in database)
        next(seperate)
        for x in seperate:
            result = x.lower()
            info = result.split(',')

            date = info[ 0 ]
            year_month_day = date.split('-')
            month = year_month_day[ 1 ]
            day = year_month_day[ 2 ]

            municipality = info[ 1 ]
            province = info[3]
            cases = int((info[ 4 ]).strip('\n'))









dataextract()