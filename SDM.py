import math
import numpy as np


# calculates the distance measure based on catchment descriptors.  i is imported ungauged catchment of interest,
# j is gauged catchment from suitable for pooling file
# todo: check that input to pooling group have 'suitable for pooling = true'

def SDM(areai, areaj, saari, saarj, farli, farlj, fpexti, fpextj):
    areadiff = math.pow(((np.log(areai) - np.log(areaj)) / 1.28), 2)

    saardiff = math.pow(((np.log(saari) - np.log(saarj)) / 0.37), 2)

    farldiff = math.pow((farli - farlj) / 0.05, 2)

    fpextdiff = math.pow((fpexti - fpextj) / 0.04, 2)

    distance = math.sqrt((3.2 * areadiff) + (0.5 * saardiff) + (0.1 * farldiff) + (0.2 * fpextdiff))
    return distance
