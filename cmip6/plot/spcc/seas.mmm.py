import os
import sys
sys.path.append('../../data/')
sys.path.append('/home/miyawaki/scripts/common')
import pickle
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LatitudeFormatter
from scipy.stats import linregress
from tqdm import tqdm
from util import mods
from utils import monname,varnlb,unitlb
import colormaps as cmaps

s='min'
seas='djf'
# lvn=['tas']
# vnp= 'tas'
# lvn=['ta_advtsurf']
# vnp= 'ta_advtsurf'
lvn=['advt850.ctas.d3']
vnp= 'advt850.ctas.d3'
# lvn=['advtsurf.ctas.d3']
# vnp= 'advtsurf.ctas.d3'
domp=True
nhmon=[12,1,2]
shmon=[6,7,8]
tlat=30 # upper bound for low latitude
plat=30 # lower bound for high latitude
nhhl=True
tropics=False
reverse=True
# lvn=['ooplh','ooplh_fixbc','ooplh_fixmsm','ooplh_rddsm']
# vnp='ooplh'
se = 'sc' # season (ann, djf, mam, jja, son)

mgen='cmip6'
fo1='historical' # forcings 
fo2='ssp370' # forcings 
his='1950-1980'
fut='2070-2100'

# mgen='cmip5'
# fo1='historical' # forcings 
# fo2='rcp85' # forcings 
# his='1950-1980'
# fut='2070-2100'

fo='%s-%s'%(fo2,fo1)
dpi=600
skip507599=True

md='mmm'

# load land indices
lmi,_=pickle.load(open('/project/amp/miyawaki/data/share/lomask/cesm2/lomi.pickle','rb'))

# grid
rgdir='/project/amp/miyawaki/data/share/regrid'
# open CESM data to get output grid
cfil='%s/f.e11.F1850C5CNTVSST.f09_f09.002.cam.h0.PHIS.040101-050012.nc'%rgdir
cdat=xr.open_dataset(cfil)
gr=xr.Dataset({'lat': (['lat'], cdat['lat'].data)}, {'lon': (['lon'], cdat['lon'].data)})

def cmap(vn):
    vbr=['td_mrsos','ti_pr','ti_ev']
    if vn in vbr:
        return 'BrBG'
    else:
        return cmaps.cmp_b2r

def vmaxdd(vn):
    lvm={   
            'tas':  [6,1],
            'ta850':  [6,1],
            'snc':  [0.4,0.04],
            'advt850_t':  [6,1],
            'advty_mon850_t':  [6,1],
            'advty_mon850_t_hs':  [6,1],
            'advt850_t18_t':  [6,1],
            'advty850_t18_t':  [6,1],
            'advt850_t_hs':  [6,1],
            'ta850':  [6,1],
            'twas': [6,1],
            'hurs': [5,0.5],
            'ef':  [0.05,0.005],
            'ef2':  [0.05,0.005],
            'ef3':  [0.05,0.005],
            'mrsos': [6,1],
            'sfcWind': [0.5,0.005],
            'rsfc': [10,1],
            'swsfc': [10,1],
            'lwsfc': [10,1],
            'hfls': [10,1],
            'hfss': [10,1],
            'gflx': [10,1],
            'fsm': [10,1],
            'plh': [10,1],
            'plh_fixbc': [10,1],
            'ooef': [0.05,0.005],
            'ooef2': [0.05,0.005],
            'ooef3': [0.05,0.005],
            'oopef': [0.05,0.005],
            'oopef2': [0.05,0.005],
            'oopef3': [0.05,0.005],
            'oopef_fixbc': [0.05,0.005],
            'oopef3_fixbc': [0.05,0.005],
            'ooplh': [10,1],
            'ooplh_msm': [10,1],
            'ooplh_fixmsm': [10,1],
            'ooplh_orig': [10,1],
            'ooplh_fixbc': [10,1],
            'ooplh_rddsm': [10,1],
            'td_mrsos': [2,0.1],
            'ti_pr': [5,0.5],
            'fa850': [0.3,0.03],
            'fat850': [0.3,0.03],
            'advt850_wm2': [50,5],
            'advt850': [2.0,0.5],
            'advtsurf': [2.0,0.5],
            'ta_advtsurf': [2.0,0.5],
            'advtsurf.ctas.d3': [2.0,0.5],
            'advt850.ctas.d3': [2.0,0.5],
            'advt_doy850': [2.0,0.5],
            'advt_mon850': [2.0,0.5],
            'advt_mon925': [2.0,0.5],
            'advty_doy850': [2.0,0.5],
            'advty_mon850': [2.0,0.5],
            'advty_mon925': [2.0,0.5],
            'advt850_t18': [2.0,0.5],
            'advtx850': [0.03,0.003],
            'advtx850_t18': [0.03,0.003],
            'advty850': [2.0,0.5],
            'advm850': [2.0,0.5],
            'advmx850': [0.03,0.003],
            'advmy850': [2.0,0.5],
            }
    return lvm[vn]

