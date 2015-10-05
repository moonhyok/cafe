from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.db import connection
from django.http import HttpResponseServerError
from django.http import HttpResponseRedirect
from django.core.validators import validate_email

from opinion.opinion_core.models import *
from opinion.opinion_core.admin import *
from opinion.opinion_core.forms import *
from opinion.includes.queryutils import *
from opinion.settings import *

from opinion.settings_local import CATEGORIES
from opinion.includes.plotutils import *
from opinion.decorators import *

from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_control

import math
import numpy
import operator
import random
import sys
import datetime
import time
import datetime
import hashlib
import os
import re

os.environ['MPLCONFIGDIR'] = "/tmp"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    import json
except ImportError:
    import simplejson as json

def geostats(request):
    """produce geojson file for leaflet"""
    geo_json=open(os.path.join(GEOJSON_ROOT, 'geo.json'))
    geo_data=json.load(geo_json)

    statements = OpinionSpaceStatement.objects.all().order_by('id')
    for s in statements:
       for i in range(0,len(geo_data['features'])-1):
          county=geo_data['features'][i]['properties']['NAME']
          zipcode_in_county=ZipCode.objects.filter(state='CA').filter(county__startswith=county)
          s_grade=[]
          for j in range(0, len(zipcode_in_county)):
             log=ZipCodeLog.objects.filter(location__exact=zipcode_in_county[j])
             for k in range(0, len(log)):
                user_grade_s=log[k].user.userrating_set.filter(opinion_space_statement=s,is_current=True)
                if len(user_grade_s)>0:
                   s_grade.append(user_grade_s[0].rating)
          if len(s_grade)==0:
             geo_data['features'][i]['properties']["s"+str(s.id)]=10
             geo_data['features'][i]['properties']['PARTICIPANTS']=0
          if len(s_grade)>0:
             geo_data['features'][i]['properties']["s"+str(s.id)]=numpy.median(s_grade)
             geo_data['features'][i]['properties']['PARTICIPANTS']=len(s_grade)

    #find median for non ca zipcode
    zipcode_nonca=ZipCode.objects.exclude(state='CA')
    for s in statements:
        s_grade=[]
        for j in range(0, len(zipcode_nonca)):
            log=ZipCodeLog.objects.filter(location__exact=zipcode_nonca[j])
            for k in range(0, len(log)):
                user_grade_s=log[k].user.userrating_set.filter(opinion_space_statement=s,is_current=True)
                if len(user_grade_s)>0:
                   s_grade.append(user_grade_s[0].rating)
        if len(s_grade)==0:
            geo_data['features'][len(geo_data['features'])-1]['properties']["s"+str(s.id)]=10
            geo_data['features'][len(geo_data['features'])-1]['properties']['PARTICIPANTS']=0
        if len(s_grade)>0:
            geo_data['features'][len(geo_data['features'])-1]['properties']["s"+str(s.id)]=numpy.median(s_grade)
            geo_data['features'][len(geo_data['features'])-1]['properties']['PARTICIPANTS']=len(s_grade)

    outfile = open('geostat.js', 'w')
    outfile.write('var geostat=')
    json.dump(geo_data, outfile)
    outfile.write(';')
    outfile.close()


def issues_hist(request):
   """produce histogram for each issue"""
   statements = OpinionSpaceStatement.objects.all().order_by('id')
   bins=[0,0.01,0.19,0.32,0.38,0.44,0.56,0.63,0.69,0.81,0.86,0.92,0.99,1]  
        # F    D-   D    D+   C-   C    C+   B-   B   B+    A-   A    A+
   N=len(bins)-1
   ind=numpy.arange(N)
   width=0.35
   
   for s in statements:
       s_rating=UserRating.objects.filter(opinion_space_statement=s,is_current=True)
       s_rating_list=[]
       for rating in s_rating:
          s_rating_list.append(1-rating.rating)
       
       hist,bin_edges = numpy.histogram(s_rating_list,bins,normed=False)
       hist_in_percent=(100*hist/float(sum(hist)))[::-1]
       
       fig, ax = plt.subplots()
       rects1 = ax.bar(ind, hist_in_percent, width, color='r')
       median=numpy.median(s_rating_list)
       median_bar=median_index(request,median)
       rects1[median_bar].set_color('b')
       ax.set_ylabel('Percentages (%)')
       ax.set_title(s.statement)
       ax.set_xticks(ind+width/2)
       ax.set_xticklabels( ('A+', 'A', 'A-', 'B+', 'B','B-','C+','C','C-','D+','D','D-','F') )
       plt.savefig(s.statement+'.png',dpi=300,format='png')

def median_index(request,median):
     if median<=1 and median>0.99:
        return 0
     if median<=0.99 and median>0.92:
        return 1
     if median<=0.92 and median>0.86:
        return 2
     if median<=0.86 and median>0.81:
        return 3
     if median<=0.81 and median>0.69:
        return 4
     if median<=0.69 and median>0.63:
        return 5
     if median<=0.63 and median>0.56:
        return 6
     if median<=0.56 and median>0.44:
        return 7
     if median<=0.44 and median>0.38:
        return 8
     if median<=0.38 and median>0.32:
        return 9
     if median<=0.32 and median>0.19:
        return 10
     if median<=0.19 and median>0.01:
        return 11
     if median<=0.01:
        return 12


