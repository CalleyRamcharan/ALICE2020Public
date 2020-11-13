import numpy as np
import matplotlib.pyplot as pl
import scipy.optimize as optimize
import math
#import adcarray as adc
import numpy as np
#import o32reader as rdr
#Load specific synchronised event npy file
data1=np.load('0783SYNC.npy')
#data = data1[100] #changed this to take the first event

for i in range(len(data1)):
    for x in range(144):
        for y in range(12):
            for tb in range(30):
                if data1[i,y,x,tb] != 0:
                    data1[i,y,x,tb]=data1[i,y,x,tb]-9.62
#Subtract average ADC value from non-zero counts
#print len(data1[1])
relevant = []
for i in range(len(data1)):
    for x in range(144):
        for y in range(12):
            
            tbsum = np.sum(data1[i,y,x])
            if tbsum > 10000: #was 300
                relevant.append([i,y,x])

print len(relevant)/3

#for x in range(144):
#    for y in range(12):
#        for tb in range(30):
#            if data[y,x,tb] != 0:
#                data[y,x,tb]=data[y,x,tb]-9.62
#Zoom image to pads that are triggered by cosmic

anglenorm = []
anglexy = []
counts = []

for m in range(len(relevant)/3):
   # data = data1[k] changing it so it reads the right one
    k = relevant[m][0]

    data = data1[k]

    xmin= relevant[k][2] -5 #was 60
    xmax= relevant[k][2] + 5  #was 70
    ymin= relevant[k][1] -2 #was 8
    ymax= relevant[k][1] + 1 #was 11
    #Extract cosmic ray in flattened array:
    cosmic=[]
    for i in range(ymin,ymax):
        for j in range(xmin,xmax):
            cosmic.append(data[i,j,:])
    #Calculating the centre of mass in x/y components
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

    #Fit straight lines through the centre of mass functions
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

    #Plot the results
    #First plot the average over time bin, for each triggered pad
   
    tbsum=np.sum(data[ymin:ymax,xmin:xmax],axis=2)
    
    #Plot flattened array of cosmic, over time bin

    #The pad count in y-axis, are numbered left to right, top to bottom, form the 2D plane
 
    #pl.show()

    #Plot the centre of mass over time bin, with straight line fit

    #pl.show()
    ################################################################################
    ##########3
    #3D Analysis
    #The data above is used to derive a 3D vetor of the trajectory of the cosmic ray
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import rcParams
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import FancyArrowPatch
    from mpl_toolkits.mplot3d import proj3d


    #Defining the ave vector
    tb = np.linspace(0.0,29.0, 30.0)
    x = coeffs[0]*tb+coeffs[1]
    y = coeffs2[0]*tb+coeffs2[1]

    #Converting to spherical coorinates
    #Assume the unit vector is in cm.
    dz=30.0*(3.0/20.0) #Assume 20 time bins = 3 cm
    dx=coeffs[0]*dz*0.77#The column resolution is 0.77 cm
    dy=coeffs2[0]*dz*8.91 #The row resolution is 8.91cm
    dr=np.sqrt(dx**2.0 + dy**2.0 + dz**2.0)

    #Keep angles poitive
    dtheta=math.acos(dz/dr)
    if dtheta < 0:
        dtheta=2.0*np.pi + dtheta

    dphi=math.atan(dy/dx)#+np.pi/2 #Adding 2pi is to mak 0deg in y direction
    if dphi < 0:
        dphi=2.0*np.pi + dphi

    #Convert to degrees
    dtheta=dtheta*180.0/np.pi
    dphi=dphi*180.0/np.pi

    tbsum2 = np.sum(data1[k,relevant[k][1],relevant[k][2] ])
    counts.append(tbsum2)


    anglenorm.append(round(dtheta,2))
    anglexy.append(round(dphi,2))



    #Print spherical angles:
   # print('Cosmic direction')
   # print('Angle to normal: ',round(dtheta,2))
   # print('XY plane angle: ',round(dphi,2))
    #Choosing plot properties:

    #Actual trajectory

    #Average trajectory
print len(counts)
print len(anglexy)
print len(anglenorm)

#file =open('angle_norm3.txt' , 'w+')
#file.write(str(anglenorm))
#file.close()

#file =open('angle_xy3.txt' , 'w+')
#file.write(str(anglexy))
#file.close()

#file = open('counts3.txt' , 'w+')
#file.write(str(counts))
#file.close()
