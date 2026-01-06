### This module contains functions for downloading analysis from a variety of sources.
### Christopher Phillips
### Valparaiso University
### Dec. 2024

### Import modules
from datetime import timedelta
import urllib.request as ureq

### GFS analysis downloader for AWS source
### Inputs:
###  sdate, python datetime object, the first date to download
###  edate, python datetime object, the last date to download
###  interval, int, the interval between analysis times in hours
###  sdir, string , directory to which to save the data.
def gfs_download_aws(sdate, edate, interval, sdir):
    
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

### GFS analysis downloader for NCEP data
### Inputs:
###  sdate, python datetime object, the first date to download
###  edate, python datetime object, the last date to download
###  interval, int, the interval between analysis times in hours
###  sdir, string , directory to which to save the data.
def gfs_download_ncep(sdate, edate, interval, sdir):
    
    # Download the files
    date = sdate
    while date < edate:
        
        # Download the file
        url = f'https://osdf-director.osg-htc.org/ncar/gdex/d084001/{date.year}/{date.strftime("%Y%m%d")}/gfs.0p25.{date.strftime("%Y%m%d%H")}.f000.grib2'
        try:
            ureq.urlretrieve(url, f'{sdir}/gfs.0p25.{date.strftime("%Y%m%d_%H%MUTC")}')
        except:
            print('-------------------------------------------------')
            print(f'WARNING: file for {date.strftime("%-%m-%d %H UTC")} was unable to be downloaded. See URL below.')
            print(url)

        # Update the date
        date = date+timedelta(hours=interval)

        # Check that interval is positive
        if (date < sdate):
            raise Exception('Date is counting down. Check that interval is positive.')

    return

### GFS forecast downloader for NCEP data
### Inputs:
###  sdate, python datetime object, the first date to download
###  edate, python datetime object, the last date to download
###  interval, int, the interval between analysis times in hours
###  sdir, string , directory to which to save the data.
def gfsf_download_ncep(sdate, edate, interval, sdir):
    
    # Download the files
    date = sdate
    while date < edate:
    
        fhour = int((date-sdate).total_seconds()/3600)
        
        # Download the file
        url = f'https://osdf-director.osg-htc.org/ncar/gdex/d084001/{sdate.year}/{sdate.strftime("%Y%m%d")}/gfs.0p25.{sdate.strftime("%Y%m%d%H")}.f{fhour:03d}.grib2'
        try:
            ureq.urlretrieve(url, f'{sdir}/gfs.0p25.{date.strftime("%Y%m%d_%H%MUTC")}')
        except:
            print('-------------------------------------------------')
            print(f'WARNING: file for {date.strftime("%-%m-%d %H UTC")} was unable to be downloaded. See URL below.')
            print(url)

        # Update the date
        date = date+timedelta(hours=interval)

        # Check that interval is positive
        if (date < sdate):
            raise Exception('Date is counting down. Check that interval is positive.')

    return

### GFS forecast downloader for AWS data
### Inputs:
###  sdate, python datetime object, the first date to download
###  edate, python datetime object, the last date to download
###  interval, int, the interval between analysis times in hours
###  sdir, string , directory to which to save the data.
def gfsf_download_aws(sdate, edate, interval, sdir):

    # Download the files
    date = sdate
    while date < edate:

        fhour = int((date-sdate).total_seconds()/3600)

        # Download the file
        url = f'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.{sdate.strftime("%Y%m%d")}/{sdate.hour:02d}/gfs.t{sdate.hour:02d}z.pgrb2.0p25.f{fhour:03d}'
        try:
            ureq.urlretrieve(url, f'{sdir}/gfs.0p25.{date.strftime("%Y%m%d_%H%MUTC")}')
        except:
            print('-------------------------------------------------')
            print(f'WARNING: file for {date.strftime("%-%m-%d %H UTC")} was unable to be downloaded. See URL below. Trying other format.')
            print(url)

            try:
                url = f'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.{sdate.strftime("%Y%m%d")}/{sdate.hour:02d}/atmos/gfs.t{sdate.hour:02d}z.pgrb2.0p25.f{fhour:03d}'
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
def hrrrf_download(sdate, edate, interval, sdir):

    # Download the files
    date = sdate
    while date < edate:
        
        fhour = int((date-sdate).total_seconds()/3600)

        # Download the file
        url = f'https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.{sdate.strftime("%Y%m%d")}/conus/hrrr.t{sdate.hour:02d}z.wrfprsf{fhour:02d}.grib2'
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

### NAM analysis downloader
### Inputs:
###  sdate, python datetime object, the first date to download
###  edate, python datetime object, the last date to download
###  interval, int, the interval between analysis times in hours
###  sdir, string , directory to which to save the data.
def nam_download(sdate, edate, interval, sdir):

    # Download the files
    date = sdate
    while date < edate:

        # Download the file
        url = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{date.strftime("%Y%m%d")}/nam.t{date.hour:02d}z.awphys00.tm00.grib2'
        try:
            ureq.urlretrieve(url, f'{sdir}/nam.{date.strftime("%Y%m%d_%H%MUTC")}')
        except:
            print('-------------------------------------------------')
            print(f'WARNING: file for {date.strftime("%-%m-%d %H UTC")} was unable to be downloaded. See URL below.')
            print(url)

        # Update the date
        date = date+timedelta(hours=interval)

        # Check that interval is positive
        if (date < sdate):
            raise Exception('Date is counting down. Check that interval is positive.')

    return

### NAM forecast downloader
### Inputs:
###  sdate, python datetime object, the first date to download
###  edate, python datetime object, the last date to download
###  interval, int, the interval between analysis times in hours
###  sdir, string , directory to which to save the data.
def namf_download(sdate, edate, interval, sdir):

    # Download the files
    date = sdate
    while date < edate:

        fhour = int((date-sdate).total_seconds()/3600)

        # Download the file
        url = f'https://noaa-nam-pds.s3.amazonaws.com/nam.{sdate.strftime("%Y%m%d")}/nam.t{sdate.hour:02d}z.awphys{fhour:02d}.tm00.grib2'
        try:
            ureq.urlretrieve(url, f'{sdir}/nam.{date.strftime("%Y%m%d_%H%MUTC")}')
        except:
            print('-------------------------------------------------')
            print(f'WARNING: file for {date.strftime("%-%m-%d %H UTC")} was unable to be downloaded. See URL below.')
            print(url)



        # Update the date
        date = date+timedelta(hours=interval)

        # Check that interval is positive
        if (date < sdate):
            raise Exception('Date is counting down. Check that interval is positive.')

    return

### HRRR forecast downloader
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
