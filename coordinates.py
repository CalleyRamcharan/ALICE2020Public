import numpy as np
import matplotlib.pyplot as pl
import scipy.optimize as optimize
import math
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, ICRS
from astropy.time import Time

#LOAD EVENT DATA 
data1=np.load('0783SYNC.npy')
observtime = np.genfromtxt("EventLogSYNCdata0783.csv", delimiter=',',skip_header=1, usecols=1)
timeArr = []
timeUseful = []
radecArr = []
raArr = []
decArr = []
incArr = []

for time in observtime: #to make an array of the timestamps
    time = str(time)
    year = time[0:4]
    month = time[4:6]
    day = time[6:8]
    hour = time[8:10]
    mins = time[10:12]
    sec = time[12:14]

    time = "{0}-{1}-{2} {3}:{4}:{5}".format(year,month,day,hour,mins,sec)
    timeArr.append(time)

adc = 9.62 #this comes from performance

for i in range(len(data1)):
    for x in range(144):
        for y in range(12):
            for tb in range(30):
                if data1[i,y,x,tb] != 0:
                    data1[i,y,x,tb]=data1[i,y,x,tb]-adc
#Subtract average ADC value from non-zero counts
#print len(data1[1])
relevant = []
for i in range(len(data1)):
    for x in range(144):
        for y in range(12):
            tbsum = np.sum(data1[i,y,x])
            if tbsum > 300:
                #print("!!!",tbsum)
                relevant.append([i,y,x])
                timeUseful.append(timeArr[i])

lenRel = int(len(relevant))
print(lenRel)

anglenorm = []
anglexy = []
counts = []
count = 0

#CALCULATE PAD NRS FOR EVERY EVENT
for m in range(lenRel):
    print(m)
   # data = data1[k] changing it so it reads the right one
    k = relevant[m][0]

    data = data1[k]

    xmin= relevant[k][2] -5 
    xmax= relevant[k][2] + 5  
    ymin= relevant[k][1] -2 
    ymax= relevant[k][1] + 1 
                  
    #EXTRACT COSMIC RAYS IN FLATTENED ARRAY
    cosmic=[]
    for i in range(ymin,ymax):
        for j in range(xmin,xmax):
            cosmic.append(data[i,j,:])
            
    #CALCULATE THE CENTRE OF MASS FOR EACH EVENT
    comx=[]
    comy=[]
    com=np.array([])
    
    #Looping through time bins
    for tb in range(30):
        moment=0
        mass=0

    #For the x-component, we average over y.
        for i in range(ymin,ymax):
            for j in range(xmin,xmax):
                r=np.array([j,i])
                moment+=r*data[i,j,tb]
                mass+=data[i,j,tb]
        X,Y=moment/mass

        comx.append(X)
        comy.append(Y)

    #com=np.append(com,[X,Y])

    #STRAIGHT LINE FIT THROUGH CENTRE OF MASS FUNCTIONS
    tb=np.arange(0,30.0)
    
    #Residuals funtion determines the slope and constant of the line
    def residuals(p,yy,xx):
        m,c=p
        err=abs(yy-(m*xx+c))
        return err
    
    #Initial guess
    p0=np.array([4,0])

    #Perform calculation
    leastfit=optimize.leastsq(residuals,p0,(comx,tb))
    leastfit2=optimize.leastsq(residuals,p0,(comy,tb))

    #Extract coefficients
    coeffs=leastfit[0]
    coeffs2=leastfit2[0]

    #Draw lines
    fit=coeffs[0]*tb+coeffs[1]
    fit2=coeffs2[0]*tb+coeffs2[1]

    #Calculate inclination in degrees from slope
    angle=math.atan(coeffs[0])
    angle=angle*(180.0/np.pi)
    angle2=math.atan(coeffs2[0])
    angle2=angle2*(180.0/np.pi)

    if (count==0):
        incArr.append([angle,angle2])
        count+=1

    elif ([angle,angle2] != incArr[count-1]):
            incArr.append([angle,angle2])
            count+=1
    else:
        continue

    #print(incArr[count-1])
    #print (angle,angle2)


    #3D ANALYSIS
    #The data above is used to derive a 3D vetor of the trajectory of the cosmic ray 
    
    #Defining the ave vector 
    tb = np.linspace(0,29, 30) 
    x = coeffs[0]*tb+coeffs[1] 
    y = coeffs2[0]*tb+coeffs2[1]
    
    #Converting to spherical coorinates 
    #Assume the unit vector is in cm. 
    dz=30*(3/20) #Assume 20 time bins = 3 cm
    dx=coeffs[0]*dz*0.77 #The column resolution is 0.77 cm
    dy=coeffs2[0]*dz*8.91 #The row resolution is 8.91cm
    dr=np.sqrt(dx**2 + dy**2 + dz**2)
    
    #Keep angles poitive 
    dtheta=math.acos(dz/dr) 
    if dtheta < 0:
    	dtheta=2*np.pi + dtheta
    
    dphi=math.atan(dy/dx)#+np.pi/2 #Adding 2pi is to make 0deg in y direction 
    
    if dphi < 0:
    	dphi=2*np.pi + dphi
    
    #Convert to degrees 
    dtheta=dtheta*180/np.pi 
    dphi=dphi*180/np.pi
    
    #Print spherical angles: 
    print('Cosmic direction') 
    print('Angle to normal: ',round(dtheta,2)) 
    print('XY plane angle: ',round(dphi,2))
    
    #COORDINATE CONVERSION:
        
    #Position of the TRD: used as position of observation
    trd = EarthLocation(lat=-33.9553325*u.degree,lon=18.4616939*u.degree,height=100*u.m)
    
    #Local Sidereal Time
    utcoffset = 2*u.hour #South African Standard Time
    time = Time(timeUseful[m]) - utcoffset
               
    #AltAz coordinates of the cosmic ray
    c_altaz = SkyCoord(az=dphi*u.degree,alt=dtheta*u.degree,frame='altaz',obstime=time,location=trd)
    
    #Transformation from AltAz to ICRS
    c_icrs=c_altaz.transform_to('icrs')
    print([c_altaz.icrs.ra.hour,c_altaz.icrs.dec.degree])
    
    #Append RA DEC values to an array:
    radecArr.append([c_altaz.icrs.ra,c_altaz.icrs.dec]) 

    #%%
#Write RA DEC values to a txt file for further analysis
 
f = open("coordinates.txt", 'w')
f.write(str(radecArr))
f.close() 

### CODE FOR PLOTTING THE 2D MAP OF THE TRIGGERED PAD WITH, AS WELL AS THE CENTRE OF MASS PLOTS OF EACH EVENT IS NOT INCLUDED IN THIS CODE.
### PLEASE CONSULT ORGINAL SOURCE CODE analysis.py WRITTEN BY JAN-ALBERT VILJOEN, NASSP HONOURS (2016) 


#################################################################################3