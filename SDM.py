import math
from pprint import pprint

import numpy as np
from collections import OrderedDict
import psycopg2
import psycopg2.extras
from FEH import importcatchment


# calculates the distance measure based on catchment descriptors.  i is imported ungauged catchment of interest,
# j is gauged catchment from suitable for pooling file


def sdm():

    ungauged_catchment = importcatchment.import_catchment()

    areai = ungauged_catchment.areai
    saari = ungauged_catchment.saari
    farli = ungauged_catchment.farli
    fpexti = ungauged_catchment.fpexti

    conn = psycopg2.connect(dbname='feh1', user='jem', host='localhost', )
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    dict_cur.execute(
        'SELECT cd3_data.stationNum, cd3_data.dTMArea, cd3_data.saar, cd3_data.farl, cd3_data.fPExt FROM cd3_data '
        'WHERE cd3_data.suitPooling=TRUE')

    rows = dict_cur.fetchall()
    pooling_group = {}

    for row in rows:

        if (row['dtmarea'] or row['saar'] or row['farl'] or row['fpext']) is None:
            row['sdm'] = None
            pooling_group[row['stationnum']] = row
        else:

            areadiff = math.pow(((np.log(areai) - np.log(row['dtmarea'])) / 1.28), 2)

            saardiff = math.pow(((np.log(saari) - np.log(row['saar'])) / 0.37), 2)

            farldiff = math.pow((farli - row['farl']) / 0.05, 2)

            fpextdiff = math.pow((fpexti - row['fpext']) / 0.04, 2)

            row['sdm'] = math.sqrt((3.2 * areadiff) + (0.5 * saardiff) + (0.1 * farldiff) + (0.2 * fpextdiff))

            nt_cur = conn.cursor()
            st = row['stationnum']
            nt_cur.execute('SELECT flow FROM amaxdata WHERE stationnum=%s', (st,))

            amaxdata = nt_cur.fetchall()
            amaxdata = [flow[0] for flow in amaxdata]
            row['amaxdata'] = amaxdata

            pooling_group[row['stationnum']] = row
            all_stations_sdm = OrderedDict(pooling_group)

    return all_stations_sdm

    # todo: make a new version  with select query changed to sdm_query and check speed of python vs SQL
    # todo: add number of years data (count of amax list) to total
    # todo: remove entry from dict
    # todo: do until number of years = 500
