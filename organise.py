import os
import numpy as np

# organises scintillator files into separate folders
# Uses absolute paths - put in your computers necessary file paths

for filename in os.listdir("C:/Users/kamee/OneDrive/Documents/alicePrac/data0793"):
    if filename.endswith("ch1.out"): 
        os.rename("C:/Users/kamee/OneDrive/Documents/alicePrac/data0793/%s" % filename, "C:/Users/kamee/OneDrive/Documents/alicePrac/data0793/Channel 1/%s" % filename)

    if filename.endswith("ch2.out"): 
        os.rename("C:/Users/kamee/OneDrive/Documents/alicePrac/data0793/%s" % filename, "C:/Users/kamee/OneDrive/Documents/alicePrac/data0793/Channel 2/%s" % filename)

    if filename.endswith("ch3.out"): 
        os.rename("C:/Users/kamee/OneDrive/Documents/alicePrac/data0793/%s" % filename, "C:/Users/kamee/OneDrive/Documents/alicePrac/data0793/Channel 3/%s" % filename)

    if filename.endswith("ch4.out"): 
        os.rename("C:/Users/kamee/OneDrive/Documents/alicePrac/data0793/%s" % filename, "C:/Users/kamee/OneDrive/Documents/alicePrac/data0793/Channel 4/%s" % filename)
