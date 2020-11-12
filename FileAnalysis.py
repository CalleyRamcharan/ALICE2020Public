import matplotlib.pyplot as plt
import numpy as np
import os
#import pylandau
#from scipy.stats import moyal
import scipy
from scipy.optimize import curve_fit,minimize_scalar 
from scipy import asarray as ar,exp
from scipy.stats import norm

def readFile(fD):
    f = open(fD,'r')
    data = f.read()
    data = data[1:len(data)-1]
    data = data.split(',')

    for i in range(0,len(data)):
        data[i] = float(data[i])

    data = np.array(data)

    return data

def landauApprox(x,loc,scale,A): #A - height, loc - x shift, scale - spread
    x = (x-loc)/scale
    return A*(((1/np.sqrt(2*np.pi))*(np.e**(-1*((x+(np.e**(-1*x)))/2))))/scale)

def uX(fwhm, counts):
    return(fwhm/(2.35*np.sqrt(sum(counts))))

def gaus(x,a,x0,sigma):
    return (a/(sigma*np.sqrt(2*np.pi))*exp(-((x-x0)**2)/(2*sigma**2)))

################### Defining Variables

fileChoice = "EventLogSYNCdata0783.csv"

eventID = np.genfromtxt(fileChoice,delimiter=',',skip_header=1,usecols=0)
integral1 = np.genfromtxt(fileChoice,delimiter=',',skip_header=1,usecols=2)
integral2 = np.genfromtxt(fileChoice,delimiter=',',skip_header=1,usecols=3)
timeD1 = np.genfromtxt(fileChoice,delimiter=',',skip_header=1,usecols=4)
timeD2 = np.genfromtxt(fileChoice,delimiter=',',skip_header=1,usecols=5)

timeD1 = timeD1*(4)
timeD2 = timeD2*(4)

integral1 = np.abs(integral1)
integral2 = np.abs(integral2)

dataNo = len(integral1)
n = 902

################# Event counter/Comparing time methods
binNo = 80

counts, edges = np.histogram(timeD1,bins = binNo)
centres = (edges[1:] + edges[:-1]) / 2
x = np.linspace(0,60,1000)
u = centres**0.5
mu, sigma = scipy.stats.norm.fit(timeD1)

popt,pcov = curve_fit(gaus,centres,counts,p0=[200,mu,sigma])
print("mean 1 =", popt[1], "+/-", pcov[1,1]**0.5)
print("sigma 1 =", popt[2], "+/-", pcov[2,2]**0.5)
print("um 1 =", popt[2]/(902)**0.5)

dymin = (counts-gaus(centres,*popt))/u
min_chisq = sum(dymin*dymin)
dof =len(centres)-len(popt)

print("Chi square:", min_chisq )
print("Number of degrees of freedom:",dof)
print("Chi square per degree of freedom:" , min_chisq/dof )
print()

plt.plot(x,gaus(x,*popt),'r--',label='Gaussian fit',markersize=1)
plt.hist(timeD1,bins = binNo,color="deepskyblue")
plt.title("Method 1: Minimums")
plt.ylabel("Number of counts")
plt.xlabel("Time(ns)")
plt.xlim(0,55)
plt.show()

counts, edges = np.histogram(timeD2,bins = binNo)
centres = (edges[1:] + edges[:-1]) / 2
u = centres**0.5
mu, sigma = scipy.stats.norm.fit(timeD2)

popt,pcov = curve_fit(gaus,centres,counts,p0=[25,mu,sigma])
print("mean 2 =", popt[1], "+/-", pcov[1,1]**0.5)
print("sigma 2 =", popt[2], "+/-", pcov[2,2]**0.5)
print("um 2 =", popt[2]/(902)**0.5)

dymin = (counts-gaus(centres,*popt))/u
min_chisq = sum(dymin*dymin)
dof =len(centres)-len(popt)

print("Chi square:", min_chisq )
print("Number of degrees of freedom:",dof)
print("Chi square per degree of freedom:" , min_chisq/dof )
print()

plt.plot(x,gaus(x,*popt),'r--',label='Gaussian fit',markersize=1)

plt.hist(timeD2,bins = binNo,color = "royalblue")
plt.title("Method 2: Signal Starts")
plt.ylabel("Number of counts")
plt.xlabel("Time(ns)")
plt.xlim(0,60)
plt.show()

plt.hist(timeD1,bins = binNo)
plt.hist(timeD2,bins = binNo)
plt.show()

################# Integral Histograms
# binNo = 50

# plt.hist(integral1,bins = binNo, log=True)
# plt.title("Ch 1")
# plt.ylabel("Counts")
# plt.xlabel("Integral")
# plt.xlim(0,8)
# #plt.ylim(0,200)
# plt.show()

