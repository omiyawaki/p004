import os,sys
sys.path.append('../')
sys.path.append('/home/miyawaki/scripts/common')
import pickle
import numpy as np
import xarray as xr
import pandas as pd
import constants as c
from tqdm import tqdm
from glade_utils import grid
from util import mods,simu,emem,load_raw
from concurrent.futures import ProcessPoolExecutor as Pool

lsn=['djf','mam','jja','son']
varn='advtsurf' # input1
cvar='tas'
d=3 # number of days to average prior to seasonal min/max
ovarn='%s.c%s.d%g'%(varn,cvar,d)
ty='2d'
checkexist=False

##################################################
mgen='cmip6'

# fo = 'historical' # forcing (e.g., ssp245)
# # byr=[1980,2000]
# byr=[1950,1980]

fo = 'ssp370' # forcing (e.g., ssp245)
byr='gwl2.0'
# byr=[2070,2100]

# fo = 'ssp585' # forcing (e.g., ssp245)
# byr=[2070,2100]

lmd=mods(fo) # create list of ensemble members

###################################################
# mgen='cmip5'
# lmd=['CanESM2','CNRM-CM5','CSIRO-Mk3-6-0','inmcm4','MPI-ESM-LR','MPI-ESM-MR']

# # fo = 'historical' # forcing (e.g., ssp245)
# # byr=[1950,1980]

# fo = 'rcp85' # forcing (e.g., ssp245)
# byr=[2070,2100]

freq='day'
se='sc'

# for regridding
rgdir='/project/amp/miyawaki/data/share/regrid'
# open CESM data to get output grid
cfil='%s/f.e11.F1850C5CNTVSST.f09_f09.002.cam.h0.PHIS.040101-050012.nc'%rgdir
cdat=xr.open_dataset(cfil)
ogr=xr.Dataset({'lat': (['lat'], cdat['lat'].data)}, {'lon': (['lon'], cdat['lon'].data)})


def calc_pvn(md):
    try:
        ens=emem(md)

        odir='/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo,md,ovarn)
        if not os.path.exists(odir):
            os.makedirs(odir)

        if 'gwl' in byr:
            oname='%s/ssc.%s_%s.%s.nc' % (odir,ovarn,byr,se)
        else:
            oname='%s/ssc.%s_%g-%g.%s.nc' % (odir,ovarn,byr[0],byr[1],se)

        if checkexist:
            if os.path.isfile(oname):
                print('Output file already exists, skipping...')
                return

        # load variable of interest and conditioning variable 
        def loadvar(varn0,byr0):
            idir='/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo,md,varn0)
            return load_raw(idir,varn0,byr0,se)[varn0]

        vn=loadvar(varn,byr)
        cvn=loadvar(cvar,byr)
        cvn=cvn.drop_isel(time=np.arange(d)) # drop first d days

        time=vn['time']
        ngp=vn.shape[1]

        ovn=np.empty([len(lsn),3,vn.shape[1]])
        # compute seasonal climatology
        print('\n Computing seasonal min mean max...')
        vnavg=vn.resample(time='QS-DEC').mean()

        # Group by season and find the index of the minimum value within each group
        def get_seasonal_min_indices(group):
            return group.idxmin(dim='time')
        idmin=cvn.groupby('time.year').apply(lambda group: group.groupby('time.season').apply(get_seasonal_min_indices))
        idmin=idmin.rename({'year':'time'})

        def get_seasonal_max_indices(group):
            return group.idxmax(dim='time')
        idmax=cvn.groupby('time.year').apply(lambda group: group.groupby('time.season').apply(get_seasonal_max_indices))
        idmax=idmax.rename({'year':'time'})

        # Shifts datetime in datarray by d days
        def shiftdate(xvn0,d0):
            xvn=xvn0.copy()
            xvn.data=xvn.data+pd.Timedelta(days=d0)
            return xvn

        # aggregate 3 days prior to seasonal min/max date
        idmin=xr.concat([shiftdate(idmin,d) for d in tqdm(np.arange(-d,0,1))],dim='time')
        idmax=xr.concat([shiftdate(idmax,d) for d in tqdm(np.arange(-d,0,1))],dim='time')

        for i,sn in enumerate(tqdm(lsn)):
            ovn[i,0,:]=vn.sel(time=idmin.sel(season=sn.upper())).mean('time')
            ovn[i,1,:]=vnavg.sel(time=vnavg['time.season']==sn.upper()).mean('time')
            ovn[i,2,:]=vn.sel(time=idmax.sel(season=sn.upper())).mean('time')

        ovn=xr.DataArray(ovn,name=ovarn,coords={'season':lsn,'stat':['min','mean','max'],'gpi':np.arange(ngp)},dims=('season','stat','gpi'))

        ovn.to_netcdf(oname,format='NETCDF4')
    except Exception as e:
        print(e)

# calc_pvn('MPI-ESM1-2-HR')
[calc_pvn(md) for md in tqdm(lmd)]

# if __name__=='__main__':
#     with Pool(max_workers=len(lmd)) as p:
#         p.map(calc_pvn,lmd)
