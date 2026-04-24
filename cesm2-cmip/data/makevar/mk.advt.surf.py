import os
import sys
sys.path.append('../')
sys.path.append('/home/miyawaki/scripts/common')
from concurrent.futures import ProcessPoolExecutor as Pool
import numpy as np
import xarray as xr
import constants as c
from tqdm import tqdm
from util import casename
from cesmutils import realm,history

# collect warmings across the ensembles

varn='ADVTSURF'

fo = 'historical' # forcing (e.g., ssp245)
# fo = 'ssp370' # forcing (e.g., ssp245)

checkexist=False
freq='day'

cname=casename(fo)

def calc_adv(md):
    rlm=realm(varn.lower())
    hst=history(varn.lower())

    idir='/project/amp02/miyawaki/data/share/cesm2/%s/%s/proc/tseries/%s_1' % (cname,rlm,freq)
    odir=idir
    for _,_,files in os.walk(idir):
        files=[fn for fn in files if '.TREFHT.' in fn]
        for fn in tqdm(files):
            print(fn)
            ofn='%s/%s'%(odir,fn.replace('.TREFHT.','.%s.'%varn))
            if checkexist and os.path.isfile(ofn):
                continue
            fn1='%s/%s'%(idir,fn)
            ta=xr.open_dataset(fn1)['TREFHT']
            fn1=fn1.replace('.TREFHT.','.UBOT.')
            ua=xr.open_dataset(fn1)['UBOT']
            fn1=fn1.replace('.UBOT.','.VBOT.')
            va=xr.open_dataset(fn1)['VBOT']
            time=ta['time']
            xlat=ta['lat']
            xlon=ta['lon']

            lat=np.deg2rad(ta['lat'].data)
            lon=np.deg2rad(ta['lon'].data)

            # compute grad(doy mean(T))
            lonm=1/2*(lon[1:]+lon[:-1])
            latm=1/2*(lat[1:]+lat[:-1])
            clat=np.transpose(np.tile(np.cos(lat),(1,1,1)),[0,2,1])
            clatm=np.transpose(np.tile(np.cos(latm),(1,1,1)),[0,2,1])
            ta=ta.data
            # zonal derivative
            taym=1/2*(ta[:,1:,:]+ta[:,:-1,:]) # meridional midpoints
            dxm=1/(c.a*clatm)*(taym[...,1:]-taym[...,:-1])/(lon[1:]-lon[:-1])
            # meridional divergence
            taxm=1/2*(ta[...,1:]+ta[...,:-1]) # zonal midpoints
            dym=1/(c.a)*(taxm[:,1:,:]-taxm[:,:-1,:])/(lat[1:]-lat[:-1]).reshape([1,len(latm),1])

            # evaluate at original grid
            lonmd=np.rad2deg(lonm)
            latmd=np.rad2deg(latm)
            dxm=xr.DataArray(dxm,name='dx',coords={'time':time,'lat':latmd,'lon':lonmd},dims=('time','lat','lon'))
            dym=xr.DataArray(dym,name='dy',coords={'time':time,'lat':latmd,'lon':lonmd},dims=('time','lat','lon'))
            dx=dxm.interp(lat=xlat,lon=xlon)
            dy=dym.interp(lat=xlat,lon=xlon)

            # total horizontal advection
            adv=ua*dx+va*dy

            # save
            adv=adv.rename(varn)
            adv.to_netcdf(ofn)

calc_adv('CESM2')

# if __name__=='__main__':
#     with Pool(max_workers=len(lmd)) as p:
#         p.map(calc_adv,lmd)
