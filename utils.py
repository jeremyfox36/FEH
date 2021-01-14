import os
import statistics
import zipfile
from math import sqrt, pow, exp
from tkinter import filedialog

import psycopg2
import psycopg2.extras


def check_if_table_exists(table_name: str):

    db = psycopg2.connect("dbname='feh1' user='jem' host='localhost'")
    cur = db.cursor()

    cur.execute("SELECT EXISTS (SELECT * FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND c.relname =%s)", (table_name,))

    exists = cur.fetchone()

    return exists[0]


# def import_catchment():
#
#     # todo: ask for user file to be uploaded in .CD3 format
#     # todo: check program.py for flask procedure hints
#     # this function should return data to the database under the user account
#     # may be redundant for the web app
#
#     with open('/Users/jem/WINFAP-FEH_v4.1/FEH/FEH/gore water.csv', 'r') as catchmentfile:
#         reader = csv.reader(catchmentfile)
#         ungaugedcatchment_list = list(reader)
#         ungauged_catchment_dict = {}
#         # later the name of ungauged_catchment will be changed according to user
#         # input so that it can be saved to the users database
#
#         ungauged_catchment_dict['catchment_name'] = 'test' # change to user id or something similar and index on this
#         ungauged_catchment_dict['version'] = ' '.join(ungaugedcatchment_list[0][1:8])
#         ungauged_catchment_dict['catchment'] = ','.join(ungaugedcatchment_list[1][2:4])
#         ungauged_catchment_dict['centroid'] = ','.join(ungaugedcatchment_list[2][2:4])
#         ungauged_catchment_dict['centroid_e'] = int(ungaugedcatchment_list[2][2])
#         ungauged_catchment_dict['centroid_n'] = int(ungaugedcatchment_list[2][3])
#         ungauged_catchment_dict['area'] = float(ungaugedcatchment_list[3][1])
#         ungauged_catchment_dict['altbar'] = float(ungaugedcatchment_list[4][1])
#         ungauged_catchment_dict['aspbar'] = float(ungaugedcatchment_list[5][1])
#         ungauged_catchment_dict['aspvar'] = float(ungaugedcatchment_list[6][1])
#         ungauged_catchment_dict['bfihost'] = float(ungaugedcatchment_list[7][1])
#         ungauged_catchment_dict['dplbar'] = float(ungaugedcatchment_list[8][1])
#         ungauged_catchment_dict['dpsbar'] = float(ungaugedcatchment_list[9][1])
#         ungauged_catchment_dict['farl'] = float(ungaugedcatchment_list[10][1])
#         ungauged_catchment_dict['fpext'] = float(ungaugedcatchment_list[11][1])
#         ungauged_catchment_dict['fpdbar'] = float(ungaugedcatchment_list[12][1])
#         ungauged_catchment_dict['fploc'] = float(ungaugedcatchment_list[13][1])
#         ungauged_catchment_dict['ldp'] = float(ungaugedcatchment_list[14][1])
#         ungauged_catchment_dict['propwet'] = float(ungaugedcatchment_list[15][1])
#         ungauged_catchment_dict['rmed_1h'] = float(ungaugedcatchment_list[16][1])
#         ungauged_catchment_dict['rmed_1d'] = float(ungaugedcatchment_list[17][1])
#         ungauged_catchment_dict['rmed_2d'] = float(ungaugedcatchment_list[18][1])
#         ungauged_catchment_dict['saar'] = float(ungaugedcatchment_list[19][1])
#         ungauged_catchment_dict['saar4170'] = float(ungaugedcatchment_list[20][1])
#         ungauged_catchment_dict['sprhost'] = float(ungaugedcatchment_list[21][1])
#         ungauged_catchment_dict['urbconc1990'] = float(ungaugedcatchment_list[22][1])
#         ungauged_catchment_dict['urbext1990'] = float(ungaugedcatchment_list[23][1])
#         ungauged_catchment_dict['urbloc1990'] = float(ungaugedcatchment_list[24][1])
#         ungauged_catchment_dict['urbconc2000'] = float(ungaugedcatchment_list[25][1])
#         ungauged_catchment_dict['urbext2000'] = float(ungaugedcatchment_list[26][1])
#         ungauged_catchment_dict['urbloc2000'] = float(ungaugedcatchment_list[27][1])
#         ungauged_catchment_dict['c'] = float(ungaugedcatchment_list[28][1])
#         ungauged_catchment_dict['d1'] = float(ungaugedcatchment_list[29][1])
#         ungauged_catchment_dict['d2'] = float(ungaugedcatchment_list[30][1])
#         ungauged_catchment_dict['d3'] = float(ungaugedcatchment_list[31][1])
#         ungauged_catchment_dict['e'] = float(ungaugedcatchment_list[32][1])
#         ungauged_catchment_dict['f'] = float(ungaugedcatchment_list[33][1])
#         ungauged_catchment_dict['c_1km'] = float(ungaugedcatchment_list[34][1])
#         ungauged_catchment_dict['d1_1km'] = float(ungaugedcatchment_list[35][1])
#         ungauged_catchment_dict['d2_1km'] = float(ungaugedcatchment_list[36][1])
#         ungauged_catchment_dict['d3_1km'] = float(ungaugedcatchment_list[37][1])
#         ungauged_catchment_dict['e_1km'] = float(ungaugedcatchment_list[38][1])
#         ungauged_catchment_dict['f_1km'] = float(ungaugedcatchment_list[39][1])
#
#         conn = psycopg2.connect(dbname='feh1', user='jem', host='localhost', )
#         cur = conn.cursor()
#
#         columns = ungauged_catchment_dict.keys()
#         values = [ungauged_catchment_dict[column] for column in columns]
#
#     if check_if_table_exists('ungauged_catchment'):
#         qry = "INSERT INTO ungauged_catchment(%s) VALUES (%s)"
#         values.insert(0, 0)
#         cur.execute(qry, (AsIs(','.join(columns)), values))
#         # print(cur.mogrify(qry, (AsIs(','.join(columns)), tuple(values))))
#     else:
#         engine = create_engine('postgresql+psycopg2://jem:flanagan@localhost:5432/feh1', echo=True)
#         data = pd.DataFrame(ungauged_catchment_dict, index=[0])
#         data.to_sql('ungauged_catchment', engine)

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# todo: tidy this up into separate functions.  probably becomes the back end stuff to import winfap zip file


