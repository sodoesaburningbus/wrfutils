### This script reads a namelist.wps file
### and plots the grid described therein.
### 
### Christopher Phillips
### Valparaiso University
### Dec. 2024
###
### Usage -
### python display_grid_wps.py `file_path` `save plot` [lon_of_interest] [lat_of_interest]
###
### Examples -
### python display_grid_wps.py namelist.wps True
### python display_grid_wps.py namelist.wps False -96 40

# Import modules
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import f90nml
import matplotlib.patches as patches
import matplotlib.pyplot as pp
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

# Read in the namelist
nml = f90nml.read(file_path)

# Pull the grid parameters
ngrids = nml['share']['max_dom']
xs = nml['geogrid']['i_parent_start']
ys = nml['geogrid']['j_parent_start']
xe = nml['geogrid']['e_we']
ye = nml['geogrid']['e_sn']
ratio = nml['geogrid']['parent_grid_ratio']
dx = list([nml['geogrid']['dx']/r for r in ratio])
dy = list([nml['geogrid']['dy']/r for r in ratio])
latc = nml['geogrid']['ref_lat']
lonc = nml['geogrid']['ref_lon']
true_lat1 = nml['geogrid']['truelat1']
true_lat2 = nml['geogrid']['truelat2']
true_lon = nml['geogrid']['stand_lon']

# Handle the projection
pc_proj = ccrs.PlateCarree()
if (nml['geogrid']['map_proj'] == 'lambert'):
    wrf_proj = ccrs.LambertConformal(true_lon, latc, standard_parallels=(true_lat1, true_lat2))

elif (nml['geogrid']['map_proj'] == 'mercator'):
    wrf_proj = ccrs.Mercator(central_longitude=true_lon, latitude_true_scale=true_lat1)

else:
    raise Exception(f'"{nml["geogrid"]["map_proj"]}" not currently supported by this script.')

# Build the WRF grid
# First convert center points into the proper projection
xc, yc = wrf_proj.transform_point(lonc, latc, pc_proj)

# Now compute the grid point locations
x = list([(np.arange(0, e)-e/2)*d for e, d in zip(xe, dx)])
y = list([(np.arange(0, e)-e/2)*d for e, d in zip(ye, dy)])

# Mesh the grid
xg = []
yg = []
for xi, yi in zip(x, y):
    dummy_x, dummy_y = np.meshgrid(xi, yi)
    xg.append(dummy_x)
    yg.append(dummy_y)

# Make the plot
fig, ax = pp.subplots(subplot_kw={'projection':wrf_proj}, figsize=(8,8))

# Map decorations
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.LAND, color='darkolivegreen')
ax.add_feature(cfeature.OCEAN, color='skyblue')

# Add grid patches
for gi, xi, yi in zip(range(ngrids), x, y):

    grid = patches.Rectangle(xy=[xi[0], yi[0]], width=xi[-1]-xi[0], height=yi[-1]-yi[0],
                             facecolor='none', edgecolor='firebrick', linewidth=2.0, transform=wrf_proj)
    ax.add_patch(grid)
    ax.text(xi[0], yi[-1]+dy[gi]*4, f'Grid {gi}', color='firebrick', fontsize=14)

# Set the extent
ax.set_extent([x[0][0]-dx[0]*10, x[0][-1]+dx[0]*10, y[0][0]-dy[0]*10, y[0][-1]+dy[0]*10], crs=wrf_proj)
ax.scatter(lonc, latc, transform=pc_proj, color='firebrick', marker='x')

# Check for point of interest
if (len(sys.argv) == 5):
    ax.scatter(float(sys.argv[3]), float(sys.argv[4]), color='darkgoldenrod', transform=pc_proj)

# Save or display?
if save_plot:
    pp.savefig('wrf_grid.png')
else:
    pp.show()