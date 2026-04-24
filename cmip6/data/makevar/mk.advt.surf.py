import os
import sys
sys.path.append('../')
sys.path.append('/home/miyawaki/scripts/common')
from concurrent.futures import ProcessPoolExecutor as Pool
import numpy as np
import xarray as xr
import constants as c
from tqdm import tqdm
from util import mods,simu,emem
from glade_utils import grid
from scipy.interpolate import interp1d

# collect warmings across the ensembles

slev='surf'
ivar='advt'
varn='%s%s'%(ivar,slev)
gvar='gradt%s'%slev
uvar='uas'
vvar='vas'

mgen='cmip6'
fo = 'historical' # forcing (e.g., ssp245)
# fo = 'ssp370' # forcing (e.g., ssp245)
# fo = 'ssp585' # forcing (e.g., ssp245)

# mgen='cmip5'
# fo='historical'
# # fo='rcp85' # forcing (e.g., ssp245)

checkexist=False
freq='day'

lmd=mods(fo) # create list of ensemble members
# lmd=['CanESM2','CNRM-CM5','CSIRO-Mk3-6-0','inmcm4','MPI-ESM-LR','MPI-ESM-MR']

def calc_adv(md):
    try:
        ens=emem(md)
        grd=grid(md,mgen)

        odir='/project/amp02/miyawaki/data/share/%s/%s/%s/%s/%s/%s%s' % (mgen,fo,freq,varn,md,ens,grd)
        if not os.path.exists(odir):
            os.makedirs(odir)

        idir='/project/amp02/miyawaki/data/share/%s/%s/%s/%s/%s/%s%s' % (mgen,fo,freq,gvar,md,ens,grd)
        for _,_,files in os.walk(idir):
            print(files)
            for fn in files:
                ofn='%s/%s'%(odir,fn.replace(gvar,varn))
                if checkexist and os.path.isfile(ofn):
                    continue
                try:
                    fn1='%s/%s'%(idir,fn)
                    ds = xr.open_dataset(fn1)
                    dx=ds['dx']
                    dy=ds['dy']
                    fn1=fn1.replace(gvar,uvar)
                    fn1=fn1.replace('/amp02/miyawaki/data/share','')
                    ds = xr.open_dataset(fn1)
                    ua=ds[uvar]
                    fn1=fn1.replace(uvar,vvar)
                    ds = xr.open_dataset(fn1)
                    va=ds[vvar]

                    # total horizontal advection
                    if not va.shape==ua.shape:
                        va=va.interp(lat=ua['lat'])

                    adv=ua.copy()
                    adv.data=ua.data*dx.data+va.data*dy.data

                    adv=adv.rename(varn)
                    adv.to_netcdf(ofn)
                except Exception as e:
                    print(e)
                    print('WARNING skipping %s'%ofn)
    except Exception as e:
        print(e)

# calc_adv(lmd[0])
# [calc_adv(md) for md in tqdm(lmd)]

if __name__=='__main__':
    with Pool(max_workers=len(lmd)) as p:
        p.map(calc_adv,lmd)