def participant_hist(request):
    """produce histogram for all participant above level 8"""
    
    
    os = get_os(1)
    disc_stmt = get_disc_stmt(os, 1)
    
    bins=[0,0.01,0.19,0.32,0.38,0.44,0.56,0.63,0.69,0.81,0.86,0.92,0.99,1]  
        # F    D-   D    D+   C-   C    C+   B-   B   B+    A-   A    A+
    N=len(bins)-1
    ind=numpy.arange(N)
    width=0.35
    alluser=User.objects.all()
   
    for cur_user in alluser:
        if len(cur_user.email)>0:
           cur_user_comment=DiscussionComment.objects.filter(user=cur_user,discussion_statement= disc_stmt,is_current = True)
           if len(cur_user_comment)>0:
              slider1=CommentAgreement.objects.filter(comment=cur_user_comment[0])
              slider2=CommentRating.objects.filter(comment=cur_user_comment[0])
              slider1_rating=[]
              slider2_rating=[]
               
              for i in range(0, len(slider1)):
                 slider1_rating.append(1-slider1[i].agreement)
              for i in range(0, len(slider2)):
                 slider2_rating.append(1-slider2[i].rating)
              #produce png only if len(slider) >0
              if len(slider1)>0:
                 slider1_hist,bin_edges_1 = numpy.histogram(slider1_rating,bins,normed=False)
                 slider1_hist_in_percent=(100*slider1_hist/float(sum(slider1_hist)))[::-1]
                 fig1, ax1=plt.subplots()
                 rects1 = ax1.bar(ind, slider1_hist_in_percent, width, color='r')
                 median1=numpy.median(slider1_rating)
                 median_bar1=median_index(request,median1)
                 rects1[median_bar1].set_color('b')
                 ax1.set_ylabel('Percentages (%)')
                 ax1.set_title("How important is this issue for the next Report Card?")
                 ax1.set_xticks(ind+width/2)
                 ax1.set_xticklabels( ('A+', 'A', 'A-', 'B+', 'B','B-','C+','C','C-','D+','D','D-','F') )
                 plt.savefig(str(cur_user.id)+'_1.png',dpi=300,format='png')
              
              if len(slider2)>0:
                 slider2_hist,bin_edges_2 = numpy.histogram(slider2_rating,bins,normed=False)              
                 slider2_hist_in_percent=(100*slider2_hist/float(sum(slider2_hist)))[::-1]
                 plt.figure()
                 fig2, ax2=plt.subplots()
                 rects2 = ax2.bar(ind, slider2_hist_in_percent, width, color='r')
                 median2=numpy.median(slider2_rating)
                 median_bar2=median_index(request,median2)
                 rects2[median_bar2].set_color('b')
                 ax2.set_ylabel('Percentages (%)')
                 ax2.set_title("How would you rate the State of California on this issue today?")
                 ax2.set_xticks(ind+width/2)
                 ax2.set_xticklabels( ('A+', 'A', 'A-', 'B+', 'B','B-','C+','C','C-','D+','D','D-','F') )
                 plt.savefig(str(cur_user.id)+'_2.png',dpi=300,format='png')

def neighbor_stat(request):
    zipcode=request.REQUEST.get('zipcode',-1)
    statements = OpinionSpaceStatement.objects.all().order_by('id')
    if zipcode!=-1:
       city=ZipCode.objects.filter(code__exact=zipcode)[0].city
       zipcode_in_city=ZipCode.objects.filter(city__exact=city)
       neighbors=[]

       for s in statements:
          s_grade=[]
          for i in range(0, len(zipcode_in_city)):
             log=ZipCodeLog.objects.filter(location__exact=zipcode_in_city[i])

             for j in range(0, len(log)):
                user_grade_s=log[j].user.userrating_set.filter(opinion_space_statement=s,is_current=True)
                if len(user_grade_s)>0:
                  s_grade.append(user_grade_s[0].rating)
          neighbors.append({'statement':s.statement,'avgG':score_to_grade(100*numpy.median(s_grade)),'avg': int((1-numpy.median(s_grade))*300)})
       return neighbors
    else:
       return None

def neighbor_city(request):
    zipcode=request.REQUEST.get('zipcode',-1)
    if zipcode!=-1:
       city=ZipCode.objects.filter(code__exact=zipcode)[0].city
       return city
    else:
       return None

def participant_stat(request):
    uid = request.GET.get('username',-1)
    auth = False
    os = get_os(1)
    disc_stmt = get_disc_stmt(os, 1)
    participant_rating={}
    participant_rating['s1_avg']='NA'
    participant_rating['s2_avg']='NA'
    if uid != -1:
        cur_user = User.objects.filter(id=uid)
        if len(cur_user) > 0:
            cur_user = cur_user[0]
            auth = True
            cur_user_comment=DiscussionComment.objects.filter(user=cur_user,discussion_statement= disc_stmt,is_current = True)
            if len(cur_user_comment)>0:
               participant_rating['comment']=cur_user_comment[0].comment
               participant_rating['date']=cur_user_comment[0].created
               slider1=CommentAgreement.objects.filter(comment=cur_user_comment[0])
               slider2=CommentRating.objects.filter(comment=cur_user_comment[0])
               slider1_rating=[]
               slider2_rating=[]


               for i in range(0, len(slider1)):
                   slider1_rating.append(slider1[i].agreement)
               for i in range(0, len(slider2)):
                   slider2_rating.append(slider2[i].rating)


               participant_rating['s1_rating']=slider1_rating
               participant_rating['s2_rating']=slider2_rating
               return participant_rating
            else:
               return participant_rating
        else:
            return participant_rating
    else:
      return participant_rating

def number_to_ordinal(num):
    ordinal='th'
    if num % 10 == 1:
       ordinal='st'
    elif num % 10 == 2:
       ordinal='nd'
    elif num % 10 ==3:
       ordinal='rd'

    if num % 100 == 11:
        ordinal='th'
    if num % 100 == 12:
        ordinal='th'
    if num % 100 == 13:
        ordinal='th'

    return ordinal
