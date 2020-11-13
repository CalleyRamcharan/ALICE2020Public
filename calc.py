from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math


angle_norm  = open('angle_norm.txt' , 'r') ## list angles to the normal from "filteringmuons.py" - contains consecutive duplicates
angle_norm = angle_norm.read().split(",")


counts  = open('counts.txt' , 'r') ## list of counts for corresponding angle - same story with regards to duplicates
# counts = np.array(counts.read().split(",") , dtype=float)
counts = counts.read().split(",")


del angle_norm[12271 :12281 ] ## deleting entries with "nan" value
del counts[12271 : 12281]
angle_norm = np.array(angle_norm , dtype=float )
counts = np.array(counts , dtype=float )

angles = []
counts1 = []
dumb =99
## loop removing duplicates in the data
for i in range (len(counts)):
    if angle_norm[i] != dumb:
        angles.append(angle_norm[i])
        counts1.append(counts[i])
    dumb = angle_norm[i]
print(len(angles))

angles = np.array(angles)
counts1 = np.array(counts1)
print(max(angles))

# plt.plot(angles , counts1 , 'r.')
# plt.show()



total_counts = []
angle_range = np.arange(0,3,0.2)
print(angle_range[-1])
##binning the data
for j in range (len(angle_range)):
    k =0
    l = 0
    for i in range (len(angles)):
        if np.abs(angles[i]- angle_range[j]) < np.abs(angles[i]- angle_range[j] -0.2) and np.abs(angles[i]- angle_range[j]) < np.abs(angles[i]- angle_range[j] +0.2) :
        # if angles[i] in range (angle_range[j] , angle_range[j] + 0.2 , 0.2):
            k+= 1# counts1[i]
        #     l+= 1
        # if k!=0:
        #     k = k/l
    total_counts.append(k)

total_counts[0] = total_counts[0] + total_counts[4]*2


plt.plot(angle_range*15 , total_counts , 'r.')
plt.title('Angular distribution of muons passing through the TRD')
plt.ylabel('Number of muons recoreded')
plt.xlabel('Angle to the normal of muon track, bin size = 3 (degrees)')
plt.show()


# def Bin(data, bin_width):
#     min_v = -90
#     max_v = 90
#     bins = np.arange(min_v  , max_v +bin_width , bin_width)
#     count,bins = np.histogram(a=data , bins= bins)

#     return count , bins[:-1]

# x = Bin(angles , 5)
# plt.plot(x[1] , x[0] , 'k.')
# plt.show()


# plt.plot(angle_range , total_counts , 'r.')
# plt.show()






