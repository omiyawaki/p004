import os
import sys
sys.path.append('../../data/')
sys.path.append('/home/miyawaki/scripts/common')
import dask
from dask.distributed import Client
import dask.multiprocessing
from concurrent.futures import ProcessPoolExecutor as Pool
import pickle
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from scipy.stats import gaussian_kde
from tqdm import tqdm
from util import mods
from utils import corr,corr2d,monname,varnlb,unitlb
from regions import pointlocs
from etregimes import bestfit
from CASutils import shapefile_utils as shp

# relb='fourcorners'
# re=['Utah','Colorado','Arizona','New Mexico']

lrelb=['swus']

varn1='hfls'
varn2='mrsos'
varn='%s+%s'%(varn1,varn2)
se='sc'
mo=7

fo1='historical' # forcings 
yr1='1980-2000'

fo2='ssp370' # forcings 
yr2='gwl2.0'

fo='%s+%s'%(fo1,fo2)
fod='%s-%s'%(fo2,fo1)

# md='CanESM5'
# md='CESM2'
# md='MPI-ESM1-2-LR'
lmd=mods(fo1)
lmd = ['CESM2']

# load ocean indices
latgpi,longpi=pickle.load(open('/project/amp/miyawaki/data/share/lomask/cesm2/lmilatlon.pickle','rb'))

# grid
rgdir='/project/amp/miyawaki/data/share/regrid'
# open CESM data to get output grid
cfil='%s/f.e11.F1850C5CNTVSST.f09_f09.002.cam.h0.PHIS.040101-050012.nc'%rgdir
cdat=xr.open_dataset(cfil)
gr=xr.Dataset({'lat': (['lat'], cdat['lat'].data)}, {'lon': (['lon'], cdat['lon'].data)})

def load_data(md,fo,varn,igpi,yr):
    idir = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,varn)
    ds=xr.open_dataset('%s/lm.%s_%s.%s.nc' % (idir,varn,yr,se))
    vn=ds[varn]
    gpi=ds['gpi']
    # select data
    vn=vn.sel(time=vn['time.month']==mo, gpi=igpi)
    return vn

def bcmon(ibin, vn1,vn2, btas):
    svn1 = vn1.where(btas == ibin)
    svn2 = vn2.where(btas == ibin)
    csm=np.nan
    mtr=np.nan
    nvn1=svn1.data.flatten()
    nvn2=svn2.data.flatten()
    nans=np.logical_or(np.isnan(nvn1),np.isnan(nvn2))
    nvn1=nvn1[~nans]
    nvn2=nvn2[~nans]
    try:
        f1,f2=bestfit(nvn2,nvn1)
        bc=f2['line']
        csm=f2['xc']
        mtr=f2['mt']
    except Exception as e:
        print(e)
        bc = None
    return bc,csm,mtr

def plot(relb,fo=fo1,yr=yr1):
    slat, slon = pointlocs(relb)
    dlat, dlon = gr['lat'].data[slat], gr['lon'].data[slon]
    ilat = np.where(latgpi == dlat)
    ilon = np.where(longpi == dlon)
    igpi = np.intersect1d(ilat, ilon)[0]

    odir= '/project/amp/miyawaki/plots/p004/cmip6/%s/%s/%s/%s/%s/pct/%s' % (se,fo,md,varn,'regions', relb)
    if not os.path.exists(odir):
        os.makedirs(odir)

    print('Loading %s...'%varn1)
    vn1=load_data(md,fo,varn1,igpi,yr)
    print('Loading %s...'%varn2)
    vn2=load_data(md,fo,varn2,igpi,yr)
    print('Loading tas...')
    tas=load_data(md,fo,'tas',igpi,yr)

    print('Loading tas percentile')
    tdir = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,'tas')
    pvn=xr.open_dataarray('%s/p.%s_%s.%s.nc' % (tdir,'tas',yr,se)).sel(
            month = mo,
            gpi = igpi
            )
    bins = np.arange(len(pvn['percentile'])+1)

    # bin data
    btas = np.digitize(tas.data, pvn.data)

    with Client(n_workers=len(bins)):
        tasks=[dask.delayed(bcmon)(ibin,vn1,vn2, btas) for ibin in np.arange(len(bins))]
        l=dask.compute(*tasks)
        bc=[il[0] for il in l]
        csm=[il[1] for il in l]
        mtr=[il[2] for il in l]
        csm=np.stack(csm)
        mtr=np.stack(mtr)

    # colormap
    if fo == 'historical':
        colors = cm.Blues(np.linspace(0, 1, len(bins)-1))
    elif fo == 'ssp370':
        colors = cm.Oranges(np.linspace(0, 1, len(bins)-1))

    print('Plotting...')
    tname=r'%s' % (md)
    oname1=f'{odir}/{varn}_{yr}.{se}.{relb}.{mo}.pct.pbc'
    fig,ax=plt.subplots(figsize=(4,3),constrained_layout=True)
    if fo == 'historical':
        clf=ax.scatter(vn2,vn1,s=0.5,c=btas,cmap='Blues')
    elif fo == 'ssp370':
        clf=ax.scatter(vn2,vn1,s=0.5,c=btas,cmap='Oranges')
    [ax.plot(sbc[0], sbc[1], color=c) for sbc, c in zip(bc, colors)]
    ax.set_title(f'{tname} ({dlat:g}, {dlon:g})',fontsize=16)
    ax.set_xlabel('%s (%s)'%(varnlb(varn2),unitlb(varn2)))
    ax.set_ylabel('%s (%s)'%(varnlb(varn1),unitlb(varn1)))
    cb=fig.colorbar(clf,location='right')
    cb.set_ticks( (1/2*(bins[1:] + bins[:-1]))[::2] )
    cb.set_ticklabels(pvn['percentile'].data[::2])
    cb.set_label('Temperature percentile')
    fig.savefig('%s.png'%oname1, format='png', dpi=600)

if __name__=='__main__':
    for md in tqdm(lmd):
        for relb in lrelb:
            plot(relb,fo=fo1,yr=yr1)
