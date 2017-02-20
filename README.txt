Specification

Download flow data directly from NRFA website at http://nrfa.ceh.ac.uk/winfap-feh-files (backend infrequent updates)
	- automate checking of hiflows website for updated zip
	
Unzip and parse into postgresql db
migrate to Django framework

Allow upload of selected catchment data from FEH web service as a text file

perform FEH procedures
	import or convert R library LMOMRFA for heterogeneity calcs
	Calculate distance measure
	Find optimal pool from NRFA data
	calculate L-moments using LMOM library
	calculate growth curve
	provide pooling group stats for assessment
