
#import defaults
import o32reader as rdr
import adcarray as adc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import itertools
import argparse
from roi import regions_of_interest
import os


if __name__ == "__main__":

    # ------------------------------------------------------------------------
    # generate a parser for the command line arguments
    parser = argparse.ArgumentParser(description='Generate a pulse-height plot.')
    parser.add_argument('filename', help='the TRD raw data file to process')
    parser.add_argument('--nevents', '-n' , default=1000, type=int,
                        help='number of events to analyse')
    parser.add_argument('date',help='date on which the run was taken')
    parser.add_argument('--progress', '-p' , default=-1, type=int,
                        help='print event number every N events')
    parser.add_argument('--allplots', action='store_true',
                        help='draw a crowded plot with all tracklets')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')

    args = parser.parse_args()

    if args.printargs:
        print (args)
        exit(0)

    # ------------------------------------------------------------------------
    # setup the reader
    reader = rdr.o32reader(args.filename)
    analyser = adc.adcarray()

    # ------------------------------------------------------------------------
    # some default settings
    DATA_EXCLUDE_MASK = np.zeros((12, 144, 30), dtype=bool)
    DATA_EXCLUDE_MASK[4:8,0:72,:] = True

    sumtrkl = np.zeros(30)
    ntrkl = 0

    # ------------------------------------------------------------------------
    # create 2D array of scintillator time stamps for comparison
    
    scTimeArr = []
    scStrTimeArr = []

    for scEv in os.listdir("/Users/nathansonnina/ALICE/ALICE2020/Performance/data{0}/Channel1".format(args.filename)):
        if(scEv != ".DS_Store"):
            scHour = (scEv[9:11])
            scMin = (scEv[11:13])
            scSec = (scEv[13:15])
            
            hS = int(scHour)*60*60
            hM = int(scMin)*60

            time = int(scSec)+hS+hM
            strTime = str(scHour)+str(scMin)+str(scSec)

            scStrTimeArr.append(strTime)
            scTimeArr.append(time)

    #print(scStrTimeArr)
    print(len(scTimeArr))
    # ------------------------------------------------------------------------
    # create the histogram

    #hist, bins = np.histogram((), np.linspace(0, 20, 2000))

    alldata = None
    count = 0
    validScFiles = []
    trdTimeArr = []
    trdSizeArr = []

    # ------------------------------------------------------------------------
    # event loop
    for evno, raw_data in enumerate(reader):

        # limit number of events to be processed
        if evno >= args.nevents: break

        # skip the first event, which is usually a config event
        if evno == 0: continue

        if args.progress > 0 and evno%args.progress==0:
            print ("###  EVENT %d" % evno )

        # read the data
        try:
            analyser.analyse_event(raw_data)
            #print(reader.peekNextLine())

        except adc.datafmt_error as e:
            print ("data format error in event %d" % evno)
            continue

        timestamp = (reader.ev_timestamp)
        trdTime = ((timestamp.hour+2)*60*60)+(timestamp.minute*60)+timestamp.second
        sizes = reader.blk_size

        trdTimeArr.append(trdTime)
        trdSizeArr.append(sizes)

        data = analyser.data[:12]  # The last four rows are zeros.
        data[DATA_EXCLUDE_MASK] = 0

        if(sizes[0]>500 or sizes[1]>500):
            for i in range(len(scTimeArr)):
                if(trdTime < scTimeArr[i]+7 and trdTime > scTimeArr[i]-7):

                    if alldata is None:
                        alldata = np.expand_dims(data, axis=0)
                    else:
                        alldata = np.concatenate( (alldata,np.expand_dims(data, axis=0)), axis=0 )

                    #print(scStrTimeArr[i],timestamp)
                    scTimeArr[i] = -1 
                    validScFiles.append(scStrTimeArr[i])

    os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/SYNCdata{0}".format(args.filename))
    os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/SYNCdata{0}/Channel1".format(args.filename))
    os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/SYNCdata{0}/Channel2".format(args.filename))
    #os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/SYNCdata{0}/SYNCChannel3".format(args.filename))
    #os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/SYNCdata{0}/SYNCChannel4".format(args.filename))

    for j in range(len(validScFiles)):
        fileDate = "{0}_{1}".format(args.date,validScFiles[j])
        for k in range(1,3):
            os.system("cp /Users/nathansonnina/ALICE/ALICE2020/Performance/data{1}/Channel{0}/{2}_ch{0}.out /Users/nathansonnina/ALICE/ALICE2020/Performance/SYNCdata{1}/Channel{0}/".format(k,args.filename,fileDate))
            

    print("Number of Events Recorded",i)
    np.save(args.filename+'SYNC.npy', alldata)
