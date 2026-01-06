### This script reads geogrid files from a WPS directory
### and plots the grid described therein.
### 
### Christopher Phillips
### Valparaiso University
### Dec. 2025
###
### Usage -
### python display_grid_wps.py `file_path` `save plot` [lon_of_interest] [lat_of_interest]
###
### Examples -
### python display_grid_wps.py /home/WPS True
### python display_grid_wps.py /home/WPS False -96 40

# Import modules
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from glob import glob
import matplotlib.patches as patches
import matplotlib.pyplot as pp
import netCDF4 as nc
import numpy as np
import sys

# Read the command line arguments
file_path = sys.argv[1]
if (sys.argv[2].lower() == 'true'):
    save_plot = True
elif (sys.argv[2].lower() == 'false'):
    save_plot = False
else:
    raise ValueError(f'Save flag must be "True" or "False" not "{sys.argv[2]}"')

# Create the figure object for map
pc_proj = ccrs.PlateCarree()
fig, ax = pp.subplots(subplot_kw={'projection':pc_proj}, figsize=(8,8), dpi=100)

# Map decorations
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.LAND, color='darkolivegreen')
ax.add_feature(cfeature.OCEAN, color='skyblue')

# Locate the geogrid files
gfiles = sorted(glob(file_path+'/geo_em*.nc'))

# Loop over the grid files and make the figure
for gi, gfile in enumerate(gfiles):
    fn = nc.Dataset(gfile)
    lons = fn.variables['XLONG_M'][0,:,:]
    lats = fn.variables['XLAT_M'][0,:,:]

    grid = patches.Rectangle(xy=[lons[0,0], lats[0,0]], width=lons[-1,-1]-lons[0,0], height=lats[-1,-1]-lats[0,0],
                             facecolor='none', edgecolor='firebrick', linewidth=2.0, transform=pc_proj)
    ax.add_patch(grid)
    ax.text(lons[0,0]+0.1, lats[-1,-1]+0.1, f'Grid {gi}', color='firebrick', fontsize=14, transform=pc_proj)

    # Add center of the domain
    ax.scatter(np.mean(lons), np.mean(lats), transform=pc_proj, color='firebrick', marker='x')

# Check for point of interest
if (len(sys.argv) == 5):
    ax.scatter(float(sys.argv[3]), float(sys.argv[4]), color='darkgoldenrod', transform=pc_proj)

# Save or display?
if save_plot:
    pp.savefig('wrf_grid.png')
else:
    pp.show()
