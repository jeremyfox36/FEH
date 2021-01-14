# Background
This is a Python3/postgresql/Flask application.
The goal is to translate the Flood Estimation Handbook (http://www.ceh.ac.uk/services/flood-estimation-handbook) methods into a web application.

# Specification
Should be be able to upload a new ungauged catchment and calculate the growth curve and QMED for different return periods. The package should also allow me to add climate change corrections.
I can do calcs for a guaged catchment and add a donor.

# Essential	
Unzip and parse NRFA Hiflows data into postgresql db

Allow upload of selected catchment data as a text file

perform FEH procedures
        Calculate distance measure
	Find pooling group
	calculate heterogeneity measure (import or convert R library LMOMRFA)
	display pooling group with the option to remove or add catchments
	display individual AMAX data
	calculate growth curv
	
# Nice to have
Download flow data directly from NRFA website at http://nrfa.ceh.ac.uk/winfap-feh-files (backend infrequent updates)
	- automate checking of hiflows website for updated zip
