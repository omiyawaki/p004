import os
import sys
sys.path.append('../../data/')
sys.path.append('/home/miyawaki/scripts/common')
import pickle
import numpy as np
import xarray as xr
from concurrent.futures import ProcessPoolExecutor as Pool
import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import MultipleLocator
from scipy import ndimage
from scipy.stats import ttest_1samp as tt1
from sklearn.utils import resample
from tqdm import tqdm
from util import mods
from utils import monname,varnlb,unitlb
from mpl_toolkits.axes_grid1 import Divider,Size

nbs=int(1e2) # number of bootstrap resamples
# lre=['et','tr'] # tr=tropics, ml=midlatitudes, hl=high lat, et=extratropics
lre=['tr'] # tr=tropics, ml=midlatitudes, hl=high lat, et=extratropics
tlat=30 # latitude bound for tropics
plat=50 # midlatitude bound
alc=0.05 # significance level (that mmm is different from 0)
cval=0.4 # threshold DdT value for drawing contour line
npai=20 # number of bins for AI percentiles
dpai=100/npai
lpai=np.arange(0,100+dpai,dpai)
mppai=1/2*(lpai[1:]+lpai[:-1])
filt=False # only look at gridpoints with max exceeding value below
fmax=0.5
title=True
xlb=True
ylboverride=True
cboverride=True
titleoverride=True
fs=(3.5,3)
pds=(1,0.5)
axs=(1.5,2)
h=[Size.Fixed(pds[0]), Size.Fixed(axs[0])]
v=[Size.Fixed(pds[1]), Size.Fixed(axs[1])]

varn='tas'
varn1='mtr'
varnp='mtr'
reverse=True
se = 'sc' # season (ann, djf, mam, jja, son)
fo1='historical' # forcings 
fo2='ssp370' # forcings 
fo='%s-%s'%(fo2,fo1)
his='1980-2000'
# fut='2080-2100'
fut='gwl2.0'
skip507599=True

# lmd=mods(fo1)
# md='mmm'

lmd=['CESM2']
md='CESM2'

def vmax(vn):
    d={ 'hfls':         5,
        'hfss':         5,
        'gflx':         5,
        'fsm':          2.5,
        'snc':          0.05,
        'qvege':        5,
        'qvegt':        5,
        'qsoil':        5,
        'rsfc':         5,
        'swsfc':        5,
        'lwsfc':        5,
        'sfcWind':      0.1,
        'ooplh':        5,
        'ooplh_msm':    5,
        'ooplh_fixmsm': 5,
        'ooplh_fixasm': 5,
        'ooplh_fixbc':  5,
        'ooplh_rdbc':   5,
        'ooplh_dbc':   5,
        'ooplh_rnl':   5,
        'ooplh_rbcsm':  5,
        'ooplh_rddsm':  5,
        'ooplh_mtr':    5,
        'rfa':          10,
        'pblh':         100,
        'wap850':       1,
        'wapt850':      100,
        'fat850':       0.01,
        'advt850_wm2':  5,
        'advt850':      1,
        'advtsurf':     1,
        'advt850_t18':  0.03,
        'advtx850':     0.01,
        'advty850':     0.01,
        'advty850_18':  0.01,
        'advm850':      0.01,
        'advmx850':     0.01,
        'advmy850':     0.01,
        'tas':          1,
        'huss':         5e-4,
        'hurs':         3,
        'ta850':        1,
        'pr':           0.1,
        'mrsos':        1,
        'td_mrsos':     1,
        'ti_pr':        1,
        'ti_ev':        1,
        'ti_ro':        1,
        'ef':           0.05,
        'ef2':          0.05,
        'ef3':          0.05,
        'oosf':         0.05,
        'ooef':         0.05,
        'oopef':        0.05,
        'oopef_fixbc':  0.05,
        'oopef_fixmsm': 0.05,
        'oopef_rddsm':  0.05,
        'advt850_t':    1,
        'advt850_t18_t':1,
        'advty850_t18_t':1,
        'advt_rmean850_t':    1,
        'advt_doy850_t':    1,
        'adv5t_doy850_t':    1,
        'advty_doy850_t':    1,
        'advt_mon850_t':    1,
        'gflx_t':       1,
        'advt850_t_hs':    1,
        'gflx_t_hs':       1,
            }
    return d[vn]

