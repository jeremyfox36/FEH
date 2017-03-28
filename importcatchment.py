import csv
from collections import namedtuple
import psycopg2


def import_catchment(user_name: str):

    # reads csv in and puts in it in a list of tuples
    # todo: ask for user file to be uploaded in .CD3 format
    # todo: check program.py for flask procedure hints
    # this function should return data to the database under the user account
    # may be redundant for the web app

    ungauged_catchment = namedtuple('ungauged_catchment', ['areai', 'saari', 'farli', 'fpexti'])

    with open('/Users/jem/WINFAP-FEH_v4.1/FEH/FEH/gore water.csv', 'r') as catchmentfile:
        reader = csv.reader(catchmentfile)
        ungaugedcatchment_list = list(reader)

        # later the name of ungauged_catchment will be changed according to user
        # input so that it can be saved ot the users database

        # most of these parameters are not used but might be needed later when we put this into the users
        # project database

        version = ' '.join(ungaugedcatchment_list[0][1:8])
        catchment = ','.join(ungaugedcatchment_list[1][2:4])
        centroid = ','.join(ungaugedcatchment_list[2][2:4])
        area = float(ungaugedcatchment_list[3][1])
        altBar = float(ungaugedcatchment_list[4][1])
        aspBar = float(ungaugedcatchment_list[5][1])
        aspVar = float(ungaugedcatchment_list[6][1])
        bfiHost = float(ungaugedcatchment_list[7][1])
        dplBar = float(ungaugedcatchment_list[8][1])
        dpsBar = float(ungaugedcatchment_list[9][1])
        farl = float(ungaugedcatchment_list[10][1])
        fpExt = float(ungaugedcatchment_list[11][1])
        fpdBar = float(ungaugedcatchment_list[12][1])
        fpLoc = float(ungaugedcatchment_list[13][1])
        ldp = float(ungaugedcatchment_list[14][1])
        propwet = float(ungaugedcatchment_list[15][1])
        rmed_1h = float(ungaugedcatchment_list[16][1])
        rmed_1d = float(ungaugedcatchment_list[17][1])
        rmed_2d = float(ungaugedcatchment_list[18][1])
        saar = float(ungaugedcatchment_list[19][1])
        saar4170 = float(ungaugedcatchment_list[20][1])
        sprHost = float(ungaugedcatchment_list[21][1])
        urbConc1990 = float(ungaugedcatchment_list[22][1])
        urbExt1990 = float(ungaugedcatchment_list[23][1])
        urbLoc1990 = float(ungaugedcatchment_list[24][1])
        urbConc2000 = float(ungaugedcatchment_list[25][1])
        urbExt2000 = float(ungaugedcatchment_list[26][1])
        urbLoc2000 = float(ungaugedcatchment_list[27][1])
        c = float(ungaugedcatchment_list[28][1])
        d1 = float(ungaugedcatchment_list[29][1])
        d2 = float(ungaugedcatchment_list[30][1])
        d3 = float(ungaugedcatchment_list[31][1])
        e = float(ungaugedcatchment_list[32][1])
        f = float(ungaugedcatchment_list[33][1])
        c_1km = float(ungaugedcatchment_list[34][1])
        d1_1km = float(ungaugedcatchment_list[35][1])
        d2_1km = float(ungaugedcatchment_list[36][1])
        d3_1km = float(ungaugedcatchment_list[37][1])
        e_1km = float(ungaugedcatchment_list[38][1])
        f_1km = float(ungaugedcatchment_list[39][1])

    db = psycopg2.connect("dbname='feh1' user='jem' host='localhost'")
    cur = db.cursor()
    uc = ungauged_catchment(areai=area, saari=saar, farli=farl, fpexti=fpExt)
    cur.execute('CREATE TABLE IF NOT EXISTS user_ungauged_catchment'
              '(catchment_name VARCHAR, areai REAL, saari REAL, farli REAL, fpexti REAL)')
    db.commit()

    SQLinsert = (
    "INSERT INTO user_ungauged_catchment(catchment_name, areai, saari, farli, fpexti) VALUES (%s, %s, %s, %s, %s)")
    data = (user_name, uc.areai, uc.saari, uc.farli, uc.fpexti)
    cur.execute(SQLinsert, data)
    db.commit()


