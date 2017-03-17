#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# readziptodict2.py just a dump for all new stuff
# todo: tidy this up into separate functions.  probably becomes the back end stuf to import winfap zip file
import os.path
from os.path import basename
import psycopg2
import sqlite3
import statistics
import zipfile
import math

import lmoments
import yaml
from tkinter import *
from tkinter import filedialog
import os


def getstation(stations, stationNum):
    print(yaml.dump(stations[stationNum], default_flow_style=True))  # yaml prints the dictionary out nicely


def doPrint(stations, stationNum):  # just prints out data for selected station number with L-Moments
    flowdata = [float(i) for i in stations[stationNum]['AM_Flow']]  # convert flow rates from strings to floats
    QMED = statistics.median(flowdata)  # QMED of station
    N = len(flowdata)
    print("Station -> {}".format(stationNum))
    print("Data -> {}".format(stations[stationNum]['AM_Flow']))
    print("QMED -> {}".format(QMED))
    print("N -> {}".format(N))
    LMOM = (lmoments.samlmu(flowdata, 5))
    print("L1: {} L2: {} L3: {} L4: {} L5: {}".format(round(LMOM[0], 2), round(LMOM[1], 2), round(LMOM[2], 2),
                                                      round(LMOM[3], 2), round(LMOM[4], 2)))


if __name__ == "__main__":
    # def getStData():
    # Extracts and loads the files in a zip file to a specified destination
    root = Tk()
    root.withdraw()
    # dbfile=filedialog.askopenfilename(initialdir="", title="choose sqlite file", filetypes=(("sqlite files","*.sqlite"), ("all files","*.*")))
    # db = sqlite3.connect(dbfile)  #connect to database
    # cursor = db.cursor()  #create cursor for SQL commands

    # cursor.execute('CREATE TABLE IF NOT EXISTS am_DETAILS(stationNum INTEGER PRIMARY KEY, yearType TEXT, waterYear TEXT, aMRejected TEXT, fileType TEXT)')
    # cursor.execute('CREATE TABLE IF NOT EXISTS amaxdata(stationNum INTEGER, mon_date DATE, flow REAL)')
    # sets up pathname to winfap zip file
    root.update()
    pathtozip = filedialog.askopenfilename(initialdir="", title="choose winfap zip file",
                                           filetypes=(("zip files", "*.zip"), ("all files", "*.*")))

    with zipfile.ZipFile(pathtozip, 'r') as ze:
        ze.extractall()  # just unzip to same directory as zipfile.
# sets up path to unzipped winfap files
pathtounzipped = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(pathtozip))[0])
db = psycopg2.connect("dbname='feh1' user='jem' host='localhost'")  # connect to database
cursor = db.cursor()  # create cursor for SQL commands

cursor.execute('CREATE TABLE IF NOT EXISTS am_DETAILS(stationNum INTEGER PRIMARY KEY, yearType VARCHAR, '
               'waterYear VARCHAR, aMRejected VARCHAR)')
cursor.execute('CREATE TABLE IF NOT EXISTS amaxdata(stationNum INTEGER, mon_date DATE, flow REAL)')

for subdir, dirs, files in os.walk(pathtounzipped):  # to be replaced with user selected subdirectory
    for name in files:
        stations = {}
        if name.endswith(".AM"):
            with open(os.path.join(subdir, name), 'r') as input_data:

                stationNum = None;
                aMDetails = [];
                aMDetailsAll = None;
                aMRejected = [];
                aMValues = [];
                flag = 'END';
                yearType = []
                waterYear = [];
                aMRejectedAll = [];
                aMFlow = [];
                aMmon_date = [];
                aMSt_num = [];
                stationnums = []

                for line in input_data:
                    if line.strip() == '[END]':
                        flag = 'END'
                    # move this block to a different database table "AMAX_Data" with station number as key field
                    if flag == 'AM Values':
                        # aMValues.append([_.strip() for _ in line.split(',')])#splits AM data into date, flow rate and stage
                        current = line.replace(' ', '').split(',')[
                            1]  # gets the flow data from each line of AM values and puts in a new list
                        mon_date = line.replace(' ', '').split(',')[0]

                        stationnums.append(stationNum)
                        aMFlow.append(current)
                        aMmon_date.append(mon_date)

                        SQLinsert = "INSERT INTO amaxdata (stationNum, mon_date, flow) VALUES (%s,%s,%s);"
                        data = (stationNum, mon_date, current,)
                        cursor.execute(SQLinsert, data)
                        db.commit()

                        # aMValues=zip(stationnums, aMmon_date, aMFlow)#makes lists into a list of tuples for sqlite executemany
                        # cursor.execute('INSERT INTO amaxdata(stationNum, mon_date, flow) VALUES(?,?,?)',(stationNum, mon_date, current))
                    # end of block to move to "AMAX_Data" table in db
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
            cursor.execute(SQLinsert, data)
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
            # a function that gets the file path to the FEH CD-ROM csv file and imports the unguaged catchment. Might be better as a class.


        elif name.endswith(
                ".CD3"):  # parse data from CD3 file.  All information describing the gauging station and related catchment

            with open(os.path.join(subdir, name), 'r') as input_data:

                cD3 = '.CD3';
                ver = '';
                stName = '';
                Loc = '';
                nomArea = 0;
                nomNGRE = None;
                nomNGRN = None;
                iHDTMNGRE = None;
                iHDTMNGRN = None;
                centroidNGRE = None;
                centroidNGRN = None;
                dTMArea = 0;
                altBar = None;
                aspBar = None;
                aspVar = None;
                bFIHost = None;
                dPLBar = None;
                dPSBar = None;
                farl = None;
                fPExt = None;
                lDP = None;
                propWet = None;
                rmed1H = None;
                rmed1D = None;
                rmed_2D = None;
                saar = None;
                saar_4170 = None;
                sprHost = None;
                urbConc1990 = None;
                urbExt1990 = None;
                urbLoc1990 = None;
                urbConc2000 = None;
                urbExt2000 = None;
                urbLoc2000 = None;
                suitQMED = False;
                suitPooling = False;
                comments = ''
                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS cd3_data(stationNum INT, ver REAL, stName VARCHAR, Loc VARCHAR, nomArea REAL, nomNGRE INT,'
                    'nomNGRN INT, iHDTMNGRE INT, iHDTMNGRN INT, centroidNGRE INT, centroidNGRN INT, dTMArea REAL, altBar INT, aspBar INT, aspVar REAL, bFIHost REAL,'
                    'dPLBar REAL, dPSBar REAL, farl REAL, fPExt REAL, lDP REAL, propWet REAL, rmed1H REAL, rmed1D REAL, rmed2D REAL, saar INT, saar_1470 INT,'
                    'sprHost REAL, urbConc1990 REAL, urbExt1990 REAL, urbLoc1990 REAL, urbConc2000 REAL, urbExt2000 REAL, urbLoc2000 REAL, suitQMED BOOLEAN, suitPooling BOOLEAN,'
                    'comments VARCHAR)')
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

                SQLinsert = "INSERT INTO cd3_data(stationNum, ver, stName, Loc, nomArea, nomNGRE, nomNGRN, iHDTMNGRE, iHDTMNGRN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                data = (stationNum, ver, stName, Loc, nomArea, nomNGRE, nomNGRN, iHDTMNGRE, iHDTMNGRN)
                cursor.execute(SQLinsert, data)
                db.commit()
