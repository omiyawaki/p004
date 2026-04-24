import os
import sys
sys.path.append('../')
sys.path.append('/home/miyawaki/scripts/common')
import dask
from dask.diagnostics import ProgressBar
import dask.multiprocessing
from concurrent.futures import ProcessPoolExecutor as Pool
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

varn='shus500'

mgen='cmip6'
fo = 'historical' # forcing (e.g., ssp245)
# fo = 'ssp370' # forcing (e.g., ssp245)

freq='day'

lmd=mods(fo) # create list of ensemble members

def saturation_mixing_ratio(p,t):
    # p in pa, T in K
    t=t-273.15
    es=1e2*6.112*np.exp(17.67*t/(t+243.5)) # *100 for Pa
    rs=c.ep*es/(p-es)
    return rs/(1+rs)

def calc_shus500(md):
    ens=emem(md)
    grd=grid(md,mgen)

    odir='/project/amp02/miyawaki/data/share/%s/%s/%s/%s/%s/%s/%s' % (mgen,fo,freq,varn,md,ens,grd)
    if not os.path.exists(odir):
        os.makedirs(odir)

    chk=0
    idir='/project/amp02/miyawaki/data/share/%s/%s/%s/%s/%s/%s/%s' % (mgen,fo,freq,'ta500',md,ens,grd)
    for _,_,files in os.walk(idir):
        for fn in files:
            ofn='%s/%s'%(odir,fn.replace('ta500',varn,1))
            if os.path.isfile(ofn):
                continue
            fn1='%s/%s'%(idir,fn)
            ds = xr.open_dataset(fn1)
            ta500=ds['ta500']
            # compute saturation sp humidity
            shus500=ta500.copy()
            shus500.data=saturation_mixing_ratio(500e2,ta500.data)
            shus500=shus500.rename(varn)
            shus500.to_netcdf(ofn)

# calc_shus500('KACE-1-0-G')
[calc_shus500(md) for md in tqdm(lmd)]

# if __name__=='__main__':
#     with Pool(max_workers=len(lmd)) as p:
#         p.map(calc_shus500,lmd)
