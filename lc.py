from astropy.io import fits
import matplotlib.pyplot as plt 
import requests
from info import common
import lightkurve as lk

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
    from concurrent.futures import ThreadPoolExecutor

    t = ThreadPoolExecutor(10)

    # def run(tic):
    #     lk.search_lightcurve(f'TIC {tic}').download_all()
        
    # fus = []
    # for tic in common:
    #     fus.append(t.submit(lambda: run(tic)))
        
    # t.shutdown()

    # res = []
    # for fu in fus:
    #     res.append(fu.result())

        
    # print(res)
    for tic in common:
        print(f' >>>  downloading {tic}')
        lk.search_lightcurve(f'TIC {tic}').download_all()
        print(f' <<< finished downloading {tic}')


download_lc()