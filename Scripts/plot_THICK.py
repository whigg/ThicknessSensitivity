"""
Plot thickness profile difference between HIT and FIT experiments. 
These are sea ice thickness perturbation experiments using WACCM4.

Notes
-----
    Author : Zachary Labe
    Date   : 14 August 2017
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import nclcmaps as ncm
import datetime
import read_MonthlyOutput as MO
import calc_Utilities as UT

### Define directories
directorydata = '/surtsey/zlabe/simu/'
directoryfigure = '/home/zlabe/Desktop/'
#directoryfigure = '/home/zlabe/Documents/Research/SITperturb/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting temperature - %s----' % titletime)

### Alott time series
year1 = 1900
year2 = 2000
years = np.arange(year1,year2+1,1)

### Call function for vertical thickness data
lat,lon,time,lev,thickh = MO.readExperi(directorydata,'THICK','HIT',
                                        'surface')
lat,lon,time,lev,thickf = MO.readExperi(directorydata,'THICK','FIT',
                                        'surface')

### Separate per periods (ON,DJ,FM)
thickh_on = np.nanmean(thickh[:,9:10,:,:],axis=1)
thickf_on = np.nanmean(thickf[:,9:10,:,:],axis=1)

thickh_dj,thickf_dj = UT.calcDecJan(thickh,thickf,lat,lon,
                                    'surface',1)

thickh_fm = np.nanmean(thickh[:,1:2,:,:],axis=1)
thickf_fm = np.nanmean(thickf[:,1:2,:,:],axis=1)

#### Calculate period differenceds
diff_on = np.nanmean((thickf_on-thickh_on),axis=0)
diff_dj = np.nanmean((thickf_dj-thickh_dj),axis=0)
diff_fm = np.nanmean((thickf_fm-thickh_fm),axis=0)

#### Calculate significance
stat_on,pvalue_on = UT.calc_indttest(thickh_on,thickf_on)
stat_dj,pvalue_dj = UT.calc_indttest(thickh_dj,thickf_dj)
stat_fm,pvalue_fm = UT.calc_indttest(thickh_fm,thickf_fm)

###########################################################################
###########################################################################
###########################################################################
### Plot surface temperature
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

### Set limits for contours and colorbars
limit = np.arange(-30,30.1,1)
barlim = np.arange(-30,31,15)

fig = plt.figure()
ax1 = plt.subplot(131)

m = Basemap(projection='ortho',lon_0=0,lat_0=89,resolution='l',
            area_thresh=10000.)

var, lons_cyclic = addcyclic(diff_on, lon)
var, lons_cyclic = shiftgrid(180., var, lons_cyclic, start=False)
lon2d, lat2d = np.meshgrid(lons_cyclic, lat)
x, y = m(lon2d, lat2d)

pvalue_onq,lons_cyclic = addcyclic(pvalue_on, lon)
pvalue_onq,lons_cyclic = shiftgrid(180.,pvalue_onq,lons_cyclic,start=False)
          
m.drawmapboundary(fill_color='white',color='dimgray',linewidth=0.7)
m.drawcoastlines(color='dimgray',linewidth=0.8)
parallels = np.arange(-90,90,45)
meridians = np.arange(-180,180,60)
#m.drawparallels(parallels,labels=[True,True,True,True],
#                linewidth=0.6,color='dimgray',fontsize=6)
#m.drawmeridians(meridians,labels=[True,True,True,True],
#                linewidth=0.6,color='dimgray',fontsize=6)
#m.drawlsmask(land_color='dimgray',ocean_color='mintcream')

cs = m.contourf(x,y,var,limit,extend='both')
cs1 = ax1.scatter(x,y,pvalue_onq,color='k',marker='.',alpha=0.5,
                edgecolor='k',linewidth=0.2)

ax1.annotate(r'\textbf{ON}',
            xy=(0, 0),xytext=(0.35,1.05),xycoords='axes fraction',
            fontsize=25,color='dimgrey',rotation=0)

cmap = ncm.cmap('NCV_blu_red')            
cs.set_cmap(cmap)   

###########################################################################

ax2 = plt.subplot(132)

m = Basemap(projection='ortho',lon_0=0,lat_0=89,resolution='l',
            area_thresh=10000.)

var, lons_cyclic = addcyclic(diff_dj, lon)
var, lons_cyclic = shiftgrid(180., var, lons_cyclic, start=False)
lon2d, lat2d = np.meshgrid(lons_cyclic, lat)
x, y = m(lon2d, lat2d)

pvalue_djq,lons_cyclic = addcyclic(pvalue_dj, lon)
pvalue_djq,lons_cyclic = shiftgrid(180.,pvalue_djq,lons_cyclic,start=False)
          
m.drawmapboundary(fill_color='white',color='dimgray',linewidth=0.7)
m.drawcoastlines(color='dimgray',linewidth=0.8)
parallels = np.arange(-90,90,45)
meridians = np.arange(-180,180,60)
#m.drawparallels(parallels,labels=[True,True,True,True],
#                linewidth=0.6,color='dimgray',fontsize=6)
#m.drawmeridians(meridians,labels=[True,True,True,True],
#                linewidth=0.6,color='dimgray',fontsize=6)
#m.drawlsmask(land_color='dimgray',ocean_color='mintcream')

cs = m.contourf(x,y,var,limit,extend='both')
cs1 = ax2.scatter(x,y,pvalue_djq,color='k',marker='.',alpha=0.5,
                edgecolor='k',linewidth=0.2)

ax2.annotate(r'\textbf{DJ}',
            xy=(0, 0),xytext=(0.35,1.05),xycoords='axes fraction',
            fontsize=25,color='dimgrey',rotation=0)

cmap = ncm.cmap('NCV_blu_red')            
cs.set_cmap(cmap)  

###########################################################################

ax3 = plt.subplot(133)

m = Basemap(projection='ortho',lon_0=0,lat_0=89,resolution='l',
            area_thresh=10000.)

var, lons_cyclic = addcyclic(diff_fm, lon)
var, lons_cyclic = shiftgrid(180., var, lons_cyclic, start=False)
lon2d, lat2d = np.meshgrid(lons_cyclic, lat)
x, y = m(lon2d, lat2d)

pvalue_fmq,lons_cyclic = addcyclic(pvalue_fm, lon)
pvalue_fmq,lons_cyclic = shiftgrid(180.,pvalue_fmq,lons_cyclic,start=False)
          
m.drawmapboundary(fill_color='white',color='dimgray',linewidth=0.7)
m.drawcoastlines(color='dimgray',linewidth=0.8)
parallels = np.arange(-90,90,45)
meridians = np.arange(-180,180,60)
#m.drawparallels(parallels,labels=[True,True,True,True],
#                linewidth=0.6,color='dimgray',fontsize=6)
#m.drawmeridians(meridians,labels=[True,True,True,True],
#                linewidth=0.6,color='dimgray',fontsize=6)
#m.drawlsmask(land_color='dimgray',ocean_color='mintcream')

cs = m.contourf(x,y,var,limit,extend='both')
cs1 = ax3.scatter(x,y,pvalue_fmq,color='k',marker='.',alpha=0.5,
                edgecolor='k',linewidth=0.2)

ax3.annotate(r'\textbf{FM}',
            xy=(0, 0),xytext=(0.35,1.05),xycoords='axes fraction',
            fontsize=25,color='dimgrey',rotation=0)

cmap = ncm.cmap('NCV_blu_red')            
cs.set_cmap(cmap)  

cbar_ax = fig.add_axes([0.312,0.23,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='max',extendfrac=0.07,drawedges=False)
cbar.set_label(r'\textbf{m}',fontsize=11,color='dimgray')
cbar.set_ticks(barlim)
cbar.set_ticklabels(map(str,barlim)) 
cbar.ax.tick_params(axis='x', size=.01)

plt.subplots_adjust(wspace=0.01)

plt.savefig(directoryfigure + 'THICK_diff_FIT-HIT.png',dpi=300)
print('Completed: Script done!')