# plt.hist(integral2,bins = binNo,color="orange", log=True)
# plt.title("Ch 2")
# plt.ylabel("Counts")
# plt.xlabel("Integral")
# plt.xlim(0,3)
# #plt.ylim(0,180)
# plt.show()


# plt.hist(integral1,bins = binNo,label="Ch 1")
# plt.hist(integral2,bins = binNo,label="Ch 2")
# plt.ylabel("Number of datasets")
# plt.xlabel("Integral")
# plt.title("Ch 1 and Ch 2")
# plt.legend()
# #plt.xlim(0.5,5)
# #plt.ylim(0,220)
# plt.show()














################# Landau???????
'''
## Channel 1 
x = np.linspace(0,10,10000)

binNo = 200

counts, edges = np.histogram(integral1,bins = binNo)
counts = counts[14:45]
edges = edges[14:46]

centers = (edges[1:] + edges[:-1]) / 2
guess = [3,4,200]
print(counts)

popt,pcov = curve_fit(landauApprox,xdata=centers,ydata=counts,p0 = guess)

sigma = np.sqrt(counts)
dymin = (counts - landauApprox(centers,*popt))/sigma
min_chisq = sum((dymin*dymin))
dof = len(centers) - len(popt)
print("CHISQ/DOF:",min_chisq/dof)

y = landauApprox(x,*popt)
peak = (max(y))
HM = peak/2

index = 0
W1 = 0
W2 = 0

for i in range(0,len(y)):
    if y[i] == peak:
        index = i
        break

for i in range(1,index):
    if y[i-1]<HM and y[i]>HM:
        W1 = i
        break

for i in range(index,len(y)):
    if y[i-1]>HM and y[i]<HM:
        W2 = i
        break


posPeak = x[index]

posW1 = x[W1]
posW2 = x[W2]

width = posW2 - posW1 
FWHM = width*HM
print("FWHM:",FWHM)
print("Width:",width)

dx = uX(width,counts)
print(posPeak, '+/-', dx)


plt.hist(integral1,bins = binNo,color = 'deepskyblue')
plt.title("Channel 1")

plt.xlim(0.5,4)
plt.ylim(0,200)
plt.plot(x,landauApprox(x,*popt),color="midnightblue", linewidth=3)
plt.plot(posPeak,peak,'ok',ms=10,label="Peak of Landau Distribution")
plt.vlines(x=posW1,ymin=0, ymax = HM, color='black', linestyle='dashed',label="Points used to calculate FWHM")
plt.vlines(x=posW2,ymin=0, ymax = HM, color='black', linestyle='dashed')

plt.ylabel("Number of Data Sets")
plt.xlabel("Integrated Signal Value")
plt.legend()
plt.show()
##



##Channel 2
x = np.linspace(-0.5,10,10000)

binNo = 200

counts, edges = np.histogram(integral2,bins = binNo)
counts = counts[35:72]
edges = edges[35:73]
print(counts)
centers = (edges[1:] + edges[:-1]) / 2
guess = [1,1,200]

popt,pcov = curve_fit(landauApprox,xdata=centers,ydata=counts,p0 = guess)

sigma = np.sqrt(counts)
dymin = (counts - landauApprox(centers,*popt))/sigma
min_chisq = sum((dymin*dymin))
dof = len(centers) - len(popt)
print("CHISQ/DOF:",min_chisq/dof)

y = landauApprox(x,*popt)
peak = (max(y))
HM = peak/2

index = 0
W1 = 0
W2 = 0

for i in range(0,len(y)):
    if y[i] == peak:
        index = i
        break

for i in range(1,index):
    if y[i-1]<HM and y[i]>HM:
        W1 = i
        break

for i in range(index,len(y)):
    if y[i-1]>HM and y[i]<HM:
        W2 = i
        break


posPeak = x[index]


posW1 = x[W1]
posW2 = x[W2]

width = posW2 - posW1 
FWHM = width*HM
print("FWHM:",FWHM)
print("Width:",width)

dx = uX(width,counts)
print(posPeak, '+/-', dx)

plt.hist(integral2,bins = binNo,color = 'yellowgreen')
plt.title("Channel 2")

#plt.xlim(-0.5,3)
plt.ylim(0,650)
plt.plot(x,landauApprox(x,*popt),color="darkgreen", linewidth=3)
plt.plot(posPeak,peak,'ok',ms=10,label="Peak of Landau Distribution")
plt.vlines(x=posW1,ymin=0, ymax = HM, color='black', linestyle='dashed',label="Points used to calculate FWHM")
plt.vlines(x=posW2,ymin=0, ymax = HM, color='black', linestyle='dashed')
plt.ylabel("Number of Data Sets")
plt.xlabel("Integrated Signal Value")
plt.legend()
plt.show()
'''