psuwxdata-populator
===================

This repo contains the programs I created for the final project in METEO 498 
at Penn State University (Spring 2014).

In it's current form, the only file in the project simply populates a MySQL 
database with all the key weather statistics from the PSU Co-op station 
(1896 to present). *At the current time, this only goes from 1-1-1896 to 
3-31-2014, though it could easily be modified to go process any number of 
dates.*

Currently, the following 5 entries are added, if available, for each day:
* High Temperature
* Low Temperature
* Amount of Liquid Precipitation
* Amount of Solid Precipitation (i.e. Snow/Sleet/Hail)
* Snow Depth
