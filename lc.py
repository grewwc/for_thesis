from astropy.io import fits
import matplotlib.pyplot as plt 

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


quick_plot('470911286', 24)
