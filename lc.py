from astropy.io import fits
import matplotlib.pyplot as plt
import requests
import lightkurve as lk
import warnings
import os
import shutil
import numpy as np
from helpers.preprocessing import *

# warnings.filterwarnings("error")

cur_file_dir = os.path.dirname(__file__)


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


# works
# have downloaded
def download_lc():
    def get_tic_sector_from_url(url):
        url = url.strip()
        target = url.split('/')[-1].strip()
        sector, tic = url.split('-')[1:3]
        sector = sector[1:]
        return tic, sector

    def requests_download(url):
        tic, sector = get_tic_sector_from_url(url)
        fname = url.split('/')[-1]
        local_filename = os.path.join(cur_file_dir, 'data', 'lightcurve', tic, sector, fname)
        if not os.path.exists(os.path.dirname(local_filename)):
            os.makedirs(os.path.dirname(local_filename))

        print(f"{local_filename}")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return local_filename

    # download all common tic
    from concurrent.futures import ThreadPoolExecutor
    t = ThreadPoolExecutor(100)
    fus = []
    cnt = 0
    with open(os.path.join(cur_file_dir, 'data', 'all_light_curve.sh')) as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            fus.append(t.submit(requests_download, line))

    t.shutdown()
    for fu in fus:
        fu.result()


def merge_lc_gen_global_local(tic):
    if isinstance(tic, str):
        tic = int(tic)

    tic = f'{tic:016d}'
    rootdir = os.path.join(cur_file_dir, 'data', 'lightcurve', tic)
    time = None
    flux = None

    for sub in os.listdir(rootdir):
        fname = os.path.join(rootdir, sub)
        fname = os.path.join(fname, os.listdir(fname)[0])
        h = fits.open(fname)
        data = h[1]
        curtime, curflux = data.data['TIME'], data.data['PDCSAP_FLUX']
        mask = np.logical_not(np.logical_or(np.isnan(curtime), np.isnan(curflux)))
        curtime = curtime[mask]
        curflux = curflux[mask]
        curflux = curflux / np.mean(curflux)

        if time is None:
            time = curtime
            flux = curflux
        else:
            time = np.concatenate([time, curtime])
            flux = np.concatenate([flux, curflux])

    # print(time.shape, flux.shape)
    period_list = [3.81429, 319.93800]
    t0_list = [1327.42, 1350.32]
    duration_list = [1.4038/24, 14.9009/24]
    planet_nums = [1, 2]
    for i, (period, t0, duration, planet_num) in \
            enumerate(zip(
                period_list,
                t0_list,
                duration_list,
                planet_nums
            )):

        cur_time, cur_flux = remove_points_other_tce(
            time, flux, period, period_list=period_list,
            t0_list=t0_list, duration_list=duration_list
        )

        global_flux = process_global(
            cur_time, cur_flux, period, t0, duration
        )

        local_flux = process_local(
            cur_time, cur_flux, period, t0, duration, center_ratio=7
        )

        # print(cur_time, cur_flux)
        plt.plot(global_flux, '.', ms=0.8)
        plt.show()


tic = "0000000260004324"


merge_lc_gen_global_local(tic)
