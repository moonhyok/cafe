#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *

"""
The fields of the file look like this:
"zip","type","primary_city","acceptable_cities","unacceptable_cities","state","county","timezone","area_codes","latitude","longitude","world_region","country","decommissioned","estimated_population","notes"
"""

with open('/Users/jaypatel/cafe/doc/zip_code_database.csv') as zipcode_db:
    for i, line in enumerate(zipcode_db):
        if i == 0: #header row
            continue
        else:
            line = line.split(",")
            if 'CA' in line[5]:
                code, city, state = line[0], line[2], line[5]
                z = ZipCode(code=code, city=city, state=state)
                z.save()
                
            
        
