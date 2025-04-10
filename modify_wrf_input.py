### This program demonstrates how to change a variable in a set of WRF input files.
### It overwrites the original files so real.exe has to be re-run if you want the originals back.
### Christopher Phillips
### Valparaiso University

##### START OPTIONS #####

# Location of WRF run ditrectory
wdir = '/storage/cphill19/met430/phillips/BUILD_WRF/WRF/run_test/'

# Location to save plot with showing changes
spath = 'changed_inputs.png'

#####  END OPTIONS  #####

### Import modules
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from glob import glob
import matplotlib.pyplot as pp
import netCDF4 as nc
import numpy as np

# Locate the WRF input files
wfiles = glob(f'{wdir}/wrfinput_d*')

for wfile in wfiles:

    # Open the file and bring in the data
    fn = nc.Dataset(wfile, 'a')
    lons = fn.variables['XLONG'][0,:,:] # Time, Y, X dimensions
    lats = fn.variables['XLAT'][0,:,:]
    pres = fn.variables['PB'][:,:,:,:] #Time, Z, Y, X dimensions

    print(pres.shape)

    # Let's adjust the pressure using a sinusoidal wave based on longitude
    pwave = np.sin(lons/lons.max()*np.pi/2.0)+0.1
    new_pres = np.ones(pres.shape)*pres
    for k in range(pres.shape[1]):
        new_pres[:,k,:,:] *= pwave

    # Re-assign the pressure variable
    fn.variables['PB'][:] = new_pres

    # Save the file
    fn.close()

# Make the plot using the last input file
fig, (ax1, ax2) = pp.subplots(nrows=2, subplot_kw={'projection':ccrs.PlateCarree()})

cont1 = ax1.contourf(lons, lats, pres[0,0,:,:])
cont2 = ax2.contourf(lons, lats, new_pres[0,0,:,:])

cb1 = fig.colorbar(cont1, ax=ax1, orientation='vertical')
cb1.set_label('Pressure (Pa)')

cb2 = fig.colorbar(cont2, ax=ax2, orientation='vertical')
cb2.set_label('Pressure (Pa)')


# Add map stuff
for ax in (ax1, ax2):
    ax.add_feature(cfeature.STATES)
    ax.add_feature(cfeature.COASTLINE)

pp.savefig(spath)
pp.close # When running SLURM jobs, make sure to close your plots