def vstr(vn):
    d={ 'ooplh':        r'$BC_{all}$',
        'ooplh_fixbc':  r'$BC_{hist}$',
        'ooplh_rdbc':   r'$\Delta BC$',
        'ooplh_dbc':   r'$\Delta BC$',
        'ooplh_rnl':   r'Residual',
        'ooplh_rbcsm':  r'(a)$-$(b)$-$(c)',
        'ooplh_rddsm':  r'(b)$-$(c)',
        'ooplh_fixmsm': r'$BC_{hist}$, $\Delta\delta SM=0$',
        'ooplh_fixasm': r'$BC_{hist}$, $\Delta\delta SM=0$',
        'ooplh_mtr':    r'$\frac{\mathrm{d}LH}{\mathrm{d}SM}_{hist}\Delta SM$',
        'oopef':        r'$BC_{all}$',
        'oopef_fixbc':  r'$BC_{hist}$',
        'oopef_fixmsm': r'$BC_{hist}$, $\Delta\delta SM=0$',
        'oopef_rbcsm':  r'(a)$-$(b)$-$(c)',
        'oopef_rddsm':  r'(b)$-$(c)',
        'oopef_dbc':    r'$SM_{hist}$',
        'huss':         r'$q$',
        'qvege':        r'$LH_{vegE}$',
        'qvegt':        r'$LH_{vegT}$',
        'qsoil':        r'$LH_{soil}$',
        'hurs':         r'$RH$',
        'mrsos':        r'$SM$',
        'sfcWind':      r'$U_{10\,m}$',
        'td_mrsos':     r'$SM_{\mathrm{30\,d}}$',
        'ti_pr':        r'$P_{\mathrm{30\,d}}$',
        'ti_ev':        r'$-E_{\mathrm{30\,d}}$',
        'ti_ro':        r'$-R_{\mathrm{30\,d}}$',
        'pr':           r'$P$',
        'rfa':          r'$-\langle\nabla\cdotF_a\rangle$',
        'ta850':        r'$T_{850}$',
        'pblh':         r'$\mathrm{PBLH}$',
        'wap850':       r'$\omega_{850}$',
        'wapt850':      r'$(\omega T)_{850}$',
        'fa850':        r'$-\nabla\cdotF_{a,\,850}$',
        'fat850':       r'$-\nabla\cdot(vc_pT)_{850}$',
        'advt850_wm2':  r'$-\rho z_{850}(uc_p\partial_xT+vc_p\partial_yT)_{850}$',
        'advtsurf':      r'$-(uc_p\partial_xT+vc_p\partial_yT)_{}$',
        'advt850':      r'$-(uc_p\partial_xT+vc_p\partial_yT)_{850}$',
        'advt850_t18':  r'$-(uc_p\partial_xT+vc_p\partial_yT)_{850}$',
        'advtx850':     r'$-(uc_p\partial_xT)_{850}$',
        'advty850':     r'$-(vc_p\partial_yT)_{850}$',
        'advty850_t18': r'$-(vc_p\partial_yT)_{850}$',
        'advm850':      r'$-(u\partial_xm+v\partial_ym)_{850}$',
        'advmx850':     r'$-(u\partial_xm)_{850}$',
        'advmy850':     r'$-(v\partial_ym)_{850}$',
        'advt850_t':    r'$a(uc_p\partial_xT+vc_p\partial_yT)_{850}$',
        'advt850_t18_t':r'$a(uc_p\partial_xT+vc_p\partial_yT)_{850}$',
        'advty850_t18_t':r'$a(vc_p\partial_yT)_{850}$',
        'advt_doy850_t':    r'$a(uc_p\partial_x\overline{T}+vc_p\partial_y\overline{T})_{850}$',
        'adv5t_doy850_t':    r'$a(uc_p\partial_x\overline{T}+vc_p\partial_y\overline{T})_{850}$',
        'advty_doy850_t':    r'$a(vc_p\partial_y\overline{T})_{850}$',
        'advt_mon850_t':    r'$a(uc_p\partial_x\overline{T}+vc_p\partial_y\overline{T})_{850}$',
        'advt_rmean850_t':    r'$a(uc_p\partial_x\overline{T}+vc_p\partial_y\overline{T})_{850}$',
        'mtr':    r'Transition regime slope',
            }
    return d[vn]

