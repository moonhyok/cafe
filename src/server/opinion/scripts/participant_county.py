#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
try:
    import json
except ImportError:
    import simplejson as json
import numpy
from opinion.includes.queryutils import *

os.environ['MPLCONFIGDIR'] = "/tmp"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import settings
imagepath = settings.MEDIA_ROOT + "/mobile/img/dailyupdate/"
jspath= settings.MEDIA_ROOT + "/mobile/js/"
import datetime



def geostats():
    """produce geojson file for leaflet"""
    f=open(imagepath+'participant_county.txt','w')
    f.write("all log zip "+str(len(ZipCodeLog.objects.all()))+'\n')
    geo_json=open('/var/www/latest-version/src/server/opinion/geo-ca.json')
    geo_data=json.load(geo_json)
    skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)
    statements = OpinionSpaceStatement.objects.all().order_by('id')
    for s in statements:
       skip_ca=0
       for i in range(0,len(geo_data['features'])):
          county=geo_data['features'][i]['properties']['NAME']
          zipcode_in_county=ZipCode.objects.filter(state='CA').filter(county__startswith=county)
          s_grade=[]
          s_skip=0
          for j in range(0, len(zipcode_in_county)):
             log=ZipCodeLog.objects.filter(location__exact=zipcode_in_county[j])
             for k in range(0, len(log)):
             	if log[k].user.is_active:  #make sure active
                   visitor=Visitor.objects.filter(user=log[k].user)  #connect to visitor
                   user_grade_s=log[k].user.userrating_set.filter(opinion_space_statement=s,is_current=True) #filter grade
                   if len(user_grade_s)>0:
                      if len(visitor)>0:
                         if user_grade_s[0].created>=skip_begin_date:
                            s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains=str(s.id)).order_by('-created') #get issue skip log
                            s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').filter(details__startswith='slider_set '+str(s.id)).order_by('-created')
                            if len(s_log_skip)==0: #no skip
                               if len(s_log_rating)>0:
                                  s_grade.append(user_grade_s[0].rating)
                               else: #not click on skip, not move slider s, => skip
                                  s_skip=s_skip+1
                            else:
                               if len(s_log_rating)==0:  #click skip, not move slider s => skip
                                  s_skip=s_skip+1
                               else:
                                  if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                                     s_skip=s_skip+1
                                  else:
                                     s_grade.append(user_grade_s[0].rating)
                         else:
                            s_grade.append(user_grade_s[0].rating) 
                      else: 
                         s_grade.append(user_grade_s[0].rating)
                   else:
                      s_skip=s_skip+1
          skip_ca=skip_ca+s_skip
          f.write(str(county)+":"+str(len(s_grade)+s_skip)+'\n')
          if len(s_grade)+s_skip==0:
             geo_data['features'][i]['properties']["s"+str(s.id)]=10  #for leaflet to show NA color
             geo_data['features'][i]['properties']['PARTICIPANTS']=0
          if len(s_grade)+s_skip>0:
             geo_data['features'][i]['properties']['PARTICIPANTS']=len(s_grade)+s_skip
             if len(s_grade)>0:
                geo_data['features'][i]['properties']["s"+str(s.id)]=numpy.median(s_grade)
             else:
                geo_data['features'][i]['properties']["s"+str(s.id)]=10
    with open(jspath+'geostat_population.js', 'w') as outfile:
         outfile.write('var geostat_population=')
         json.dump(geo_data, outfile)
         outfile.write(';')  

geostats()
