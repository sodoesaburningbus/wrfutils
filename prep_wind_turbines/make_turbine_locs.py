### This script creats the windturbines.txt file for WRF.
### To use it, change the list of farm names in the options
### to add those wind turbines to the list.
### This name matches the "p_name" field in national_windturbines.csv.
###
### Note, new wind turbine files are created each time, so
### be careful when setting the save path. Also, the model and details files are to aid the user
### in creating the turbine table files. They are NOT WRF-ready.
### The location file IS WRF-ready.
###
### Christopher Phillips

##### START OPTIONS #####

# Wind farms to include
farms = ['Maple Ridge', 'Maple Ridge (Lowville)',]

# Location to save the wind turbine location file
spath = 'winter_windturbines.txt'
spath2 = 'winter_model_numbers.txt'
spath3 = 'winter_turbine_details.txt'

#####  END OPTIONS  #####

### Import required modules
import pandas as pd

# Open a new file for writing
out_fn1 = open(spath, 'w')
out_fn2 = open(spath2, 'w')
out_fn3 = open(spath3, 'w')
out_fn2.write('Label,Manufacturer,ModelNumber,')

# Read the file
all_turbines = pd.read_csv('national_windturbines.csv', usecols=[8,12,13,14,15,16,25,26])

# Loop over desired wind farms and extract from file
turbine_type = None
turbine_type_num = 0
loc_list = []
details = ['HubHeight RotorDiameter MaxPower']
for farm in farms:
    turbines = all_turbines[all_turbines['p_name'] == farm]

    # Now add each of these to the save file
    for r, row in turbines.iterrows():

        # Check if a new wind turbine type
        # and update model file
        if (row['t_model'] != turbine_type):
            turbine_type_num += 1
            turbine_type = row['t_model']
            out_fn2.write(f"\n{turbine_type_num},{row['t_manu']},{row['t_model']}")

        # Add turbine to the location list
        loc_list.append(f"{row['ylat']} {row['xlong']} {turbine_type_num}\n")
        details.append(f'\n{row['t_hh']} {row['t_rd']} {row['t_cap']}')

# Write location file
out_fn1.write(''.join(loc_list)[:-1]) # Through last character to remove tariling newline
out_fn3.write(''.join(details))

# Close files
out_fn1.close()
out_fn2.close()
out_fn3.close()

