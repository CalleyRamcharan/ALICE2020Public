
import numpy as np
import matplotlib.pyplot as plt


#Output file of coordinates.py had to have minor manual changes made to allow it to be read into this code as an input file
# Input file format should be of the form:
# [ , ] [ , ] [ , ] - with entries of each array being floats
# ^^ This is different to the output file from coordinates.py - so sorry :( we didn't have time to write to the file in a nice colummated format :(
# find and replace should do the trick to help you out with reformatting the output file from coordinates.py, unless if you want to go edit
# coordinates.py to let it write in a nice format, then by all means be my guest


#read in input file
radec = open("coordinates.txt", "r")

#read entire file as one large string
file = radec.read(-1)
file = file.split(" ")

RA = np.zeros(len(file))
dec = np.zeros(len(file))

for i in range(0,len(file)):
    arr = file[i].split(",")
    RA[i] = float(arr[0][1:])/15
    print(RA[i])
    dec[i] = float(arr[1][:arr[1].index("]")])

#create polar plot of RA and dec values to see dispersion of cosmic rays    
plt.polar(RA,dec,'ro',ms=2)
plt.show()

#plt.hist(RA,bins=50)
#plt.show()
#plt.hist(dec,bins=50)
#plt.show()

radec.close()
