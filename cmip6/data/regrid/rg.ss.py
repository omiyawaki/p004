import os,sys
sys.path.append('../')
sys.path.append('/home/miyawaki/scripts/common')
import pickle
import numpy as np
import xarray as xr
import constants as c
from tqdm import tqdm
from glade_utils import grid
from util import mods,simu,emem,load_raw
from concurrent.futures import ProcessPoolExecutor as Pool

lsn=['djf','mam','jja','son']
varn='tas' # input1
ty='2d'
checkexist=False

fo = 'historical' # forcing (e.g., ssp245)
byr=[1950,1980]

# fo = 'ssp370' # forcing (e.g., ssp245)
# byr=[2070,2100]

freq='day'
se='sc'

# for regridding
rgdir='/project/amp/miyawaki/data/share/regrid'
# open CESM data to get output grid
cfil='%s/f.e11.F1850C5CNTVSST.f09_f09.002.cam.h0.PHIS.040101-050012.nc'%rgdir
cdat=xr.open_dataset(cfil)
ogr=xr.Dataset({'lat': (['lat'], cdat['lat'].data)}, {'lon': (['lon'], cdat['lon'].data)})

lmd=mods(fo) # create list of ensemble members

def calc_pvn(md):
    ens=emem(md)
    grd=grid(md)

    idir='/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,varn)
    odir='/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,varn)
    if not os.path.exists(odir):
        os.makedirs(odir)

    oname='%s/ss.%s_%g-%g.%s.nc' % (odir,varn,byr[0],byr[1],se)

    if checkexist:
        if os.path.isfile(oname):
            print('Output file already exists, skipping...')
            return

    ds=load_raw(odir,varn,byr,se)
    vn=ds[varn]

    # select data within time of interest
    print('\n Selecting data within range of interest...')
    vn=vn.sel(time=vn['time.year']>=byr[0])
    vn=vn.sel(time=vn['time.year']<byr[1])
    otime=vn['time'].sel(time=vn['time.year']==byr[0])
    print('\n Done.')

    time=vn['time']
    ngp=vn.shape[1]

    ovn=np.empty([len(lsn),4,vn.shape[1]])
    # compute seasonal climatology
    print('\n Computing seasonal min mean max...')

    vnmin=vn.resample(time='QS-DEC').min()
    vnavg=vn.resample(time='QS-DEC').mean()
    vnvar=vn.resample(time='QS-DEC').std()**2
    vnmax=vn.resample(time='QS-DEC').max()
    for i,sn in enumerate(tqdm(lsn)):
        ovn[i,0,:]=vnmin.sel(time=vnmin['time.season']==sn.upper()).mean('time')
        ovn[i,1,:]=vnavg.sel(time=vnavg['time.season']==sn.upper()).mean('time')
        ovn[i,2,:]=vnvar.sel(time=vnvar['time.season']==sn.upper()).mean('time')
        ovn[i,3,:]=vnmax.sel(time=vnmax['time.season']==sn.upper()).mean('time')

    ovn=xr.DataArray(ovn,coords={'season':lsn,'stat':['min','mean','var','max'],'gpi':np.arange(ngp)},dims=('season','stat','gpi'))

    ovn.to_netcdf(oname,format='NETCDF4')

# calc_pvn('CESM2')
# # [calc_pvn(md) for md in tqdm(lmd)]

if __name__=='__main__':
    with Pool(max_workers=len(lmd)) as p:
        p.map(calc_pvn,lmd)
