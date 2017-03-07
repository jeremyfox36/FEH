import math
import numpy as np

# calculates the distance measure based on catchment descriptors.  i is imported ungauged catchment of interest, j is gauged catchment from suitable for pooling file
#check that input to pooling group have 'suitable for pooling = true'
#combine groups of varaibles into single algorithm - used lots of intermediates to debug equation
def SDM (areai, areaj, saari, saarj, farli, farlj, fpexti, fpextj):

    lnareai = np.log(areai)
    lnareaj = np.log(areaj)
    lnsaari = np.log(saari)
    lnsaarj = np.log(saarj)

    areadiff = (lnareai-lnareaj)/1.28
    saardiff = (lnsaari-lnsaarj)/0.37
    farldiff = (farli-farlj)/0.05
    fpextdiff = (fpexti-fpextj)/0.04

    areapower = math.pow(areadiff,2)
    saarpower = math.pow(saardiff,2)
    farlpower = math.pow(farldiff,2)
    fpextpower = math.pow(fpextdiff,2)


    distance = math.sqrt((3.2*areapower)+(0.5*saarpower)+(0.1*farlpower)+(0.2*fpextpower))
    return distance
