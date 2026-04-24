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

# lvn=['tas'] # input1
# lvn=['ta_advtsurf'] # input1
lvn=['advtsurf.ctas.d3'] # input1
se = 'sc' # season (ann, djf, mam, jja, son)

mgen='cmip6'
fo1='historical' # forcings 
his='1980-2000'
# his='1950-1980'

fo2='ssp370' # forcings 
fut='gwl2.0'
# fut='2070-2100'

# fo2='ssp585' # forcings 
# fut='2070-2100'

fo='%s-%s'%(fo2,fo1)

lmd=mods(fo1)
lmd.remove('NorESM2-LM')
lmd.remove('NorESM2-MM')
lmd.remove('TaiESM1')

# lmd=['MIROC6','IPSL-CM6A-LR','EC-Earth3','MPI-ESM1-2-LR','KACE-1-0-G','MRI-ESM2-0','CanESM5','MIROC-ES2L','MPI-ESM1-2-HR','ACCESS-CM2']
# lmd=['ACCESS-CM2','MPI-ESM1-2-HR','CanESM5','KACE-1-0-G','MPI-ESM1-2-LR','EC-Earth3','MIROC6']
# lmd=['CanESM2','CNRM-CM5','CSIRO-Mk3-6-0','inmcm4','MPI-ESM-LR','MPI-ESM-MR']

