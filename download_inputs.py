### This script downloads grib2 files for a user-selected model
### that can then be used with the WPS.
### Command line inputs are start date, end date, interval between analyses in hours, data source, and save directory.
### Note that the date range is inclusive on both ends.
###
### Usage
### python download_inputs.py startYYYYMMDD_HH endYYYYMMDD_HH interval source save_directory
###
### Example
### python download_inputs.py 20210203_00 20210204_00 6 GFS gfs_inputs
###
### Christopher Phillips
### Valparaiso Univ.
### Dec. 2024
###
### Currently supports
### GFS

# Import modules
from datetime import datetime
import os
import sys

from utils import downloaders

# Read in the command line arguments
start_date = datetime.strptime(sys.argv[1], "%Y%m%d_%H")
end_date = datetime.strptime(sys.argv[2], "%Y%m%d_%H")
interval = int(sys.argv[3])
source = sys.argv[4].lower()
save_dir = sys.argv[5]

# Try to make the save directory in case it doesn't exist
try:
    os.system(f'mkdir {save_dir}')
except:
    pass

# Call the appropriate downloader
if (source == 'gfs'):
    downloaders.gfs_download(start_date, end_date, interval, save_dir)

else:
    raise Exception(f'Source "{source}" is not supported at this time. See script header for supported data sources.')