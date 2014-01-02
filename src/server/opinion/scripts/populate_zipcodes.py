#!/usr/bin/env python
import environ
import os
import csv
from opinion.opinion_core.models import *

"""
The fields of the file look like this:
zip,type,primary_city,acceptable_cities,unacceptable_cities,state,county,timezone,area_codes,latitude,longitude,world_region,country,decommissioned,estimated_population,notes
"""

fname = '../../../doc/zip_code_database.csv'
raw_input("Using zipcode db located at: " \
          + os.path.abspath(fname) + ", ok? [y]")

for i, line in enumerate(csv.reader(open(fname))):
    if i == 0: # header row
        continue
    else:
        if i % 1000 == 0:
            print str(i) + " completed"

        code, city, state, county  = line[0], line[2], line[5], line[6]
        
        z = ZipCode(code=code, city=city, state=state, county=county)
        z.save()
                
            
        