def vmaxd(vn):
    lvm={   
            'tas':  [6,1],
            'ta850':  [6,1],
            'snc':  [0.4,0.04],
            'advt850_t':  [6,1],
            'advty_mon850_t':  [6,1],
            'advty_mon850_t_hs':  [6,1],
            'advt850_t18_t':  [6,1],
            'advty850_t18_t':  [6,1],
            'advt850_t_hs':  [6,1],
            'ta850':  [6,1],
            'twas': [6,1],
            'hurs': [5,0.5],
            'ef':  [0.05,0.005],
            'ef2':  [0.05,0.005],
            'ef3':  [0.05,0.005],
            'mrsos': [6,1],
            'sfcWind': [0.5,0.005],
            'rsfc': [10,1],
            'swsfc': [10,1],
            'lwsfc': [10,1],
            'hfls': [10,1],
            'hfss': [10,1],
            'gflx': [10,1],
            'fsm': [10,1],
            'plh': [10,1],
            'plh_fixbc': [10,1],
            'ooef': [0.05,0.005],
            'ooef2': [0.05,0.005],
            'ooef3': [0.05,0.005],
            'oopef': [0.05,0.005],
            'oopef2': [0.05,0.005],
            'oopef3': [0.05,0.005],
            'oopef_fixbc': [0.05,0.005],
            'oopef3_fixbc': [0.05,0.005],
            'ooplh': [10,1],
            'ooplh_msm': [10,1],
            'ooplh_fixmsm': [10,1],
            'ooplh_orig': [10,1],
            'ooplh_fixbc': [10,1],
            'ooplh_rddsm': [10,1],
            'td_mrsos': [2,0.1],
            'ti_pr': [5,0.5],
            'fa850': [0.3,0.03],
            'fat850': [0.3,0.03],
            'advt850_wm2': [50,5],
            'advt850': [2.0,0.5],
            'advtsurf': [2.0,0.5],
            'advtsurf.ctas.d3': [2.0,0.5],
            'advt850.ctas.d3': [2.0,0.5],
            'ta_advtsurf': [2.0,0.5],
            'advt_doy850': [2.0,0.5],
            'advt_mon850': [2.0,0.5],
            'advt_mon925': [2.0,0.5],
            'advty_doy850': [2.0,0.5],
            'advty_mon850': [2.0,0.5],
            'advty_mon925': [2.0,0.5],
            'advt850_t18': [2.0,0.5],
            'advtx850': [0.03,0.003],
            'advtx850_t18': [0.03,0.003],
            'advty850': [2.0,0.5],
            'advm850': [2.0,0.5],
            'advmx850': [0.03,0.003],
            'advmy850': [2.0,0.5],
            }
    return lvm[vn]