def clear_old_data():
    db_to_clear = psycopg2.connect("dbname='feh1' user='jem' host='localhost'")
    curs = db_to_clear.cursor()
    curs.execute('DELETE FROM am_details')
    print('Done')
    curs.execute('DELETE FROM amaxdata')
    print('Done')
    curs.execute('DELETE FROM cd3_data')
    print('Done')
    db_to_clear.commit()
    return None


def unzip():
    pathtozip = filedialog.askopenfilename(initialdir="", title="choose winfap zip file",
                                           filetypes=(("zip files", "*.zip"), ("all files", "*.*")))

    with zipfile.ZipFile(pathtozip, 'r') as ze:
        ze.extractall()

    return pathtozip


def parse_zipfile():
    """
    Take WINFAP zip file and parse files into a postgresql database
    """

    db = psycopg2.connect("dbname='feh1' user='jem' host='localhost'")
    c = db.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS am_DETAILS(stationNum INTEGER PRIMARY KEY, yearType VARCHAR, '
              'waterYear VARCHAR, aMRejected VARCHAR)')
    c.execute('CREATE TABLE IF NOT EXISTS amaxdata(stationNum INTEGER, mon_date DATE, flow REAL)')

    pathtozip = unzip()
    pathtounzipped = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(pathtozip))[0])

    for subdir, dirs, files in os.walk(pathtounzipped):  # to be replaced with user selected subdirectory
        for name in files:
            # stations = {}
            if name.endswith(".AM"):
                with open(os.path.join(subdir, name), 'r') as input_data:

                    stationNum = None
                    aMDetails = []
                    aMDetailsAll = None
                    aMRejected = []
                    aMValues = []
                    flag = 'END'
                    yearType = []
                    waterYear = []
                    aMRejectedAll = []
                    aMFlow = []
                    aMmon_date = []
                    aMSt_num = []
                    stationnums = []

                    for line in input_data:
                        if line.strip() == '[END]':
                            flag = 'END'

                        if flag == 'AM Values':
                            # gets the flow data from each line of AM values and puts in a new list
                            current = line.replace(' ', '').split(',')[1]
                            mon_date = line.replace(' ', '').split(',')[0]

                            stationnums.append(stationNum)
                            aMFlow.append(current)
                            aMmon_date.append(mon_date)

                            SQLinsert = "INSERT INTO amaxdata (stationNum, mon_date, flow) VALUES (%s, %s, %s);"
                            data = (stationNum, mon_date, current,)
                            c.execute(SQLinsert, data)
                            db.commit()

                        elif line.strip() == '[STATION NUMBER]':
                            stationNum = next(input_data).rstrip(
                                '\n')  # next line after the heading is always the station number
                        elif line.strip() == '[AM Details]':
                            aMDetailsAll = next(input_data).strip()
                            aMDetails = aMDetailsAll.replace(' ', ',')
                            yearType = aMDetails.split(',')[2]
                            waterYear = aMDetails.split(',')[4]
                        elif line.strip() == '[AM Rejected]':
                            aMRejectedAll = next(input_data).strip()
                            aMRejected = aMRejectedAll.split(',')
                        elif line.strip() == '[AM Values]':
                            flag = 'AM Values'
                        else:
                            continue

                input_data.close()
                SQLinsert = "INSERT INTO am_Details (stationNum, yearType, waterYear, aMRejected) VALUES (%s,%s,%s,%s) ON CONFLICT (stationNum) DO NOTHING;"
                data = (stationNum, yearType, waterYear, aMRejected)
                c.execute(SQLinsert, data)
                db.commit()

                # stations[stationNum] = {'AM_Details': {'Year_Type': yearType, 'Water_Year': waterYear},
                # 'AM_Rejected': aMRejected,
                # 'AM_Values': aMValues, 'AM_Flow': aMFlow}
                # .CD3 file data to dictionary
                # 'File_Format': {'Type': cD3, 'Version': version}, 'CDS_Details': {'Name': stName, 'Location': location,
                # 'Nominal_Area': nomArea, 'Nominal_NGR': nomNGR}, 'Decsriptors': {'IHDTM_NGR': iHDTMNGR, 'Centroid_NGR': centroidNGR, 'DTM_Area': dTMArea,
                # 'AltBar': altBar, 'AspBar': aspBar, 'AspVar': aspVar, 'BFIHost': bFIHost, 'DPLBar': dPLBar, 'DPSBar': dPSBar, 'FARL': farl, 'FPExt': fPExt,
                # 'LDP': lDP, 'PropWet': propWet, 'RMED_1H': rmed1H, 'RMED_1D': rmed1D, 'RMED_2D': rmed_2D, 'SAAR': saar, 'SAAR_4170': saar_4170, 'SPRHOST': sprHost,
                # 'URBCONC1990': urbConc1990, 'URBEXT1990': urbExt1990, 'URBLOC1990': urbLoc1990, 'URBCONC2000': urbConc2000, 'URBEXT2000': urbExt2000,
                # 'URBLOC2000': urbLoc2000}, 'Suitability': {'QMED': suitQMED, 'Pooling': suitPooling}, 'COMMENTS': comments}
                # return stations

            elif name.endswith(
                    ".CD3"):
                # parse data from CD3 file.  All information describing the gauging station and related catchment info

                with open(os.path.join(subdir, name), 'r') as input_data:

                    cD3 = '.CD3'
                    ver = ''
                    stName = ''
                    Loc = ''
                    nomArea = None
                    nomNGRE = None
                    nomNGRN = None
                    iHDTMNGRE = None
                    iHDTMNGRN = None
                    centroidNGRE = None
                    centroidNGRN = None
                    dTMArea = None
                    altBar = None
                    aspBar = None
                    aspVar = None
                    bFIHost = None
                    dPLBar = None
                    dPSBar = None
                    farl = None
                    fPExt = None
                    lDP = None
                    propWet = None
                    rmed1H = None
                    rmed1D = None
                    rmed_2D = None
                    saar = None
                    saar_4170 = None
                    sprHost = None
                    urbConc1990 = None
                    urbExt1990 = None
                    urbLoc1990 = None
                    urbConc2000 = None
                    urbExt2000 = None
                    urbLoc2000 = None
                    suitQMED = False
                    suitPooling = False
                    station_comments = None
                    catchment_comments = None
                    qmed_comments = None
                    pooling_comments = None

                    c.execute(
                        'CREATE TABLE IF NOT EXISTS cd3_data(stationNum INT, ver REAL, stName VARCHAR, Loc VARCHAR, nomArea REAL, nomNGRE INT,'
                        'nomNGRN INT, iHDTMNGRE INT, iHDTMNGRN INT, centroidNGRE INT, centroidNGRN INT, dTMArea REAL, altBar INT, aspBar INT, aspVar REAL, bFIHost REAL,'
                        'dPLBar REAL, dPSBar REAL, farl REAL, fPExt REAL, lDP REAL, propWet REAL, rmed1H REAL, rmed1D REAL, rmed2D REAL, saar INT, saar_1470 INT,'
                        'sprHost REAL, urbConc1990 REAL, urbExt1990 REAL, urbLoc1990 REAL, urbConc2000 REAL, urbExt2000 REAL, urbLoc2000 REAL, suitQMED BOOLEAN, suitPooling BOOLEAN,'
                        'station_comments VARCHAR, catchment_comments VARCHAR, qmed_comments VARCHAR, pooling_comments VARCHAR)')

                    for line in input_data:
                        splitline = line.split(',')
                        if splitline[0] == 'VERSION':
                            ver = splitline[1].strip()
                        elif splitline[0] == 'NAME':
                            stName = splitline[1].strip()
                        elif splitline[0] == 'LOCATION':
                            Loc = splitline[1].strip()
                        elif splitline[0] == 'NOMINAL AREA':
                            nomArea = float(splitline[1].strip())
                        elif splitline[0] == 'NOMINAL NGR':
                            nomNGRE = int(splitline[1].strip())
                            nomNGRN = int(splitline[2].strip())
                        elif splitline[0] == 'IHDTM NGR':
                            iHDTMNGRE = int(splitline[2].strip())
                            iHDTMNGRN = int(splitline[3].strip())
                        elif splitline[0] == 'CENTROID NGR':
                            centroidNGRE = int(splitline[2].strip())
                            centroidNGRN = int(splitline[3].strip())
                        elif splitline[0] == 'DTM AREA':
                            dTMArea = float(splitline[1].strip())
                        elif splitline[0] == 'ALTBAR':
                            altBar = splitline[1].strip()
                        elif splitline[0] == 'ASPBAR':
                            aspBar = splitline[1].strip()
                        elif splitline[0] == 'ASPVAR':
                            aspVar = splitline[1].strip()
                        elif splitline[0] == 'BFIHOST':
                            bFIHost = splitline[1].strip()
                        elif splitline[0] == 'DPLBAR':
                            dPLBar = splitline[1].strip()
                        elif splitline[0] == 'DPSBAR':
                            dPSBar = splitline[1].strip()
                        elif splitline[0] == 'FARL':
                            farl = splitline[1].strip()
                        elif splitline[0] == 'FPEXT':
                            fPExt = splitline[1].strip()
                        elif splitline[0] == 'LDP':
                            lDP = splitline[1].strip()
                        elif splitline[0] == 'PROPWET':
                            propWet = splitline[1].strip()
                        elif splitline[0] == 'RMED-1H':
                            rmed1H = splitline[1].strip()
                        elif splitline[0] == 'RMED-1D':
                            rmed1D = splitline[1].strip()

                        elif splitline[0] == 'RMED-2D':
                            rmed_2D = splitline[1].strip()
                        elif splitline[0] == 'SAAR':
                            saar = splitline[1].strip()
                        elif splitline[0] == 'SAAR4170':
                            saar_4170 = splitline[1].strip()

                        elif splitline[0] == 'URBCONC1990':
                            urbConc1990 = splitline[1].strip()
                        elif splitline[0] == 'URBEXT1990':
                            urbExt1990 = splitline[1].strip()
                        elif splitline[0] == 'URBLOC1990':
                            urbLoc1990 = splitline[1].strip()

                        elif splitline[0] == 'URBCONC2000':
                            urbConc2000 = splitline[1].strip()
                        elif splitline[0] == 'URBEXT2000':
                            urbExt2000 = splitline[1].strip()
                        elif splitline[0] == 'URBLOC2000':
                            urbLoc2000 = splitline[1].strip()

                        elif splitline[0] == 'QMED':
                            suitQMED = splitline[1].strip()
                        elif splitline[0] == 'POOLING':
                            suitPooling = splitline[1].strip()

                        elif splitline[0] == 'STATION':
                            station_comments = line.split(',', 1)[1].strip()
                        elif splitline[0] == 'CATCHMENT':
                            catchment_comments = line.split(',', 1)[1].strip()
                        elif splitline[0] == 'Qmed Suitability':
                            qmed_comments = line.split(',', 1)[1].strip()
                        elif splitline[0] == 'Pooling Suitability':
                            pooling_comments = line.split(',', 1)[1].strip()

                    SQLinsert = "INSERT INTO cd3_data(stationNum, ver, stName, Loc, nomArea, nomNGRE, nomNGRN, iHDTMNGRE, iHDTMNGRN, centroidNGRE, " \
                                "centroidNGRN, dTMArea, altBar, aspBar, aspVar, bFIHost, dPLBar, dPSBar, farl, fPExt, lDP, propWet, rmed1H, rmed1D, " \
                                "rmed2D, saar, saar_1470, sprHost, urbConc1990, urbExt1990, urbLoc1990, urbConc2000, urbExt2000, urbLoc2000, suitQMED," \
                                " suitPooling, station_comments, catchment_comments, qmed_comments, pooling_comments) " \
                                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

                    data = (stationNum, ver, stName, Loc, nomArea, nomNGRE, nomNGRN, iHDTMNGRE, iHDTMNGRN, centroidNGRE,
                            centroidNGRN, dTMArea, altBar, aspBar,
                            aspVar, bFIHost, dPLBar, dPSBar, farl, fPExt, lDP, propWet, rmed1H, rmed1D, rmed_2D, saar,
                            saar_4170, sprHost, urbConc1990, urbExt1990,
                            urbLoc1990, urbConc2000, urbExt2000, urbLoc2000, suitQMED, suitPooling, station_comments,
                            catchment_comments, qmed_comments, pooling_comments)
                    c.execute(SQLinsert, data)
                    db.commit()


