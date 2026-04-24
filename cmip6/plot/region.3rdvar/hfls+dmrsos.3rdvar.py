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

# relb='fourcorners'
# re=['Utah','Colorado','Arizona','New Mexico']

lrelb=['swus']

varn1='hfls'
varn2='mrsos'
varn3='qsoil'
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

def plot(relb,fo=fo1,yr=yr1):
    slat, slon = pointlocs(relb)
    dlat, dlon = gr['lat'].data[slat], gr['lon'].data[slon]
    ilat = np.where(latgpi == dlat)
    ilon = np.where(longpi == dlon)
    igpi = np.intersect1d(ilat, ilon)[0]

    odir= f'/project/amp/miyawaki/plots/p004/cmip6/{se}/{fo}/{md}/{varn}/regions/{varn3}/{relb}'
    if not os.path.exists(odir):
        os.makedirs(odir)

    print('Loading %s...'%varn1)
    vn1=load_data(md,fo,varn1,igpi,yr)
    print('Loading %s...'%varn2)
    vn2=load_data(md,fo,varn2,igpi,yr)
    print('Loading %s...'%varn3)
    vn3=load_data(md,fo,varn3,igpi,yr)

    if varn3=='vpd':
        vn3 = vn3/100

    # calculate for colormap
    median = np.median(vn3)
    std = np.std(vn3)

    print('Plotting...')
    tname=r'%s' % (md)
    oname1=f'{odir}/{varn}_{yr}.{se}.{relb}.{mo}.{varn3}'
    fig,ax=plt.subplots(figsize=(4,3),constrained_layout=True)
    clf=ax.scatter(vn2,vn1,s=4,c=vn3,cmap='RdBu_r', vmin=median-2*std, vmax=median+2*std)
    ax.set_title(f'{tname} ({dlat:g}, {dlon:g})',fontsize=16)
    ax.set_xlabel('%s (%s)'%(varnlb(varn2),unitlb(varn2)))
    ax.set_ylabel('%s (%s)'%(varnlb(varn1),unitlb(varn1)))
    cb=fig.colorbar(clf,location='right')
    # cb.set_ticks( set(np.round(vn1['time.year'].data/10)*10) )
    cb.set_label(f'${varnlb(varn3)}$ ({unitlb(varn3)})')
    fig.savefig('%s.png'%oname1, format='png', dpi=600)

for md in tqdm(lmd):
    for relb in lrelb:
        plot(relb,fo=fo1,yr=yr1)
