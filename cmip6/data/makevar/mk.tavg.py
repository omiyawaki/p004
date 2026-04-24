import os
import sys
sys.path.append('../')
sys.path.append('/home/miyawaki/scripts/common')
import dask
from dask.diagnostics import ProgressBar
from dask.distributed import Client
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

# collect warmings across the ensembles

nd=3 # number of days to average
budget='energy'
varn0='advtsurf'
varn='ta_ev' if varn0=='hfls' and budget=='water' else 'ta_%s'%varn0
se='sc'
doy=False
anom=False

mgen='cmip6'
fo0 = 'historical' # forcing (e.g., ssp245)
# byr0=[1950,1980]
byr0=[1980,2000]

fo = 'historical' # forcing (e.g., ssp245)
# byr=[1950,1980]
byr=[1980,2000]

# fo = 'rcp85' # forcing (e.g., ssp245)
# byr=[2070,2100]
# # byr='gwl2.0'

freq='day'

lmd=mods(fo) # create list of ensemble members
# lmd=['CanESM2','CNRM-CM5','CSIRO-Mk3-6-0','inmcm4','MPI-ESM-LR','MPI-ESM-MR']

def get_fn0(varn,md,fo,byr):
    idir='/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo,md,varn)
    if not os.path.exists(idir):
        os.makedirs(idir)
    if 'gwl' in byr:
        fn='%s/lm.%s_%s.%s.nc' % (idir,varn,byr,se)
    else:
        fn='%s/lm.%s_%g-%g.%s.nc' % (idir,varn,byr[0],byr[1],se)
    return fn

def calc_tavg(md):
    try:
        ens=emem(md)
        grd=grid(md,fo)

        odir='/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo,md,varn)
        if not os.path.exists(odir):
            os.makedirs(odir)

        print('\n Loading data...')
        vn=xr.open_dataarray(get_fn0(varn0,md,fo,byr))
        print('\n Done.')

        if anom:
            print('\n Computing anomaly from historical climatology...')
            vn0=xr.open_dataarray(get_fn0(varn0,md,fo0,byr0)) # historical
            vn=vn.groupby('time.dayofyear')-vn0.groupby('time.dayofyear').mean('time')
            print('\n Done.')

        print('\n Computing time average...')
        svn=vn.shift(time=1) # shift time backward by 1 to exclude current day
        tavn=svn.rolling(time=nd,center=False).mean(skipna=True) # average over previous nd days
        tavn=tavn/c.Lv if varn0=='hfls' and budget=='water' else tavn # convert LH to E
        print('\n Done.')

        # save
        vn.data=tavn
        vn=vn.rename(varn)
        vn.to_netcdf(get_fn0(varn,md,fo,byr),format='NETCDF4')
    except Exception as e:
        print(e)

# if __name__=='__main__':
#     calc_tavg('CESM2')
#     # [calc_tavg(md) for md in tqdm(lmd)]

if __name__=='__main__':
    with Pool(max_workers=len(lmd)) as p:
        p.map(calc_tavg,lmd)
