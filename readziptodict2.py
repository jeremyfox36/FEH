#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#readziptodict2.py
import os.path
from os.path import basename
import sqlite3
import statistics
import zipfile

import lmoments
import yaml
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import os

def getstation(stations, stationNum):
    print (yaml.dump(stations[stationNum], default_flow_style=True))#yaml prints the dictionary out nicely
    
def doPrint(stations, stationNum):#just prints out data for selected station number with L-Moments
    flowdata = [float(i) for i in stations[stationNum]['AM_Flow']]#convert flow rates from strings to floats
    QMED = statistics.median(flowdata)#QMED of station
    N = len(flowdata)
    print ("Station -> {}".format(stationNum))
    print ("Data -> {}".format(stations[stationNum]['AM_Flow']))
    print("QMED -> {}".format(QMED))
    print("N -> {}".format(N))
    LMOM = (lmoments.samlmu(flowdata,5))
    print ("L1: {} L2: {} L3: {} L4: {} L5: {}".format(round(LMOM[0],2), round(LMOM[1],2), round(LMOM[2],2), round(LMOM[3],2), round(LMOM[4],2)))

if __name__ == "__main__":
#def getStData():    
#Extracts and loads the files in a zip file to a specified destination
    root = Tk()
    root.withdraw()
    dbfile=filedialog.askopenfilename(initialdir="", title="choose sqlite file", filetypes=(("sqlite files","*.sqlite"), ("all files","*.*")))
    db = sqlite3.connect(dbfile)  #connect to database
    cursor = db.cursor()  #create cursor for SQL commands
    
    cursor.execute('CREATE TABLE IF NOT EXISTS am_DETAILS(stationNum INTEGER PRIMARY KEY, yearType TEXT, waterYear TEXT, aMRejected TEXT, fileType TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS amaxdata(stationNum INTEGER, mon_date DATE, flow REAL)')
    #sets up pathname to winfap zip file
    pathtozip = filedialog.askopenfilename(initialdir="", title="choose winfap zip file", filetypes=(("zip files", "*.zip"), ("all files", "*.*")))

    with zipfile.ZipFile(pathtozip,'r') as ze:
        ze.extractall()#just unzip to same directory as zipfile.
root.update()
#sets up path to unzipped winfap files
pathtounzipped = os.path.join(os.path.dirname(pathtozip), os.path.splitext(os.path.basename(pathtozip))[0])

for subdir, dirs, files in os.walk(pathtounzipped):#to be replaced with user selected subdirectory
    for name in files:
        stations = {}
        if name.endswith(".AM"):
            with open(os.path.join(subdir, name), 'r') as input_data:

                stationNum = None; aMDetails = []; aMDetailsAll = None; aMRejected = []; aMValues = []; flag = 'END'; yearType = []
                waterYear = []; aMRejectedAll = []; aMFlow = []; aMmon_date = []; aMSt_num = []; stationnums = []

                for line in input_data:
                    if line.strip() == '[END]':
                            flag = 'END'
                    #move this block to a different database table "AMAX_Data" with station number as key field        
                    if flag == 'AM Values':
                        #aMValues.append([_.strip() for _ in line.split(',')])#splits AM data into date, flow rate and stage
                        current = line.replace(' ','').split(',')[1]#gets the flow data from each line of AM values and puts in a new list
                        mon_date = line.replace(' ','').split(',')[0]

                        stationnums.append(stationNum)
                        aMFlow.append(current)
                        aMmon_date.append(mon_date)
                        aMValues=zip(stationnums, aMmon_date, aMFlow)#makes lists into a list of tuples for sqlite executemany
                        #cursor.execute('INSERT INTO amaxdata(stationNum, mon_date, flow) VALUES(?,?,?)',(stationNum, mon_date, current))
                    #end of block to move to "AMAX_Data" table in db
                    elif line.strip() == '[STATION NUMBER]':
                        stationNum = next(input_data).rstrip('\n')#next line after the heading is always the station number
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
                    #add conditionals for CD3 data to be associated with AMAX data

        #elif name.endswith(".CD3"):#parse data from CD3 file.  All information describing the gauging station and related catchment
            
            #with open(os.path.join(subdir, name), 'r') as input_data:
                
                #cD3 = '.CD3'; version = ''; stName = ''; location = ''; nomArea = 0; nomNGR = (); iHDTMNGR = (); centroidNGR = (); dTMArea = 0
                #altBar = 0; aspBar = 0; aspVar = 0; bFIHost = 0; dPLBar = 0; dPSBar = 0; farl = 0; fPExt = 0; lDP = 0; propWet = 0; rmed1H = 0;
                #rmed1D = 0; rmed_2D = 0; saar = 0; saar_4170 = 0; sprHost = 0; urbConc1990 = 0; urbExt1990 = 0; urbLoc1990 = 0; urbConc2000 = 0;
                #urbExt2000 = 0; urbLoc2000 = 0; suitQMED = False; suitPooling = False; comments = ''
                
                #for line in input_data:
                    #if line.split(',')[0] == 'VERSION':
                        #version = line.strip().split(',')[0]
                    #elif line.split(',')[0] == 'NAME':
                        #stName = line.split(',')[1]
                    #else:
                        #pass
            if aMValues:
                cursor.executemany('INSERT INTO amaxdata(stationNum, mon_date, flow) VALUES(?,?,?)',
                                   (aMValues))
                db.commit()
            input_data.close()
            
            stations[stationNum] = {'AM_Details': {'Year_Type': yearType, 'Water_Year': waterYear}, 'AM_Rejected': aMRejected,
            'AM_Values': aMValues, 'AM_Flow': aMFlow}
            #.CD3 file data to dictionary
            #'File_Format': {'Type': cD3, 'Version': version}, 'CDS_Details': {'Name': stName, 'Location': location,
            #'Nominal_Area': nomArea, 'Nominal_NGR': nomNGR}, 'Decsriptors': {'IHDTM_NGR': iHDTMNGR, 'Centroid_NGR': centroidNGR, 'DTM_Area': dTMArea,
            #'AltBar': altBar, 'AspBar': aspBar, 'AspVar': aspVar, 'BFIHost': bFIHost, 'DPLBar': dPLBar, 'DPSBar': dPSBar, 'FARL': farl, 'FPExt': fPExt,
            #'LDP': lDP, 'PropWet': propWet, 'RMED_1H': rmed1H, 'RMED_1D': rmed1D, 'RMED_2D': rmed_2D, 'SAAR': saar, 'SAAR_4170': saar_4170, 'SPRHOST': sprHost,
            #'URBCONC1990': urbConc1990, 'URBEXT1990': urbExt1990, 'URBLOC1990': urbLoc1990, 'URBCONC2000': urbConc2000, 'URBEXT2000': urbExt2000,
            #'URBLOC2000': urbLoc2000}, 'Suitability': {'QMED': suitQMED, 'Pooling': suitPooling}, 'COMMENTS': comments}
#return stations
#a function that gets the file path to the FEH CD-ROM csv file and imports the unguaged catchment. Might be better as a class.