def calc_mmm(varn):
    varn0=varn

    for i,md in enumerate(tqdm(lmd)):
        print(md)
        idir1 = '/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo1,md,varn0)
        idir2 = '/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo2,md,varn)
        odir0 = '/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo,md,varn)
        if not os.path.exists(odir0):
            os.makedirs(odir0)

        c = 0
        dt={}

        # prc conditioned on temp
        pvn1=xr.open_dataarray('%s/ssc.%s_%s.%s.nc' % (idir1,varn0,his,se))
        pvn2=xr.open_dataarray('%s/ssc.%s_%s.%s.nc' % (idir2,varn,fut,se))

        # warming
        mvn1=pvn1.sel(stat=['mean'])
        mvn2=pvn2.sel(stat=['mean'])
        pvn1=pvn1.drop_sel(stat='mean')
        pvn2=pvn2.drop_sel(stat='mean')
        de1=pvn1-mvn1.data
        de2=pvn2-mvn2.data
        dpvn=pvn2-pvn1
        ddpvn=de2-de1
        # mvn1=xr.DataArray(mvn1.squeeze(),coords={'season':pvn1['season'],'gpi':pvn1['gpi']},dims=('season','gpi'))
        # mvn2=xr.DataArray(mvn2.squeeze(),coords={'season':pvn2['season'],'gpi':pvn2['gpi']},dims=('season','gpi'))
        dmvn=mvn2-mvn1
        print(np.nanmax(ddpvn.data.flatten()))
        print(np.nanmin(ddpvn.data.flatten()))

        # save individual model data
        mvn1.to_netcdf('%s/avg.%s_%s.%s.nc' % (idir1,varn,his,se))
        mvn2.to_netcdf('%s/avg.%s_%s.%s.nc' % (idir2,varn,fut,se))
        dmvn.to_netcdf('%s/d.avg.%s_%s_%s.%s.nc' % (odir0,varn,his,fut,se))
        dpvn.to_netcdf('%s/dpc.avg.%s_%s_%s.%s.nc' % (odir0,varn,his,fut,se))
        ddpvn.to_netcdf('%s/ddpc.avg.%s_%s_%s.%s.nc' % (odir0,varn,his,fut,se))

        if i==0:
            imvn1=np.empty(np.insert(np.asarray(mvn1.shape),0,len(lmd)))
            imvn2=np.empty(np.insert(np.asarray(mvn2.shape),0,len(lmd)))
            ipvn1=np.empty(np.insert(np.asarray(pvn1.shape),0,len(lmd)))
            ipvn2=np.empty(np.insert(np.asarray(pvn2.shape),0,len(lmd)))
            idmvn=np.empty(np.insert(np.asarray(dmvn.shape),0,len(lmd)))
            idpvn=np.empty(np.insert(np.asarray(dpvn.shape),0,len(lmd)))
            iddpvn=np.empty(np.insert(np.asarray(ddpvn.shape),0,len(lmd)))

        imvn1[i,...]=mvn1
        imvn2[i,...]=mvn2
        ipvn1[i,...]=pvn1
        ipvn2[i,...]=pvn2
        idmvn[i,...]=dmvn
        idpvn[i,...]=dpvn
        iddpvn[i,...]=ddpvn

    # compute mmm and std
    mmvn1=mvn1.copy()
    mmvn2=mvn2.copy()
    mmvn1.data=np.nanmean(imvn1,axis=0)
    mmvn2.data=np.nanmean(imvn2,axis=0)

    smvn1=mvn1.copy()
    smvn2=mvn2.copy()
    smvn1.data=np.nanstd(imvn1,axis=0)
    smvn2.data=np.nanstd(imvn2,axis=0)

    mpvn1=pvn1.copy()
    mpvn2=pvn2.copy()
    mpvn1.data=np.nanmean(ipvn1,axis=0)
    mpvn2.data=np.nanmean(ipvn2,axis=0)

    spvn1=pvn1.copy()
    spvn2=pvn2.copy()
    spvn1.data=np.nanstd(ipvn1,axis=0)
    spvn2.data=np.nanstd(ipvn2,axis=0)

    mdmvn=dmvn.copy()
    mdmvn.data=np.nanmean(idmvn,axis=0)
    sdmvn=dmvn.copy()
    sdmvn.data=np.nanstd(idmvn,axis=0)

    mdpvn=dpvn.copy()
    mdpvn.data=np.nanmean(idpvn,axis=0)
    sdpvn=dpvn.copy()
    sdpvn.data=np.nanstd(idpvn,axis=0)

    mddpvn=ddpvn.copy()
    mddpvn.data=np.nanmean(iddpvn,axis=0)
    sddpvn=ddpvn.copy()
    sddpvn.data=np.nanstd(iddpvn,axis=0)

    # save mmm and std
    odir1 = '/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo1,'mmm',varn)
    if not os.path.exists(odir1):
        os.makedirs(odir1)
    odir2 = '/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo2,'mmm',varn)
    if not os.path.exists(odir2):
        os.makedirs(odir2)
    odir = '/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo,'mmm',varn)
    if not os.path.exists(odir):
        os.makedirs(odir)

    mmvn1.to_netcdf('%s/avg.%s_%s.%s.nc' % (odir1,varn,his,se))
    smvn1.to_netcdf('%s/std.avg.%s_%s.%s.nc' % (odir1,varn,his,se))
    mmvn2.to_netcdf('%s/avg.%s_%s.%s.nc' % (odir2,varn,fut,se))
    smvn2.to_netcdf('%s/std.avg.%s_%s.%s.nc' % (odir2,varn,fut,se))

    mpvn1.to_netcdf('%s/pc.%s_%s.%s.nc' % (odir1,varn,his,se))
    spvn1.to_netcdf('%s/std.pc.%s_%s.%s.nc' % (odir1,varn,his,se))
    mpvn2.to_netcdf('%s/pc.%s_%s.%s.nc' % (odir2,varn,fut,se))
    spvn2.to_netcdf('%s/std.pc.%s_%s.%s.nc' % (odir2,varn,fut,se))

    mdmvn.to_netcdf('%s/d.avg.%s_%s_%s.%s.nc' % (odir,varn,his,fut,se))
    sdmvn.to_netcdf('%s/std.d.avg.%s_%s_%s.%s.nc' % (odir,varn,his,fut,se))

    mdpvn.to_netcdf('%s/dpc.avg.%s_%s_%s.%s.nc' % (odir,varn,his,fut,se))
    sdpvn.to_netcdf('%s/std.dpc.avg.%s_%s_%s.%s.nc' % (odir,varn,his,fut,se))

    mddpvn.to_netcdf('%s/ddpc.avg.%s_%s_%s.%s.nc' % (odir,varn,his,fut,se))
    sddpvn.to_netcdf('%s/std.ddpc.avg.%s_%s_%s.%s.nc' % (odir,varn,his,fut,se))

[calc_mmm(vn) for vn in lvn]