def sdm_from_db():
    
    total_years_data = 0  # keeps count of number of years data for formation of pooling group
    pooling_group = {}

    conn = psycopg2.connect(dbname='feh1', user='jem', host='localhost', )
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    dict_cur.execute(
        "SELECT catchment_name, cd3_data.stationnum,"
        "sqrt((3.2::DOUBLE PRECISION * (((ln(ungauged_catchment.area::DOUBLE PRECISION) - ln(cd3_data.dtmarea::DOUBLE PRECISION)) / 1.28::DOUBLE PRECISION) ^ 2::DOUBLE PRECISION))"
        "+(0.5::DOUBLE PRECISION * (((ln(ungauged_catchment.saar::DOUBLE PRECISION) - ln(cd3_data.saar::DOUBLE PRECISION)) / 0.37::DOUBLE PRECISION) ^ 2::DOUBLE PRECISION))"
        "+(0.1::DOUBLE PRECISION * (((ungauged_catchment.farl - cd3_data.farl) / 0.05::DOUBLE PRECISION) ^ 2::DOUBLE PRECISION))"
        "+(0.2::DOUBLE PRECISION * (((ungauged_catchment.fpext - cd3_data.fpext) / 0.04::DOUBLE PRECISION) ^ 2::DOUBLE PRECISION)))"
        " AS SDM FROM ungauged_catchment, cd3_data WHERE cd3_data.suitpooling = TRUE ORDER BY SDM")

    rows = dict_cur.fetchall()

    # as per EA Science Report: SC050050, a default pooling group with 500 years of
    # AMAX data is formed (total_years_data<=500).
    # FEH procedures state that it should be 5T, whereT is the desired return period.
    # later version could include the option to adjust the pooling group size to 5T

    for row in rows:
        if total_years_data <= 500:
            rd_cur = conn.cursor()
            st = row['stationnum']
            rd_cur.execute('SELECT flow FROM amaxdata WHERE stationnum=%s', (st,))

            amaxdata = rd_cur.fetchall()

            amaxdata = [flow[0] for flow in amaxdata]  # changes list of tuples in tuple
            row['amaxdata'] = amaxdata
            row['amaxcount'] = len(amaxdata)
            row['qmed'] = round(statistics.median(amaxdata), 2)
            pooling_group[row['stationnum']] = row
            del (row['stationnum'])
            total_years_data += len(amaxdata)

        else:
            break

    return pooling_group


