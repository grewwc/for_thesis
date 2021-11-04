import sys 
from astropy.io import fits
import matplotlib.pyplot as plt 
import numpy as np

def plot():     
    fname= sys.argv[1]
    h = fits.open(fname)    
    print(h.info())
    print(h[1].columns)
    data = h[1]
    time, flux = data.data['TIME'], data.data['PDCSAP_FLUX']
    # print(sorted(time), np.min(time))
    m = np.logical_or(np.isnan(time), np.isnan(flux))
    print(len(flux[m]), len(time))
    # plt.plot(time, flux)
    # plt.show()


plot()