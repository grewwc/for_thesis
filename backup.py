from astropy.io import fits
import matplotlib.pyplot as plt 
import requests
from info import common
import lightkurve as lk
import warnings
warnings.filterwarnings("error")

data_dir = "/Users/wwc129/phd_data/mastDownload/HLSP/"
llc_format = "hlsp_qlp_tess_ffi_s{:04d}-{:016d}_tess_v01_llc"

def combine_lightcurves_by_id_and_sector(id_, sector):
    if isinstance(id_, str):
        id_ = int(id_)
    if isinstance(sector, str):
        sector = int(sector)

    formated = llc_format.format(sector, id_)
    fname = data_dir + formated + '/' + formated + '.fits'
    return fname 

def quick_plot(id_, sector):
    absname = combine_lightcurves_by_id_and_sector(id_, sector)
    data = fits.open(absname)[1]
    time, flux = data.data['TIME'], data.data['KSPSAP_FLUX']
    plt.plot(time, flux)
    plt.show()


def download_lc():
    # download all common tic 

    def run(tic):
        print(f' >>>  downloading {tic}')
        lk.search_lightcurve(f'TIC {tic}').download_all()
        return tic
        
    fus = []
    f = open("finished.txt", 'w')
    failed = open("failed.txt", 'w')

    with warnings.catch_warnings(record=True) as w:
        for tic in common:    
            try:
                run(tic)
                print(f' <<< finished downloading {res[-1]}')
                f.write(f"{tic}\n")
                f.flush()
            except:
                print(f"FAILED: {tic}")
                failed.write(f'{tic}\n')
                failed.flush()


    f.close()
    failed.close()

    
# download_lc()

lk.search_lightcurve("TIC 458856474").download_all()