def catchment_distance(ungauged_e, ungauged_n, donor_e, donor_n):
    """
    Calculate the distance in km between two ordnance survey grid references
    
    Keyword arguments:
    ungauged_e (int): easting of the ungauged catchment
    ungauged_n (int): northing of the ungauged catchment
    donor_e (int: easting of the donor catchment
    donor_n (int): northing of the donor catchment
    
    Returns:
    distance (int): distance between points
    """
    # takes Ordnance Survey grid reference and returns the distance between the points in km
    # calculates distance between catchment centroids
    # grid refs are six figures, therefore the distance will be in m

    east_distance = abs(pow((donor_e - ungauged_e), 2))
    north_distance = abs(pow((donor_n - ungauged_n), 2))

    distance = sqrt(east_distance + north_distance)/1000

    return distance


def qmed_catchment_descriptors(area, saar, farl, bfihost):
    """
    Estimate the QMED (CUMECS) from catchment descriptors
    
    Keyword arguments:
    area (float): area of the catchment in km^2
    saar: (float):  standard average annual rainfall in mm
    farl (float): Flood Attenuation by Reservoirs and Lakes index
    bfihost (float): base flow index. A measure of catchment responsiveness derived using the 29-class Hydrology Of Soil Types (HOST) classification
    
    Returns:
    qmed_cds (float): catchment QMED estimate
    """

    qmed_cds = 8.3062 * pow(area, 0.851) * pow(0.1536, 1000/saar) * pow(farl, 3.4451) * pow(0.046, pow(bfihost, 2))

    return qmed_cds


def donor_adjusted_qmed(distance, qmed_s_cds, qmed_g_obs, qmed_g_cds):
    """
    Calculate modified qmed adjustment factor for donor catchment (EA Science Report: SC050050)
    where:
    target site (s)
    donor site (g)
    obs - observed
    cds - from catchment descriptors
    
    Keyword arguments:
    qmed_g_obs (float): observed qmed
    qmed_g_cds (float): qmed of gauged site based on catchment descriptors
    qmed_s_cds (float): qmed of ungauged site based on catchment descriptors
    
    Return:
    round(qmed_s_adj,2) (decimal): adjusted QMED rounded to 2 decimal places
    """

    a_sg = round(0.4598 * exp(-0.02 * distance) + (1 - 0.4598) * exp(-0.4785 * distance), 2)

   
    qmed_s_adj = qmed_s_cds * pow(qmed_g_obs/qmed_g_cds, a_sg)

    return round(qmed_s_adj,2)



