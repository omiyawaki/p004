import os
import sys
sys.path.append('../../data/')
sys.path.append('/home/miyawaki/scripts/common')
import pickle
import numpy as np
import xarray as xr
from tqdm import tqdm
from util import mods
from utils import monname

lvn=['tas'] # input1
se = 'sc' # season (ann, djf, mam, jja, son)
fo1='historical' # forcings 
fo2='ssp370' # forcings 
fo='%s-%s'%(fo2,fo1)
his='1950-1980'
fut='2070-2100'

lmd=mods(fo1)

def calc_mmm(varn):
    varn0=varn

    for i,md in enumerate(tqdm(lmd)):
        print(md)
        idir1 = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo1,md,varn0)
        idir2 = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo2,md,varn)
        odir0 = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,varn)
        if not os.path.exists(odir0):
            os.makedirs(odir0)

        c = 0
        dt={}

        # prc conditioned on temp
        pvn1=xr.open_dataarray('%s/ss.%s_%s.%s.nc' % (idir1,varn0,his,se))
        pvn2=xr.open_dataarray('%s/ss.%s_%s.%s.nc' % (idir2,varn,fut,se))

        # warming
        vvn1=pvn1.sel(stat=['var'])
        vvn2=pvn2.sel(stat=['var'])
        dvvn=vvn2-vvn1

        # save individual model data
        vvn1.to_netcdf('%s/var.%s_%s.%s.nc' % (idir1,varn,his,se))
        vvn2.to_netcdf('%s/var.%s_%s.%s.nc' % (idir2,varn,fut,se))

        if i==0:
            ivvn1=np.empty(np.insert(np.asarray(vvn1.shape),0,len(lmd)))
            ivvn2=np.empty(np.insert(np.asarray(vvn2.shape),0,len(lmd)))
            idvvn=np.empty(np.insert(np.asarray(dvvn.shape),0,len(lmd)))

        ivvn1[i,...]=vvn1
        ivvn2[i,...]=vvn2
        idvvn[i,...]=dvvn

    # compute mmm and std
    mvvn1=vvn1.copy()
    mvvn2=vvn2.copy()
    mvvn1.data=np.nanmean(ivvn1,axis=0)
    mvvn2.data=np.nanmean(ivvn2,axis=0)

    svvn1=vvn1.copy()
    svvn2=vvn2.copy()
    svvn1.data=np.nanstd(ivvn1,axis=0)
    svvn2.data=np.nanstd(ivvn2,axis=0)

    mdvvn=dvvn.copy()
    mdvvn.data=np.nanmean(idvvn,axis=0)
    sdvvn=dvvn.copy()
    sdvvn.data=np.nanstd(idvvn,axis=0)

    # save mmm and std
    odir1 = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo1,'mmm',varn)
    if not os.path.exists(odir1):
        os.makedirs(odir1)
    odir2 = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo2,'mmm',varn)
    if not os.path.exists(odir2):
        os.makedirs(odir2)
    odir = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,'mmm',varn)
    if not os.path.exists(odir):
        os.makedirs(odir)

    mvvn1.to_netcdf('%s/var.%s_%s.%s.nc' % (odir1,varn,his,se))
    svvn1.to_netcdf('%s/std.var.%s_%s.%s.nc' % (odir1,varn,his,se))
    mvvn2.to_netcdf('%s/var.%s_%s.%s.nc' % (odir2,varn,fut,se))
    svvn2.to_netcdf('%s/std.var.%s_%s.%s.nc' % (odir2,varn,fut,se))

    mdvvn.to_netcdf('%s/d.var.%s_%s_%s.%s.nc' % (odir,varn,his,fut,se))
    sdvvn.to_netcdf('%s/std.d.var.%s_%s_%s.%s.nc' % (odir,varn,his,fut,se))

[calc_mmm(vn) for vn in lvn]
