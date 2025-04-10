### This program demonstrates how to plot a variable from a WRF output file
###

##### START OPTIONS #####

# Location of a WRF file
wfile = '/storage/cphill19/met430/phillips/BUILD_WRF/WRF/run_test/wrfout_d01_2024-04-29_00:00:00'

# Place to save the output
spath = 'test_plot.png'

#####  END OPTIONS  #####

### Import modules
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as pp
import netCDF4 as nc
import numpy as np

# Open the file and bring in the data
fn = nc.Dataset(wfile, 'r')
lons = fn.variables['XLONG'][0,:,:] # Dimensions are Time, Y, X
lats = fn.variables['XLAT'][0,:,:]
t2 = fn.variables['T2'][0,:,:]
psfc = fn.variables['PB'][0,0,:,:]+fn.variables['P'][0,0,:,:] # Dimensions are Time, Z, Y, X
# (Combine both Base pressure and perturbation pressure)
fn.close()

# Make the plot
fig, ax = pp.subplots(subplot_kw={'projection':ccrs.PlateCarree()})

pcont = ax.contour(lons, lats, psfc, colors='black')
tcont = ax.contourf(lons, lats, t2, cmap='turbo')

cb = fig.colorbar(tcont)
cb.set_label('Temperature (K)')

ax.clabel(pcont, inline=True)

# Add map stuff
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.COASTLINE)

pp.savefig(spath)
pp.close # When running SLURM jobs, make sure to close your plots
