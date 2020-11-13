
import numpy as np
import matplotlib.pyplot as plt

radec = open("coordinates.txt", "r")

file = radec.read(-1)
file = file.split(" ")

RA = np.zeros(len(file))
dec = np.zeros(len(file))

for i in range(0,len(file)):
    arr = file[i].split(",")
    RA[i] = float(arr[0][1:])/15
    print(RA[i])
    dec[i] = float(arr[1][:arr[1].index("]")])

plt.polar(RA,dec,'ro',ms=2)
plt.show()

#plt.hist(RA,bins=50)
#plt.show()
#plt.hist(dec,bins=50)
#plt.show()

radec.close()
