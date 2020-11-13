#!/usr/bin/env python3

#import defaults
import o32reader as rdr
import adcarray as adc
import numpy as np
import matplotlib.pyplot as plt
import itertools
import argparse
import os


if __name__ == "__main__":

    # ------------------------------------------------------------------------
    # generate a parser for the command line arguments
    parser = argparse.ArgumentParser(description='Generate a pulse-height plot.')
    parser.add_argument('filename', help='the TRD raw data file to process')
    parser.add_argument('--nevents', '-n' , default=1000, type=int,
                        help='number of events to analyse')
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
    scTimeArr = []

    for scEv in os.listdir("/Users/nathansonnina/ALICE/ALICE2020/Performance/data{0}/Channel1".format(args.filename)):
        if(scEv != ".DS_Store"):
            scHour = (scEv[9:11])
            scMin = (scEv[11:13])
            scSec = (scEv[13:15])
            
            hS = int(scHour)*60*60
            hM = int(scMin)*60

            time = int(scSec)+hS+hM
            strTime = str(scHour)+str(scMin)+str(scSec)
            scTimeArr.append(time)

    print(scTimeArr)

    # ------------------------------------------------------------------------
    # some default settings
    DATA_EXCLUDE_MASK = np.zeros((12, 144, 30), dtype=bool)
    # DATA_EXCLUDE_MASK[4:8,0:72,:] = True
    DATA_EXCLUDE_MASK[8:12,0:72,:] = True

    tbsum_mask = 320
    
    sumtrkl = np.zeros(30)
    ntrkl = 0
    trdTimeArr = []
    trdSizeArr = []
    


    # ------------------------------------------------------------------------
    # event loop
    for evno, raw_data in enumerate(reader):
        # if evno % defaults.PRINT_EVNO_EVERY == 0:
        #     print("Proccessing events %d–%d"
        #             % (evno, evno + defaults.PRINT_EVNO_EVERY))
        
        if evno >= args.nevents: break

        # skip the first event, which is usually a config event
        if evno == 0: continue

        print('EVENT', evno)

        try:
            analyser.analyse_event(raw_data)
        except adc.datafmt_error as e:
            continue


        data = analyser.data[:12]  # The last four rows are zeros.
        data[DATA_EXCLUDE_MASK] = 0
        tbsum = np.sum(data, 2)

        timestamp = (reader.ev_timestamp)
        trdTime = ((timestamp.hour+2)*60*60)+(timestamp.minute*60)+timestamp.second
        sizes = reader.blk_size

        trdTimeArr.append(trdTime)
        trdSizeArr.append(sizes)
        
        if(sizes[0]>500 or sizes[1]>500):
            for i in range(len(scTimeArr)):
                #print(trdTime)
                #print(scTimeArr[i])
                if(trdTime < scTimeArr[i]+7 and trdTime > scTimeArr[i]-7):
                    tbsum_zeroes = tbsum < tbsum_mask
                    tbsum[tbsum_zeroes] = 0

                    point_of_interest = np.argwhere(tbsum > 350)
                    if len(point_of_interest) == 0: continue

                    #print(point_of_interest)

                    for r in sorted(set(point_of_interest[:,0])):
                        pads = [x[1] for x in point_of_interest if x[0]==r]

                        print ( "  Row ", r, ": ", pads)

                        start = False
                        current = False
                        for p in pads+[999]:
                            if not start:
                                start=p
                                current=p-1

                            if p==(current+1):
                                current = p
                            else:
                                npad = current-start+1
                                trkl = data[r, start:current+1, :]-9.5

                                print ("    Tracklet: ", start, current, np.sum(trkl))

                                if ( np.sum(trkl[:,0:6]) > 50 ):
                                    continue
                                
                                #print( trkl )

                                #print( "sum: ", np.sum(trkl, 0) )
                                sumtrkl += np.sum(trkl, 0)
                                ntrkl += 1
                                print(ntrkl)
                                plt.plot(np.sum(trkl,0))
                    
                    scTimeArr[i] = -1 
#        for p in point_of_interest:
#            if p[1] == 0:
#                if tbsum[p[0],p[1]-1] > tbsum[p[0],p[1]]: continue
#                # if tbsum[p[0],p[1] + 1] > tbsum[p[0],p[1]]:
#            if p[1] == 144:
#                # for i in range(4):
#                if tbsum[p[0], p[1] - 1] > tbsum[p[0], p[1]]: continue
#                # if tbsum[p[0], p[1] + 1] > tbsum[p[0], p[1]]: continue
#            else:
#                # for i in range(4):
#                if tbsum[p[0], p[1] - 1] > tbsum[p[0],p[1]]: continue
#                if tbsum[p[0], p[1] + 1] > tbsum[p[0], p[1]]: continue
#
                # else: continue

            #print(p)
            #plt.imshow(data[p[0], :, :].T)
            #plt.plot( [p[1]], [31], "ro")
            #plt.show()
            

        #plt.imshow(tbsum, cmap='hot', vmin=tbsum_mask - 1, norm=None, extent=None, aspect=None,
        #           interpolation=None)
        #plt.colorbar(orientation='horizontal')
        # plt.show()


        # print(point_of_interest)
        # for tbsum_coordinates, info in enumerate(point_of_interest):
        #     padrow = info[0]
        #     padrowlist.append(padrow)
        #     pad = info[1]
        #     padlist.append(pad)
        # print('pad row ', padrow, 'pad ', pad, 'reading ', tbsum_value)
        # plt.imshow(tbsum)
        #plt.plot(point_of_interest[:, 1], point_of_interest[:, 0], 'go')
        #plt.show()



    
        # intensity_sum = sum(intensity)
        # plt.imshow(intensity_sum)
        # plt.imshow(intensity_sum, cmap='hot', vmin=tbsum_mask - 1, norm=None, extent=None, aspect=None, interpolation=None)
        # plt.colorbar(orientation='horizontal')

    plt.figure()
    plt.plot(sumtrkl/ntrkl)
    plt.show()
