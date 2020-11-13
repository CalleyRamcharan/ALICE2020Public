import os
import numpy as np
import argparse 

# ------------------------------------------------------------------------
# generate a parser for the command line arguments
parser = argparse.ArgumentParser(description='Specify the folder you want to organize')
parser.add_argument('folder', help='the folder')
parser.add_argument('--printargs', action='store_true',
                    help='print arguments and exit')

args = parser.parse_args()

if args.printargs:
    print (args)
    exit(0)

# ------------------------------------------------------------------------

os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/Channel1".format(args.folder))
os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/Channel2".format(args.folder))
os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/Channel3".format(args.folder))
os.system("mkdir /Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/Channel4".format(args.folder))

for filename in os.listdir("/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}".format(args.folder)): 
    if filename.endswith("ch1.out"): 
        os.rename("/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/{1}".format(args.folder,filename), "/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/Channel1/{1}".format(args.folder,filename))

    if filename.endswith("ch2.out"): 
        os.rename("/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/{1}".format(args.folder,filename), "/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/Channel2/{1}".format(args.folder,filename))

    if filename.endswith("ch3.out"): 
        os.rename("/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/{1}".format(args.folder,filename), "/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/Channel3/{1}".format(args.folder,filename))

    if filename.endswith("ch4.out"): 
        os.rename("/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/{1}".format(args.folder,filename), "/Users/nathansonnina/ALICE/ALICE2020/Performance/{0}/Channel4/{1}".format(args.folder,filename))
