import os
import sys
sys.path.append('../')
sys.path.append('/home/miyawaki/scripts/common')
import dask
from dask.diagnostics import ProgressBar
import dask.multiprocessing
import pickle
import numpy as np
import xesmf as xe
import xarray as xr
import constants as c
from tqdm import tqdm
from util import mods,simu,emem
from glade_utils import grid
# from metpy.calc import saturation_mixing_ratio,specific_humidity_from_mixing_ratio
# from metpy.units import units

# collect warmings across the ensembles

varn='bo'

mgen = 'cmip6'
fo = 'historical' # forcing (e.g., ssp245)
# fo = 'ssp370' # forcing (e.g., ssp245)

freq='day'

lmd=mods(fo) # create list of ensemble members

def calc_bo(md):
    ens=emem(md)
    grd=grid(md, mgen)

    odir='/project/amp02/miyawaki/data/share/cmip6/%s/%s/%s/%s/%s%s' % (fo,freq,varn,md,ens,grd)
    if not os.path.exists(odir):
        os.makedirs(odir)

    idir='/project/cmip6/%s/%s/%s/%s/%s%s' % (fo,freq,'hfls',md,ens,grd)
    for _,_,files in os.walk(idir):
        for fn in files:
            try:
                ofn='%s/%s'%(odir,fn.replace('hfls',varn))
                if os.path.isfile(ofn):
                    continue
                fn1='%s/%s'%(idir,fn)
                ds = xr.open_dataset(fn1)
                hfls=ds['hfls']
                fn1=fn1.replace('hfls','hfss')
                ds = xr.open_dataset(fn1)
                hfss=ds['hfss']
                # compute net surface radiative heating
                bo=hfls.copy()
                bo.data=hfss.data/hfls.data
                bo=bo.rename(varn)
                bo.to_netcdf(ofn)
            except Exception as e:
                print(e)
                print(f'Skipping {fn}')

calc_bo('CESM2')

# if __name__ == '__main__':
#     with ProgressBar():
#         tasks=[dask.delayed(calc_bo)(md) for md in lmd]
#         dask.compute(*tasks,scheduler='processes')
#         # dask.compute(*tasks,scheduler='single-threaded')
