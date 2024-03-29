#!/usr/bin/env python3

from gw_lan import lan
import dso1kb
import datetime
import os
import argparse

#Connecting to a DSO.
#dso=dso1kb.Dso("10.10.0.20:3001") 
#dso=dso1kb.Dso("127.0.0.1:3129")


# ------------------------------------------------------------------------
# generate a parser for the command line arguments
parser = argparse.ArgumentParser(description='Send triggers for a synchronized data run.')
parser.add_argument('run', help='the current TRD run')
parser.add_argument('--printargs', action='store_true',
                    help='print arguments and exit')

args = parser.parse_args()

# ------------------------------------------------------------------------

if args.printargs:
    print (args)
    exit(0)

#os.system("mkdir {0}".format(args.run))

def take_event():

    dso=dso1kb.Dso("10.10.0.20:3001")
    now = datetime.datetime.now()

    os.system('dim_send_command trdbox/command "trg single"')
    

    dso.getRawData(True, 1)
    dso.getRawData(True, 2)
    dso.getRawData(True, 3)
    dso.getRawData(True, 4)
    
    fwave = []
    
    for ch in range(1,5):
        
        fwave = dso.convertWaveform(ch,1)
        
        #fname = f"data/{now.isoformat()}_ch{ch}.out"
        fname = f"data{args.run}/{now.strftime('%Y%m%d_%H%M%S')}_ch{ch}.out"

        print(fname)
        with open (fname,"w") as f:
            f.write(str(fwave))
    

#for i in range(10):
take_event()
