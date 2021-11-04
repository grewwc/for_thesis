import sys 
from astropy.io import fits
import matplotlib.pyplot as plt 

def plot():     
    fname= sys.argv[1]
    h = fits.open(fname)    
    print(h.info())
    print(h[1].columns)
    data = h[1]
    time, flux = data.data['TIME'], data.data['PDCSAP_FLUX']
    plt.plot(time, flux)
    plt.show()


plot()