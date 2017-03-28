#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# todo: tidy this up into separate functions.  probably becomes the back end stuff to import winfap zip file
import psycopg2

import zipfile

from tkinter import *
from tkinter import filedialog
import os


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

                            SQLinsert = "INSERT INTO amaxdata (stationNum, mon_date, flow) VALUES (%s,%s,%s);"
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
