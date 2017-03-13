import csv

def importcatchment():
    #reads csv in and puts in it in alist of tuples

    with open('/Users/jem/WINFAP-FEH_v4.1/gore water.csv', 'r') as catchmentfile:
      reader = csv.reader(catchmentfile)
      ungaugedCatchment = list(reader)

    #gets first element in each tuple
    #res_list = [x[0] for x in your_list]
    #print(res_list)
    
    version = ' '.join(ungaugedCatchment[0][1:8])
    catchment = ','.join(ungaugedCatchment[1][2:4])
    centroid = ','.join(ungaugedCatchment[2][2:4])
    area = float(ungaugedCatchment[3][1])
    altBar = float(ungaugedCatchment[4][1])
    aspBar = float(ungaugedCatchment[5][1])
    aspVar = float(ungaugedCatchment[6][1])
    bfiHost = float(ungaugedCatchment[7][1])
    dplBar = float(ungaugedCatchment[8][1])
    dpsBar = float(ungaugedCatchment[9][1])
    farl = float(ungaugedCatchment[10][1])
    fpExt = float(ungaugedCatchment[11][1])
    fpdBar = float(ungaugedCatchment[12][1])
    fpLoc = float(ungaugedCatchment[13][1])
    ldp = float(ungaugedCatchment[14][1])
    propwet = float(ungaugedCatchment[15][1])
    rmed_1h = float(ungaugedCatchment[16][1])
    rmed_1d = float(ungaugedCatchment[17][1])
    rmed_2d = float(ungaugedCatchment[18][1])
    saar = float(ungaugedCatchment[19][1])
    saar4170 = float(ungaugedCatchment[20][1])
    sprHost = float(ungaugedCatchment[21][1])
    urbConc1990 = float(ungaugedCatchment[22][1])
    urbExt1990 = float(ungaugedCatchment[23][1])
    urbLoc1990 = float(ungaugedCatchment[24][1])
    urbConc2000 = float(ungaugedCatchment[25][1])
    urbExt2000 = float(ungaugedCatchment[26][1])
    urbLoc2000 = float(ungaugedCatchment[27][1])
    c = float(ungaugedCatchment[28][1])
    d1 = float(ungaugedCatchment[29][1])
    d2 = float(ungaugedCatchment[30][1])
    d3 = float(ungaugedCatchment[31][1])
    e = float(ungaugedCatchment[32][1])
    f = float(ungaugedCatchment[33][1])
    c_1km = float(ungaugedCatchment[34][1])
    d1_1km = float(ungaugedCatchment[35][1])
    d2_1km = float(ungaugedCatchment[36][1])
    d3_1km = float(ungaugedCatchment[37][1])
    e_1km = float(ungaugedCatchment[38][1])
    f_1km = float(ungaugedCatchment[39][1])

    return ungaugedCatchment