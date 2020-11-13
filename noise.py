#!/usr/bin/env python3

#import defaults
import o32reader as rdr
import adcarray as adc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import itertools
import argparse
from roi import regions_of_interest
import scipy
from scipy.optimize import curve_fit,minimize_scalar 
from scipy import asarray as ar,exp
from scipy.stats import norm


if __name__ == "__main__":

    # ------------------------------------------------------------------------
    # generate a parser for the command line arguments
    parser = argparse.ArgumentParser(description='Generate a pulse-height plot.')
    parser.add_argument('filename', help='the TRD raw data file to process')
    parser.add_argument('--printargs', action='store_true',
                        help='print arguments and exit')

    args = parser.parse_args()

    if args.printargs:
        print (args)
        exit(0)

    def gaus(x,a,x0,sigma):
        return (a/(sigma*np.sqrt(2*np.pi))*exp(-((x-x0)**2)/(2*sigma**2)))

    # ------------------------------------------------------------------------
    # Load the data from the preprocessed .npy file
    alldata = np.load(args.filename,allow_pickle=True)
    rows = np.arange(0,12,1)
    pads = np.arange(3,144,1)

    d = np.average(alldata, axis=(0,3))
    s = np.std(alldata, axis=(0,3))

    #print((d))
    DATA_EXCLUDE_MASK = np.zeros((12, 144), dtype=bool)
    # DATA_EXCLUDE_MASK[4:8,0:144,:] = True
    
    
    #EDIT EXCLUDE MASK VALUE TO EXCLUDE WHICHEVER READOUT PADS ARE BROKEN - ASK TOM
    DATA_EXCLUDE_MASK [8:12, 0:72] = True
    d[DATA_EXCLUDE_MASK] = 0
    s[DATA_EXCLUDE_MASK] = 0

    #contour plot of means of ADC values of TRD - finding baseline of TRD
    plt.pcolor(pads,rows,d[0:12,3:144])
    plt.colorbar(label="$\mu$")
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.title("Baseline across the TRD")
    plt.show()

    #contour plot of standard deviations of ADC values of TRD - finding baseline standard deviation of TRD
    plt.pcolor(pads,rows,s[0:12,3:144])
    plt.colorbar(label="$\sigma$")
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.title("Noise across the TRD")
    plt.show()

    # plot histogram of frequency of the mean ADC values
    hist, bins = np.histogram(d[0:12,3:144], np.linspace(9, 10.5, 500))
    centres = (bins[1:] + bins[:-1]) / 2
    x = np.linspace(9,10.2,1000)
    u = centres**0.5
    mu, sigma = scipy.stats.norm.fit(d[0:12,3:144])

    #fitted gaussian - not completely necessary but sometimes useful
    popt,pcov = curve_fit(gaus,centres,hist,p0=[100,mu,sigma])
    print("mean 1 =", popt[1], "+/-", pcov[1,1]**0.5)
    print("sigma 1 =", popt[2], "+/-", pcov[2,2]**0.5)

    dymin = (hist-gaus(centres,*popt))/u
    min_chisq = sum(dymin*dymin)
    dof =len(centres)-len(popt)

    print("Chi square:", min_chisq )
    print("Number of degrees of freedom:",dof)
    print("Chi square per degree of freedom:" , min_chisq/dof )
    print()

    #plt.plot(x,gaus(x,*popt),'r--',label='Gaussian fit',markersize=1)
    width = bins[1] - bins[0]
    plt.bar(bins[:-1], hist, width, align='edge', log=True)
    plt.xlabel('$\mu$')
    plt.ylabel('Frequency')
    plt.title("Binned Baseline Data")
    plt.show()