def plot(re):
    if ylboverride:
        ylb=True
    else:
        ylb=True if re=='tr' else False
    if cboverride:
        showcb=True
    else:
        showcb=True if re=='hl' else False
    # plot strings
    if titleoverride:
        tstr='$%s$'%varnlb(varn1)
    else:
        if 'ooplh' in varn1 or 'oopef' in varn1:
            tstr=vstr(varn1)
        elif 'mrsos' in varn1 or 'pr' in varn1:
            tstr=vstr(varn1)
        else:
            if re=='tr':
                tstr='Tropics'
            elif re=='ml':
                tstr='Midlatitudes'
            elif re=='hl':
                tstr='High latitudes'
            elif re=='et':
                tstr='Extratropics'
    fstr='.filt' if filt else ''

    # load land indices
    lmi,_=pickle.load(open('/project/amp/miyawaki/data/share/lomask/cesm2/lomi.pickle','rb'))

    # grid
    rgdir='/project/amp/miyawaki/data/share/regrid'
    # open CESM data to get output grid
    cfil='%s/f.e11.F1850C5CNTVSST.f09_f09.002.cam.h0.PHIS.040101-050012.nc'%rgdir
    cdat=xr.open_dataset(cfil)
    gr=xr.Dataset({'lat': (['lat'], cdat['lat'].data)}, {'lon': (['lon'], cdat['lon'].data)})

    def remap(v,gr):
        llv=np.nan*np.ones([v.shape[0],gr['lat'].size*gr['lon'].size])
        llv[...,lmi]=v.data
        llv=np.reshape(llv,(v.shape[0],gr['lat'].size,gr['lon'].size))
        return llv

    def eremap(v,gr):
        llv=np.nan*np.ones([v.shape[0],v.shape[1],gr['lat'].size*gr['lon'].size])
        llv[...,lmi]=v.data
        llv=np.reshape(llv,(v.shape[0],v.shape[1],gr['lat'].size,gr['lon'].size))
        return llv

    def regsl(v,ma):
        v=v*ma
        v=np.reshape(v,[v.shape[0],v.shape[1]*v.shape[2]])
        kidx=~np.isnan(v).any(axis=(0))
        return v[...,kidx],kidx

    def regsla(v,gr,ma):
        sv=np.roll(v,6,axis=0) # seasonality shifted by 6 months
        v[:,gr['lat']<0,:]=sv[:,gr['lat']<0,:]
        return regsl(v,ma)

    def eregsl(v,ma,kidx):
        v=v*np.moveaxis(ma[...,None],-1,0)
        v=np.reshape(v,[v.shape[0],v.shape[1],v.shape[2]*v.shape[3]])
        return v[...,kidx]

    def eregsla(v,gr,ma,kidx):
        sv=np.roll(v,6,axis=1) # seasonality shifted by 6 months
        v[:,:,gr['lat']<0,:]=sv[:,:,gr['lat']<0,:]
        return eregsl(v,ma,kidx)

    def regsl2d(v,ma,kidx):
        v=v*ma
        v=np.reshape(v,[v.shape[0]*v.shape[1]])
        return v[kidx]

    def sortai(v):
        idx=np.argsort(v)
        return v[idx],idx

    def load_vn(varn,fo,byr,px='m'):
        if '_wm2' in varn: varn=varn.replace('_wm2','')
        idir = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,varn)
        return xr.open_dataarray('%s/%s.%s_%s.%s.nc' % (idir,px,varn,byr,se))

    def load_mmm(varn,varnp):
        if '_wm2' in varn: varn=varn.replace('_wm2','')
        if '_wm2' in varnp: varnp=varnp.replace('_wm2','')
        idir = '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,varn)
        return xr.open_dataarray('%s/d.%s_%s_%s.%s.nc' % (idir,varn,his,fut,se))

    dvn1=load_mmm(varn1,varnp)
    if reverse and (varn1 in ['qvege', 'qvegt', 'qsoil', 'ti_ev','gflx','fsm','hfss','hfls','fa850','fat850','advt850_wm2','advt850','advtx850','advty850','advm850','advmx850','advmy850','rfa'] or 'ooplh' in varn1):
        dvn1=-dvn1
    if 'wap' in varn1: dvn1=dvn1*86400/100 # convert from Pa/s to hPa/d
    if varn1=='pr': dvn1=86400*dvn1
    if '_wm2' in varn1: dvn1=1.16*1500*dvn1 # rho*z850
    if 'advt' in varn1: dvn1=86400*dvn1

    # variable of interest
    odir1 = '/project/amp/miyawaki/plots/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,varn1)
    if not os.path.exists(odir1):
        os.makedirs(odir1)

    def load_vn(varn,idir0):
        if '_wm2' in varn: varn=varn.replace('_wm2','')
        dvne=xr.open_dataarray('%s/d.%s_%s_%s.%s.nc' % (idir0,varn,his,fut,se))
        if varn=='pr': dvne=86400*dvne
        if '_wm2' in varn: dvne=1.16*1500*dvne # rho*z850
        return dvne

    # load data for each model
    def load_idir(varn,md):
        if '_wm2' in varn: varn=varn.replace('_wm2','')
        return '/project/amp02/miyawaki/data/p004/cmip6/%s/%s/%s/%s' % (se,fo,md,varn)
    idirs=[load_idir(varn1,md0) for md0 in lmd]
    dvne=[load_vn(varn1,idir0) for idir0 in tqdm(idirs)]
    dvne=xr.concat(dvne,'model')

    # remap to lat x lon
    dvn1=remap(dvn1,gr)
    dvne=eremap(dvne,gr)

    # mask greenland and antarctica
    aagl=pickle.load(open('/project/amp/miyawaki/data/share/aa_gl/cesm2/aa_gl.pickle','rb'))
    dvn1=dvn1*aagl
    dvne=dvne*aagl

    [mlat,mlon] = np.meshgrid(gr['lat'], gr['lon'], indexing='ij')
    awgt=np.cos(np.deg2rad(mlat)) # area weight

    # make sure nans are consistent
    nidx=np.isnan(dvn1)
    for imd in range(dvne.shape[0]):
        nidx=np.logical_or(np.isnan(nidx),np.isnan(dvne[imd,...]))
    dvn1[nidx]=np.nan
    dvne[:,nidx]=np.nan

    ah=np.ones_like(mlat)
    if re=='tr':
        ah[np.abs(gr['lat'])>tlat]=np.nan
    elif re=='ml':
        ah[np.logical_or(np.abs(gr['lat'])<=tlat,np.abs(gr['lat'])>plat)]=np.nan
    elif re=='hl':
        ah[np.abs(gr['lat'])<=plat]=np.nan
    elif re=='et':
        ah[np.abs(gr['lat'])<=tlat]=np.nan

    # select region
    ahd1,kidx=regsla(dvn1,gr,ah)
    ahde=eregsla(dvne,gr,ah,kidx)
    # weights
    ahw=regsl2d(awgt,ah,kidx)

    # area weighted mean
    ahdg=ahd1.copy()
    ahd1=np.sum(ahw*ahd1,axis=-1)/np.sum(ahw)
    ahde=np.sum(ahw*ahde,axis=-1)/np.sum(ahw)

    mon=range(12)

    # plot gp vs seasonal cycle of varn1 PCOLORMESH
    fig=plt.figure(figsize=fs)
    divider=Divider(fig, (0, 0, 1, 1), h, v, aspect=False)
    ax=fig.add_axes(divider.get_position(),axes_locator=divider.new_locator(nx=1, ny=1))
    clf=ax.plot(mon,ahd1)
    ax.text(0.5,1.05,tstr,ha='center',va='center',transform=ax.transAxes)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.set_xticks(np.arange(1,11+2,2))
    ax.set_xticklabels(np.arange(2,12+2,2))
    # ax.set_yticks(100*np.arange(0,1+0.2,0.2))
    # ax.set_xticklabels(np.arange(2,12+2,2))
    ax.set_xlim([-0.5,11.5])
    fig.savefig('%s/sc.%s.%s%s.ah.noperc.%s.png' % (odir1,varn1,fo,fstr,re), format='png', dpi=600,backend='pgf')
    fig.savefig('%s/sc.%s.%s%s.ah.noperc.%s.pdf' % (odir1,varn1,fo,fstr,re), format='pdf', dpi=600,backend='pgf')

[plot(re) for re in tqdm(lre)]

# if __name__=='__main__':
#     with Pool(max_workers=len(lre)) as p:
#         p.map(plot,lre)
