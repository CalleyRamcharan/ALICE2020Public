import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import argparse 
'''
# ------------------------------------------------------------------------
# generate a parser for the command line arguments
parser = argparse.ArgumentParser(description='specify the run you are processing')
parser.add_argument('run', help='the run of data to be processed')
parser.add_argument('--printargs', action='store_true',
                    help='print arguments and exit')

args = parser.parse_args()

if args.printargs:
    print (args)
    exit(0)

# ------------------------------------------------------------------------
'''

#Function definition to read in scintillator files into a numpy array
def readFile(fD):
    f = open(fD,'r')
    data = f.read()
    data = data[1:len(data)-1]
    data = data.split(',')

    for i in range(0,len(data)):
        data[i] = float(data[i])

    data = np.array(data)

    return data

  
#Change run number to the run corresponding to the scintillator data you want to analyse
run = "0783"

start = 0
end = 0

######## Calculating the integral over each event pulse

sum1Arr = []
sum2Arr = []

peakPosA1 = []
peakPosA2 = []

peakPosB1 = []
peakPosB2 = []

timestampArr = []


#Absolute paths used for input files - change it to your absolute path when running on your computer
for filename in os.listdir("/Users/nathansonnina/ALICE/ALICE2020/Performance/data{0}/Channel1".format(run)):
    if(filename != ".DS_Store"):
        print(filename)
        pulse = readFile("/Users/nathansonnina/ALICE/ALICE2020/Performance/data{0}/Channel1/{1}".format(run, filename))
        x = np.linspace(0,200,200)
        pulse = pulse[4900:5100]
        timestamp = filename[:15]
        timestampArr.append(timestamp)

        pulse = np.array(pulse)
        peak = min(pulse)
        index = 0

        for i in range(0,4000):
            if pulse[i] == peak:
                index = i
                break

        cent = int(x[index])
        start = cent-10
        end = cent+10
        x =  np.linspace(start,end,end-start)

        ######## Calculating the integral over each event pulse

        pulse = pulse[start:end]
        print(pulse)
        integral = sum(pulse)
        
        sum1Arr.append(integral)

        ######## Time Difference 1: Max of Data

        peakPosA1.append(cent) 

        ######## Time Difference 3: Biggest jump 2: with threshold value this time: Electric Boogaloo

        diff = peak/2
        count = 0

        for i in range(2,end-start):
            if np.abs(pulse[i-2] - pulse [i]) > diff:
                count = i-2
                pos = x[count]
                peakPosB1.append(pos)  
                break


#Absolute paths used for input files - change it to your absolute path when running on your computer
for filename in os.listdir("/Users/nathansonnina/ALICE/ALICE2020/Performance/data{0}/Channel2".format(run)):
    if(filename != ".DS_Store"):
        pulse = readFile("/Users/nathansonnina/ALICE/ALICE2020/Performance/data{0}/Channel2/{1}".format(run, filename))
        x = np.linspace(0,200,200)
        pulse = pulse[4900:5100]

        pulse = np.array(pulse)
        peak = min(pulse)
        index = 0

        for i in range(0,4000):
            if pulse[i] == peak:
                index = i
                break

        cent = int(x[index])

        start = cent-10
        end = cent+10
        x =  np.linspace(start,end,end-start)

        ######## Calculating the integral over each event pulse

        pulse = pulse[start:end]
        integral = sum(pulse)
        
        sum2Arr.append(integral)

        ######## Time Difference 1: Max of Data

        peakPosA2.append(cent) 

        ######## Time Difference 3: Biggest jump 2: with threshold value this time: Electric Boogaloo

        diff = peak/2
        count = 0

        for i in range(2,end-start):
            if np.abs(pulse[i-2] - pulse [i]) > diff:
                count = i
                pos = x[count]
                peakPosB2.append(pos)  
                break

######## Time Difference Part 1: Max of Data   

peakPosA1 = np.array(peakPosA1)
peakPosA2 = np.array(peakPosA2)
tdArr1 = np.abs(peakPosA1 - peakPosA2)

######## Time Difference Part 3: Biggest jump 2: with threshold value this time: Electric Boogaloo (NB: this method did not work well because I got it up and running the day things were due so it's not reflected in the event log BUT I think if done well, its the best way forward)

peakPosB1 = np.array(peakPosB1)
peakPosB2 = np.array(peakPosB2)
tdArr2 = np.abs(peakPosB1 - peakPosB2)

######## Saving to csv file format with channel 1 and 2 integrals as well as the two methods of calculating time difference

header = ['EventID', 'Timestamp', 'Sc1 Integral', 'Sc2 Integral', 'TD (Method 1)', 'TD (Method 2)']
rows = []

for i in range(len(sum1Arr)):
    rows.append([i,timestampArr[i],sum1Arr[i],sum2Arr[i],tdArr1[i],tdArr2[i]])

with open('EventLog{0}.csv'.format(run), 'wt') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header) 
    csv_writer.writerows(rows)
