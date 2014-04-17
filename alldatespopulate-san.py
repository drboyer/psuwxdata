#!/usr/bin/python

# This script is modified from the PSU Snow Depth site project (see 
#    https://github.com/drboyer/psusnowdepth/blob/master/populatedb.py
#    for original source) to fit the requirements of the METEO 498 class.
#
# Grabs the Walker Building observations from 1/1/1896 to 3/31/2014 and adds
#    them all to the database.

import urllib2
import re
from datetime import date, timedelta
import MySQLdb
from prepareVal import *

# Set up db connection
db = MySQLdb.connect(host="localhost",
                     user="USERNAME",
                     passwd="PASSWORD",
                     db="DBNAME")

cur = db.cursor()                             # Cursor object used to access db

processDay = True             # Flag to indicate when processing of days should stop

procDate = date(1896, 01, 01)      # Start on Jan. 1, 1896
ENDDATE = date(2014, 03, 31)       # The end date for the scope of this project - 3/31/2014

daysSkipped = 0               # The number of days skipped due to data page or database errors

while processDay:
	# Set up the dates
	# NOTE: strftime DOES NOT WORK BEFORE THE YEAR 1900, therefore it cannot be used here
	dateISOStr = procDate.isoformat()   	# This is used to create the POST date string, for
											#    insertion into the database, and for messages
											#    printed to the screen
	dateURLStr = ''                         # This has to be an empty string before we can join 
											#    on it
	dateURLStr = dateURLStr.join(dateISOStr.split('-'))
	
	# Grab the page
	print "Now processing entry for " + dateURLStr
	page = urllib2.urlopen("http://www.meteo.psu.edu/~wjs1/wxstn/getsummary.php", "dtg="+dateURLStr)
	pagestr = page.read()

	# Extract all the necessary information from the page. Days are skipped if the page is not
	#    formatted correctly (i.e. any regular expression of the 5 below are not found)
	try:
		highRes = re.search('High Temperature\s*:\s*(-?\d{1,3}|\(N\/A\))', pagestr).group(1)
		lowRes = re.search('Low Temperature\s*:\s*(-?\d{1,3}|\(N\/A\))', pagestr).group(1)
		liquidRes = re.search('Rain or Liquid Equivalent\s*:\s*(\d{1,2}.\d{2}|TRACE|\(N\/A\))', pagestr).group(1)
		solidRes = re.search('Snow and/or Ice Pellets\s*:\s*(\d{1,2}.\d{1}|TRACE|\(N\/A\))', pagestr).group(1)
		depthRes = re.search('Snow Depth\s*:\s*([0-9]{1,2}|TRACE|\(N\/A\))', pagestr).group(1)

		entries = (dateISOStr, prepareVal(highRes), prepareVal(lowRes), prepareVal(liquidRes), prepareVal(solidRes), prepareVal(depthRes))

		# Insert into DB
		try:
			cur.execute("INSERT INTO psuWxStn (entry_date, temp_high, temp_low, precip_liquid, precip_solid, snow_depth) VALUES (%s, %s, %s, %s, %s, %s)", entries)
			print "Added Entry: " + dateISOStr
		except MySQLdb.Error, e:
	        	print "ENTRY SKIPPED for " + dateISOStr + ". Could not add entry to database!"
	        	daysSkipped = daysSkipped + 1
	except AttributeError:
		print "ENTRY SKIPPED for " + dateISOStr + ". Data page did not contain the necessary information."
		daysSkipped = daysSkipped + 1

	# Increment date before looping around again
	procDate = procDate + timedelta(days=1)

	if (procDate > ENDDATE):    # Don't loop anymore if we get past the cutoff date
		processDay = False

print "Processing complete.\nNumber of days skipped: " + str(daysSkipped)