def plot(vn):
    vmdd,dvmdd=vmaxdd(vn)
    vmd,dvmd=vmaxd(vn)
    vnlb=varnlb(vn)
    unlb=unitlb(vn)
    # if 'advt' in vn:
    #     unlb='C s$^{-1}$'
    odir = '/project/amp/miyawaki/plots/p004/%s/%s/%s/%s/%s' % (mgen,se,fo,md,vn)

    vno=vn
    if '_wm2' in vn:
        vn=vn.replace('_wm2','')

    idir = '/project/amp02/miyawaki/data/p004/%s/%s/%s/%s/%s' % (mgen,se,fo,md,vn)

    if not os.path.exists(odir):
        os.makedirs(odir)

    # warming
    def loadvar(px):
        xvn=xr.open_dataarray('%s/%s.avg.%s_%s_%s.%s.nc' % (idir,px,vn,his,fut,se))
        xvn=xvn.sel(season=seas).squeeze()
        if 'pc' in px:
            stat=xvn['stat']
            xvn=xvn.sel(stat=stat==s).squeeze()
        if reverse and (vn in ['fsm','gflx','hfss','hfls','fat850','fa850','rfa'] or 'ooplh' in vn or 'adv' in vn) and '_t' not in vn:
            xvn=-xvn
        if '_wm2' in vno:
            xvn=1.16*1500*xvn
        if 'advt' in vn:
            xvn=86400*xvn
        return xvn

    if domp:
        dmvn=loadvar('d')
        dpvn=loadvar('dpc')
    ddpvn=loadvar('ddpc')
    gpi=ddpvn['gpi']

    # remap to lat x lon
    def remap(xvn):
        llxvn=np.nan*np.ones([gr['lat'].size*gr['lon'].size])
        llxvn[lmi]=xvn.data
        llxvn=np.reshape(llxvn,(gr['lat'].size,gr['lon'].size))
        return llxvn

    if domp:
        lldmvn=remap(dmvn)
        lldpvn=remap(dpvn)
    llddpvn=remap(ddpvn)

    # repeat 0 deg lon info to 360 deg to prevent a blank line in contour
    gr['lon'] = np.append(gr['lon'].data,360)
    def replon(xvn):
        xvn = np.append(xvn, xvn[...,0][...,None],axis=1)
        return xvn

    if domp:
        lldmvn=replon(lldmvn)
        lldpvn=replon(lldpvn)
    llddpvn=replon(llddpvn)

    [mlat,mlon] = np.meshgrid(gr['lat'], gr['lon'], indexing='ij')

    if nhhl:
        if domp:
            # plot NH HL ONLY
            fig,ax=plt.subplots(subplot_kw={'projection': ccrs.PlateCarree(central_longitude=0)},figsize=(5,4),constrained_layout=True)
            ax.set_title(r'%s %s %s' % (md.upper(),fo.upper(),seas.upper()),fontsize=16)
            clf=ax.contourf(mlon, mlat, lldmvn, np.arange(-vmd,vmd+dvmd,dvmd),extend='both', vmax=vmd, vmin=-vmd, transform=ccrs.PlateCarree(),cmap=cmap(vn),transform_first=True)
            ax.coastlines()
            ax.set_extent((-180,180,plat,90),crs=ccrs.PlateCarree())
            gl=ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linewidth=0.5,color='gray',y_inline=False)
            gl.ylocator=mticker.FixedLocator([])
            gl.yformatter=LatitudeFormatter()
            gl.xlines=False
            gl.left_labels=False
            gl.bottom_labels=False
            gl.right_labels=True
            gl.top_labels=False
            cb=fig.colorbar(clf,location='bottom',aspect=50)
            cb.ax.tick_params(labelsize=12)
            cb.set_label(label=r'$\Delta \overline{%s}$ (%s)'%(vnlb,unlb),size=16)
            fig.savefig('%s/%s.d%s%s.%s.%s.hl.png' % (odir,seas,'avg',vn,fo,fut), format='png', dpi=dpi)

            # plot NH HL ONLY
            fig,ax=plt.subplots(subplot_kw={'projection': ccrs.PlateCarree(central_longitude=0)},figsize=(5,4),constrained_layout=True)
            ax.set_title(r'%s %s %s' % (md.upper(),fo.upper(),seas.upper()),fontsize=16)
            clf=ax.contourf(mlon, mlat, lldpvn, np.arange(-vmd,vmd+dvmd,dvmd),extend='both', vmax=vmd, vmin=-vmd, transform=ccrs.PlateCarree(),cmap=cmap(vn),transform_first=True)
            ax.coastlines()
            ax.set_extent((-180,180,plat,90),crs=ccrs.PlateCarree())
            gl=ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linewidth=0.5,color='gray',y_inline=False)
            gl.ylocator=mticker.FixedLocator([])
            gl.yformatter=LatitudeFormatter()
            gl.xlines=False
            gl.left_labels=False
            gl.bottom_labels=False
            gl.right_labels=True
            gl.top_labels=False
            cb=fig.colorbar(clf,location='bottom',aspect=50)
            cb.ax.tick_params(labelsize=12)
            # cb.set_label(label=r'$\Delta %s^{%s}$ (%s)'%(vnlb,s,unlb),size=16)
            fig.savefig('%s/%s.dp%s%s.%s.%s.hl.png' % (odir,seas,s,vn,fo,fut), format='png', dpi=dpi)

        # plot NH HL ONLY
        fig,ax=plt.subplots(subplot_kw={'projection': ccrs.Robinson(central_longitude=240)},figsize=(5,4),constrained_layout=True)
        ax.set_title(r'%s %s %s' % (md.upper(),fo.upper(),seas.upper()),fontsize=16)
        clf=ax.contourf(mlon, mlat, llddpvn, np.arange(-vmdd,vmdd+dvmdd,dvmdd),extend='both', vmax=vmdd, vmin=-vmdd, transform=ccrs.PlateCarree(),cmap=cmap(vn),transform_first=True)
        ax.coastlines()
        ax.set_extent((-180,180,plat,90),crs=ccrs.PlateCarree())
        gl=ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linewidth=0.5,color='gray',y_inline=False)
        gl.ylocator=mticker.FixedLocator([])
        gl.yformatter=LatitudeFormatter()
        gl.xlines=False
        gl.left_labels=False
        gl.bottom_labels=False
        gl.right_labels=True
        gl.top_labels=False
        cb=fig.colorbar(clf,location='bottom',aspect=50)
        cb.ax.tick_params(labelsize=12)
        cb.set_label(label=r'$\Delta \delta %s$ (%s)'%(vnlb,unlb),size=16)
        fig.savefig('%s/%s.ddp%s%s.%s.%s.hl.png' % (odir,seas,s,vn,fo,fut), format='png', dpi=dpi)

        # plot NH HL ONLY
        fig,ax=plt.subplots(subplot_kw={'projection': ccrs.PlateCarree(central_longitude=0)},figsize=(5,4),constrained_layout=True)
        # ax.set_title(r'%s %s' % (md.upper(),fo.upper()),fontsize=16)
        ax.set_title(r'%s %s %s' % (md.upper(),fo.upper(),seas.upper()),fontsize=16)
        clf=ax.contourf(mlon, mlat, llddpvn, np.arange(-vmdd,vmdd+dvmdd,dvmdd),extend='both', vmax=vmdd, vmin=-vmdd, transform=ccrs.PlateCarree(),cmap=cmap(vn),transform_first=True)
        ax.coastlines()
        ax.set_extent((-180,180,plat,90),crs=ccrs.PlateCarree())
        gl=ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linewidth=0.5,color='gray',y_inline=False)
        gl.ylocator=mticker.FixedLocator([])
        gl.yformatter=LatitudeFormatter()
        gl.xlines=False
        gl.left_labels=False
        gl.bottom_labels=False
        gl.right_labels=True
        gl.top_labels=False
        cb=fig.colorbar(clf,location='bottom',aspect=50)
        cb.ax.tick_params(labelsize=12)
        cb.set_label(label=r'$\Delta \delta %s$ (%s)'%(vnlb,unlb),size=16)
        fig.savefig('%s/%s.ddp%s%s.%s.%s.hl.lon0.png' % (odir,seas,s,vn,fo,fut), format='png', dpi=dpi)


    # plot TROPICS ONLY
    if tropics:
        fig,ax=plt.subplots(subplot_kw={'projection': ccrs.Robinson(central_longitude=240)},figsize=(5,4),constrained_layout=True)
        # ax.set_title(r'%s %s' % (md.upper(),fo.upper()),fontsize=16)
        ax.set_title(r'%s %s %s' % (md.upper(),fo.upper(),seas.upper()),fontsize=16)
        clf=ax.contourf(mlon, mlat, llddpvn, np.arange(-vmdd,vmdd+dvmdd,dvmdd),extend='both', vmax=vmdd, vmin=-vmdd, transform=ccrs.PlateCarree(),cmap=cmap(vn))
        ax.coastlines()
        ax.set_extent((-180,180,-tlat,tlat),crs=ccrs.PlateCarree())
        gl=ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linewidth=0.5,color='gray',y_inline=False)
        gl.ylocator=mticker.FixedLocator([-50,-30,0,30,50])
        gl.yformatter=LatitudeFormatter()
        gl.xlines=False
        gl.left_labels=False
        gl.bottom_labels=False
        gl.right_labels=True
        gl.top_labels=False
        cb=fig.colorbar(clf,location='bottom',aspect=50)
        cb.ax.tick_params(labelsize=12)
        cb.set_label(label=r'$\Delta \delta %s$ (%s)'%(vnlb,unlb),size=16)
        fig.savefig('%s/%s.ddp%s%s.%s.%s.tr.png' % (odir,seas,s,vn,fo,fut), format='png', dpi=dpi)

    # plot pct warming - mean warming
    fig,ax=plt.subplots(subplot_kw={'projection': ccrs.Robinson(central_longitude=240)},figsize=(5,4),constrained_layout=True)
    clf=ax.contourf(mlon, mlat, llddpvn, np.arange(-vmdd,vmdd+dvmdd,dvmdd),extend='both', vmax=vmdd, vmin=-vmdd, transform=ccrs.PlateCarree(), cmap=cmap(vn))
    ax.coastlines()
    ax.set_title(r'%s %s %s' % (md.upper(),fo.upper(),seas.upper()),fontsize=16)
    cb=fig.colorbar(clf,location='bottom',aspect=50)
    cb.ax.tick_params(labelsize=16)
    cb.set_label(label=r'$\Delta \delta %s$ (%s)'%(vnlb,unlb),size=16)
    fig.savefig('%s/%s.ddp%s%s.%s.%s.png' % (odir,seas,s,vn,fo,fut), format='png', dpi=dpi)

# run
[plot(vn) for vn in lvn]
