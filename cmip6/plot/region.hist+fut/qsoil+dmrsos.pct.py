import os
import sys
sys.path.append('../../data/')
sys.path.append('/home/miyawaki/scripts/common')
import dask
from dask.diagnostics import ProgressBar
import dask.multiprocessing
import pickle
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.stats import gaussian_kde
from tqdm import tqdm
from util import mods
from utils import corr,corr2d,monname,varnlb,unitlb
from regions import pointlocs
from CASutils import shapefile_utils as shp
from etregimes import bestfit

# relb='fourcorners'
# re=['Utah','Colorado','Arizona','New Mexico']

lrelb=['swus']

varn1='qvegt'
varn2='mrso40'
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
    mvn = vn.sel(gpi=igpi).mean('time')
    vn=vn.sel(time=vn['time.month']==mo, gpi=igpi)
    return vn, mvn

def bcmon(svn1, svn2):
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

def proc_data(sfo, syr, igpi):
    print('Loading %s...'%varn1)
    vn1, _=load_data(md,sfo,varn1,igpi,syr)
    print('Loading %s...'%varn2)
    vn2, mvn2 =load_data(md,sfo,varn2,igpi,syr)
    print('Loading tas...')
    tas, _=load_data(md,sfo,'tas',igpi,syr)

    if varn2 == 'pr':
        vn2 = 86400 * vn2

    print('Loading tas percentile')
    tdir = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,sfo,md,'tas')
    pvn=xr.open_dataarray('%s/p.%s_%s.%s.nc' % (tdir,'tas',syr,se)).sel(
            month = mo,
            gpi = igpi
            )

    # bin data
    btas = np.digitize(tas.data, pvn.data)
    return vn1, vn2, btas, pvn, mvn2

def plot(relb):
    slat, slon = pointlocs(relb)
    dlat, dlon = gr['lat'].data[slat], gr['lon'].data[slon]
    ilat = np.where(latgpi == dlat)
    ilon = np.where(longpi == dlon)
    igpi = np.intersect1d(ilat, ilon)[0]

    odir= '/project/amp/miyawaki/plots/p004/cmip6/%s/%s/%s/%s/%s/pct/%s' % (se,fo,md,varn,'regions', relb)
    if not os.path.exists(odir):
        os.makedirs(odir)

    # load data
    vn1h, vn2h, btash, pvn, mvn2h = proc_data(fo1, yr1, igpi)
    vn1f, vn2f, btasf, _  , mvn2f = proc_data(fo2, yr2, igpi)

    # compute hot
    vn1h975 = vn1h.where(btash == len(pvn)).mean()
    vn2h975 = vn2h.where(btash == len(pvn)).mean()
    vn1f975 = vn1f.where(btasf == len(pvn)).mean()
    vn2f975 = vn2f.where(btasf == len(pvn)).mean()

    # compute median 
    vn1h500 = 1/2 * ( vn1h.where(btash == np.floor(len(pvn)/2)).mean() + vn1h.where(btash == np.floor(len(pvn)/2)).mean() )
    vn2h500 = 1/2 * ( vn2h.where(btash == np.floor(len(pvn)/2)).mean() + vn2h.where(btash == np.floor(len(pvn)/2)).mean() )
    vn1f500 = 1/2 * ( vn1f.where(btasf == np.floor(len(pvn)/2)).mean() + vn1f.where(btasf == np.floor(len(pvn)/2)).mean() )
    vn2f500 = 1/2 * ( vn2f.where(btasf == np.floor(len(pvn)/2)).mean() + vn2f.where(btasf == np.floor(len(pvn)/2)).mean() )

    # compute bc
    bch, csmh, mtrh = bcmon(vn1h, vn2h)
    bcf, csmf, mtrf = bcmon(vn1f, vn2f)

    print('Plotting...')
    tname=r'%s' % (md)
    oname1=f'{odir}/{varn}_{yr1}+{yr2}.{se}.{relb}.{mo}.pct'
    fig,ax=plt.subplots(figsize=(4,3),constrained_layout=True)
    clf=ax.scatter(vn2h,vn1h,s=0.5,c='tab:blue', label=fo1)
    ax.scatter(vn2f,vn1f,s=0.5,c='tab:orange', label=fo2)
    # ax.plot(bch[0], bch[1], color='tab:blue')
    # ax.plot(bcf[0], bcf[1], color='tab:orange')
    # ax.plot(vn2h975, vn1h975, marker='^', markersize=10, markerfacecolor='tab:blue', markeredgewidth=2, markeredgecolor='white', linestyle='None', label='> 95th')
    # ax.plot(vn2h500, vn1h500, marker='o', markersize=10, markerfacecolor='tab:blue', markeredgewidth=2, markeredgecolor='white', linestyle='None', label='Median')
    # ax.plot(vn2f975, vn1f975, marker='^', markersize=10, markerfacecolor='tab:orange', markeredgewidth=2, markeredgecolor='white')
    # ax.plot(vn2f500, vn1f500, marker='o', markersize=10, markerfacecolor='tab:orange', markeredgewidth=2, markeredgecolor='white')
    ax.set_title(f'{tname} ({dlat:g}, {dlon:g})',fontsize=16)
    ax.set_xlabel('$%s$ (%s)'%(varnlb(varn2),unitlb(varn2)))
    ax.set_ylabel('$%s$ (%s)'%(varnlb(varn1),unitlb(varn1)))
    # cb=fig.colorbar(clf,location='right')
    # bins = np.arange(len(pvn['percentile'])+1)
    # cb.set_ticks( (1/2*(bins[1:] + bins[:-1]))[::2] )
    # cb.set_ticklabels(pvn['percentile'].data[::2])
    ax.legend(frameon=False)
    # ax.set_ylim([-5,55])
    fig.savefig('%s.png'%oname1, format='png', dpi=600)

for md in tqdm(lmd):
    for relb in lrelb:
        plot(relb)
