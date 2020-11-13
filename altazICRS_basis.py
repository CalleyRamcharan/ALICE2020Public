# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 02:49:31 2020

@author: sumari
"""
### astropy COORDINATE CONVERSION CODE: HORIZONTAL (ALT-AZ) TO ICRS (RA DEC) ###
### WRITTEN BY SUMARI FAUL (ALICE 2020) ###

# IMPORT PACKAGES #
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.time import Time

# LOCATION OF OBSERVATION: TRD #
trd = EarthLocation(lat=-33.9553325*u.degree,lon=18.4616939*u.degree,height=100*u.m) #Latitude, longitude, height above sea level 
    
# LOCAL SIDEREAL TIME #
utcoffset = 2*u.hour #South African Standard Time (SAST)
time = Time('2020-11-11 01:11:11') - utcoffset #Date and time of observation. NOTE FORMAT.
               
# ALT-AZ COORDS OF COSMIC RAY #
c_altaz = SkyCoord(az=70.563*u.degree,alt=35.507*u.degree,frame='altaz',obstime=time,location=trd) #Using arbitrary alt-az values here 
    
# TRANSFORMATION FROM ALT-AZ TO ICRS # 
c_icrs=c_altaz.transform_to('icrs')

print([c_altaz.icrs.ra, c_altaz.icrs.dec]) #for RA and DEC in degrees
print([c_altaz.icrs.ra.hour, c_altaz.icrs.dec.degree]) #for RA in hours and DEC in degrees

### ### ### ### 