### This module contains functions for downloading analysis from a variety of sources.
### Christopher Phillips
### Valparaiso University
### Dec. 2024

### Import modules
from datetime import timedelta
import urllib.request as ureq

### GFS downloader
### Inputs:
###  sdate, python datetime object, the first date to download
###  edate, python datetime object, the last date to download
###  interval, int, the interval between analysis times in hours
###  sdir, string , directory to which to save the data.
def gfs_download(sdate, edate, interval, sdir):
    
    # Download the files
    date = sdate
    while date < edate:
        
        # Download the file
        url = f'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.{date.strftime("%Y%m%d")}/{date.hour:02d}/gfs.t{date.hour:02d}z.pgrb2.0p25.f000'
        try:
            ureq.urlretrieve(url, f'{sdir}/gfs.0p25.{date.strftime("%Y%m%d_%H%MUTC")}')
        except:
            print('-------------------------------------------------')
            print(f'WARNING: file for {date.strftime("%-%m-%d %H UTC")} was unable to be downloaded. See URL below. Trying other format.')
            print(url)

            try:
                url = f'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.{date.strftime("%Y%m%d")}/{date.hour:02d}/atmos/gfs.t{date.hour:02d}z.pgrb2.0p25.f000'
                ureq.urlretrieve(url, f'{sdir}/gfs.0p25.{date.strftime("%Y%m%d_%H%MUTC")}')
            except:
                print(f'Other format failed. See URL below.')
                print(url)

        # Update the date
        date = date+timedelta(hours=interval)

        # Check that interval is positive
        if (date < sdate):
            raise Exception('Date is counting down. Check that interval is positive.')

    return

### HRRR downloader
### Inputs:
###  sdate, python datetime object, the first date to download
###  edate, python datetime object, the last date to download
###  interval, int, the interval between analysis times in hours
###  sdir, string , directory to which to save the data.
def hrrr_download(sdate, edate, interval, sdir):

    # Download the files
    date = sdate
    while date < edate:
        
        # Download the file
        url = f'https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.{date.strftime("%Y%m%d")}/conus/hrrr.t{date.hour:02d}z.wrfprsf00.grib2'
        try:
            ureq.urlretrieve(url, f'{sdir}/hrrr.wrfprs.{date.strftime("%Y%m%d_%H%MUTC")}')
        except:
            print(f'WARNING: file for {date.strftime("%-%m-%d %H UTC")} was unable to be downloaded. See URL below.')
            print(url)

        # Update the date
        date = date+timedelta(hours=interval)

        # Check that interval is positive
        if (date < sdate):
            raise Exception('Date is counting down. Check that interval is positive.')

    return