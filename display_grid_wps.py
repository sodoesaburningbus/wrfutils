### This script reads a namelist.wps file
### and plots the grid described therein.
### 
### Christopher Phillips
### Valparaiso University
### Dec. 2024
###
### Usage -
### python display_grid_wps.py `file_path` `save plot`
###
### Example -
### python display_grid_wps.py namelist.wps True

# Import modules
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import f90nml
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

# Handle the projection
pc_proj = ccrs.PlateCarree()
if (nml['geogrid']['map_proj'] == 'lambert'):
    wrf_proj = ccrs.LambertConformal(lonc, latc, standard_parallels=(true_lat1, true_lat2))
else:
    raise Exception(f'"{nml["geogrid"]["map_proj"]}" not currently supported by this script.')

# Build the WRF grid
