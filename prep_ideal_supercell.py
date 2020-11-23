#This program takes a WRF input file from real.exe
#and modifies it to run an ideal supercell case.
#Chris Phillips

##### START OPTIONS #####

#Location of WRF input file
fpath = "/rstor/cphillip/model_exps/irrigated_supercell/run/wrfinput_d01"

#Location of desired sounding
sounding_path = "/rstor/cphillip/model_exps/irrigated_supercell/run/input_sounding"

#Desired land use class
lu_index = 5 #5 is USGS grassland/cropland mosaic

#Desired soil type
soil = 4 #4 is silt loam

#Desired vegetation fraction
vegfra = 100.0

#All and or all water (1=land, 2=water)
land_water = 1

#Radius of warm bubble (meters)
bubbler = 2000.0

#Starting height of warm bubble (meters)
bubbleh = 2000.0

#Warm bubble perturbation
bubblet = 2.0

#Irrigation percentage
irrigation = 100.0

#Model parameters, shouldn't need changing
#Base state temperature (Kelvin, from WRF, if you don't know, use 290)
t0 = 290.0
shdmin = 0.0 #Minimum vegetation annual fraction
shdmax = 100.0 #Maximum vegetation annual fraction

#####  END OPTIONS  #####

#Importing required modules
import atmos.thermo as at
import numpy
import netCDF4 as nc
from pysonde.pysonde import PySonde

#Read in the sounding
sonde = PySonde(sounding_path, "WRF")
sounding = sonde.strip_units()

#Convert units of sounding to match WRF
sounding["pres"] *= 100.0 #hPa -> Pa
sounding["temp"] += 273.15 #'C -> K
sounding["dewp"] += 273.15 #'C -> K

#Calculate necessary variables
theta = at.pot_temp(sounding["pres"], sounding["temp"]) #Potential temperature
mixr = at.etow(sounding["pres"], at.sat_vaporpres(sounding["dewp"]))
mtheta = (theta*1+at.RV/at.RD*mixr)

#Open the file
fn = nc.Dataset(fpath, "r+")

#Grab the model pressure levels
smlevels = numpy.mean(fn.variables["PB"], axis=0)
mlevels = (smlevels[1:]+smleves[:-1])/2.0

#Interpolate necessary variables to model levels
iuwind = numpy.interp(mlevels, sounding["pres"], sounding["uwind"])
ivwind = numpy.interp(mlevels, sounding["pres"], sounding["vwind"])
iphb = numpy.interp(smlevels, sounding["pres"], sounding["alt"]*at.G)
itheta = numpy.interp(mlevels, sounding["pres"], theta-t0)
ithm = numpy.interp(mlevels, sounding["pres"], mtheta-t0)
itinit = numpy.interp(mlevels, sounding["pres"], theta)
imixr = numpy.interp(mlevels, sounding["pres"], mixr)

#Fill the (unstaggered) model levels
for i in range(iuwind.size):
    fn.variables["U"][:,i,:,:] = iuwind[i]
    fn.variables["V"][:,i,:,:] = ivwind[i]
    fn.variables["T"][:,i,:,:] = itheta[i]
    fn.variables["THM"][:,i,:,:] = ithm[i]
    fn.variables["T_INIT"][:,i,:,:] = itinit[i]
    fn.variables["QVAPOR"][:,i,:,:] = imixr[i]

#Fill the (staggered) model levels
for i in range(iphb.size):
    fn.variables["PHB"][:,i,:,:] = iphb[i]
    
#Model surface variables
fn.variables["T2"][:] = sounding["temp"][0]
fn.variables["Q2"][:] = mixr[0]
fn.variables["TH2"][:] = theta[0]
fn.variables["PSFC"][:] = sounding["pres"][0]
fn.variables["U10"][:] = sounding["uwind"][0]
fn.variables["V10"][:] = sounding["vwind"][0]

#Set the other variables with constants
fn.variables["IRRIGATION"][:] = irrigation
fn.variables["W"][:] = 0.0
fn.variables["QCLOUD"] = 0.0
fn.variables["QRAIN"] = 0.0
fn.variables["QSNOW"] = 0.0
fn.variables["QGRAUP"] = 0.0
fn.variables["QNICE"] = 0.0
fn.variables["QNRAIN"] = 0.0
fn.variables["SHDMIN"] = shdmin
fn.variables["SHDMAX"] = shdmax
fn.variables["IVGTYP"] = lu_index
fn.variables["ISLTYP"] = soil
fn.variables["VEGFRA"] = vegfra
fn.variables["XLAND"] = land_water
fn.variables["SNOWC"] = 0
if (land_water == 1):
    fn.variables["LANDMASK"] = 1
else:
    fn.variables["LANDMASK"] = 0
fn.variables["LAKEMASK"] = 0

#Close the input file to save the changes
fn.close()
