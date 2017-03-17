def main():
    pass

    # open existing project
    # get project details from database for user

    # new project
    # two tabs - Sites and Pooling group

    # add a site to the sites tab and view the station data
    # flask procedures for lists and file opening - SelectField, wtforms, request.form.getlist

    # create a new station (ungauged site) from FEH CD-ROM data (.CD3 format)

    # begin estimation procedures
    # single site analysis or pooled analysis?

    # create pooling group
    # import ungauged catchment
    # select all suitable for pooling stations from database and put into dictionary
    # iterate over dictionary and calculate SDM for each station vs ungauged catchment
    # sort stations by SDM
    # move stations into new list (poolin_group) based on lowest SDM first until
    # number of years data is at least 500

    # calculate growth curve
    # use LMOM and enhanced procedure to do this
