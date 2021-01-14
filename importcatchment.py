import csv

import pandas as pd
import psycopg2
import psycopg2.extras
from psycopg2._psycopg import AsIs
from sqlalchemy import create_engine


def check_if_table_exists(table_name: str):

    db = psycopg2.connect("dbname='feh1' user='jem' host='localhost'")
    cur = db.cursor()

    cur.execute("SELECT EXISTS (SELECT * FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND c.relname =%s)", (table_name,))

    exists = cur.fetchone()

    return exists[0]


def import_catchment():

    # todo: ask for user file to be uploaded in .CD3 format
    # todo: check program.py for flask procedure hints
    # this function should return data to the database under the user account
    # may be redundant for the web app

    with open('/Users/jem/WINFAP-FEH_v4.1/FEH/FEH/gore water.csv', 'r') as catchmentfile:
        reader = csv.reader(catchmentfile)
        ungaugedcatchment_list = list(reader)
        ungauged_catchment_dict = {}
        # later the name of ungauged_catchment will be changed according to user
        # input so that it can be saved to the users database

        ungauged_catchment_dict['catchment_name'] = 'test' # change to user id or something similar and index on this
        ungauged_catchment_dict['version'] = ' '.join(ungaugedcatchment_list[0][1:8])
        ungauged_catchment_dict['catchment'] = ','.join(ungaugedcatchment_list[1][2:4])
        ungauged_catchment_dict['centroid'] = ','.join(ungaugedcatchment_list[2][2:4])
        ungauged_catchment_dict['centroid_e'] = int(ungaugedcatchment_list[2][2])
        ungauged_catchment_dict['centroid_n'] = int(ungaugedcatchment_list[2][3])
        ungauged_catchment_dict['area'] = float(ungaugedcatchment_list[3][1])
        ungauged_catchment_dict['altbar'] = float(ungaugedcatchment_list[4][1])
        ungauged_catchment_dict['aspbar'] = float(ungaugedcatchment_list[5][1])
        ungauged_catchment_dict['aspvar'] = float(ungaugedcatchment_list[6][1])
        ungauged_catchment_dict['bfihost'] = float(ungaugedcatchment_list[7][1])
        ungauged_catchment_dict['dplbar'] = float(ungaugedcatchment_list[8][1])
        ungauged_catchment_dict['dpsbar'] = float(ungaugedcatchment_list[9][1])
        ungauged_catchment_dict['farl'] = float(ungaugedcatchment_list[10][1])
        ungauged_catchment_dict['fpext'] = float(ungaugedcatchment_list[11][1])
        ungauged_catchment_dict['fpdbar'] = float(ungaugedcatchment_list[12][1])
        ungauged_catchment_dict['fploc'] = float(ungaugedcatchment_list[13][1])
        ungauged_catchment_dict['ldp'] = float(ungaugedcatchment_list[14][1])
        ungauged_catchment_dict['propwet'] = float(ungaugedcatchment_list[15][1])
        ungauged_catchment_dict['rmed_1h'] = float(ungaugedcatchment_list[16][1])
        ungauged_catchment_dict['rmed_1d'] = float(ungaugedcatchment_list[17][1])
        ungauged_catchment_dict['rmed_2d'] = float(ungaugedcatchment_list[18][1])
        ungauged_catchment_dict['saar'] = float(ungaugedcatchment_list[19][1])
        ungauged_catchment_dict['saar4170'] = float(ungaugedcatchment_list[20][1])
        ungauged_catchment_dict['sprhost'] = float(ungaugedcatchment_list[21][1])
        ungauged_catchment_dict['urbconc1990'] = float(ungaugedcatchment_list[22][1])
        ungauged_catchment_dict['urbext1990'] = float(ungaugedcatchment_list[23][1])
        ungauged_catchment_dict['urbloc1990'] = float(ungaugedcatchment_list[24][1])
        ungauged_catchment_dict['urbconc2000'] = float(ungaugedcatchment_list[25][1])
        ungauged_catchment_dict['urbext2000'] = float(ungaugedcatchment_list[26][1])
        ungauged_catchment_dict['urbloc2000'] = float(ungaugedcatchment_list[27][1])
        ungauged_catchment_dict['c'] = float(ungaugedcatchment_list[28][1])
        ungauged_catchment_dict['d1'] = float(ungaugedcatchment_list[29][1])
        ungauged_catchment_dict['d2'] = float(ungaugedcatchment_list[30][1])
        ungauged_catchment_dict['d3'] = float(ungaugedcatchment_list[31][1])
        ungauged_catchment_dict['e'] = float(ungaugedcatchment_list[32][1])
        ungauged_catchment_dict['f'] = float(ungaugedcatchment_list[33][1])
        ungauged_catchment_dict['c_1km'] = float(ungaugedcatchment_list[34][1])
        ungauged_catchment_dict['d1_1km'] = float(ungaugedcatchment_list[35][1])
        ungauged_catchment_dict['d2_1km'] = float(ungaugedcatchment_list[36][1])
        ungauged_catchment_dict['d3_1km'] = float(ungaugedcatchment_list[37][1])
        ungauged_catchment_dict['e_1km'] = float(ungaugedcatchment_list[38][1])
        ungauged_catchment_dict['f_1km'] = float(ungaugedcatchment_list[39][1])

        conn = psycopg2.connect(dbname='feh1', user='jem', host='localhost', )
        cur = conn.cursor()

        columns = ungauged_catchment_dict.keys()
        values = [ungauged_catchment_dict[column] for column in columns]

    if check_if_table_exists('ungauged_catchment'):
        qry = "INSERT INTO ungauged_catchment(%s) VALUES (%s)"
        values.insert(0, 0)
        cur.execute(qry, (AsIs(','.join(columns)), values))
        # print(cur.mogrify(qry, (AsIs(','.join(columns)), tuple(values))))
    else:
        engine = create_engine('postgresql+psycopg2://jem:pswd@localhost:5432/feh1', echo=True)
        data = pd.DataFrame(ungauged_catchment_dict, index=[0])
        data.to_sql('ungauged_catchment', engine)
