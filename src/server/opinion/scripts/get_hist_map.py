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

def geostats():
    """produce geojson file for leaflet"""
    geo_json=open('/var/www/latest-version/src/server/opinion/geo.json')
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
             	if log[k].user.is_active:
                   user_grade_s=log[k].user.userrating_set.filter(opinion_space_statement=s,is_current=True)
                   if len(user_grade_s)>0:
                      s_grade.append(user_grade_s[0].rating)
          if len(s_grade)==0:
             geo_data['features'][i]['properties']["s"+str(s.id)]=10  #for leaflet to show NA color
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
            	if log[k].user.is_active:
                   user_grade_s=log[k].user.userrating_set.filter(opinion_space_statement=s,is_current=True)
                   if len(user_grade_s)>0:
                      s_grade.append(user_grade_s[0].rating)

        if len(s_grade)==0:
            geo_data['features'][len(geo_data['features'])-1]['properties']["s"+str(s.id)]=10
            geo_data['features'][len(geo_data['features'])-1]['properties']['PARTICIPANTS']=0
        if len(s_grade)>0:
            geo_data['features'][len(geo_data['features'])-1]['properties']["s"+str(s.id)]=numpy.median(s_grade)
            geo_data['features'][len(geo_data['features'])-1]['properties']['PARTICIPANTS']=len(s_grade)

    with open(jspath+'geostat.js', 'w') as outfile:
         outfile.write('var geostat=')
         json.dump(geo_data, outfile)
         outfile.write(';')

def issues_hist():
   """produce histogram for each issue"""
   statements = OpinionSpaceStatement.objects.all().order_by('id')
   bins=[0,0.01,0.19,0.32,0.38,0.44,0.56,0.63,0.69,0.81,0.86,0.92,0.99,1]  
        # F    D-   D    D+   C-   C    C+   B-   B   B+    A-   A    A+
   N=len(bins)-1
   ind=numpy.arange(N)
   width=0.5
   
   for s in statements:
       s_rating=UserRating.objects.filter(opinion_space_statement=s,is_current=True)
       s_rating_list=[]
       for rating in s_rating:
       	  if rating.user.is_active:
             s_rating_list.append(1-rating.rating)
       
       if len(s_rating_list)>0:
          hist,bin_edges = numpy.histogram(s_rating_list,bins,normed=False)
          hist_in_percent=(100*hist/float(sum(hist)))[::-1]
          #overcome xscale issue in pyplot 
          if hist_in_percent[0]==0:
             hist_in_percent[0]=0.001
          if hist_in_percent[len(hist_in_percent)-1]==0:
             hist_in_percent[len(hist_in_percent)-1]=0.001
          fig, ax = plt.subplots()
          rects1 = ax.bar(ind, hist_in_percent, width, facecolor='#74b9b7', 
          align='center',edgecolor = "none")
          fig.patch.set_facecolor('#74b9b7')
          ax.patch.set_facecolor('#f5ebde')
          median=numpy.median(s_rating_list)
          median_bar=median_index(median)
          rects1[median_bar].set_color('#4f300b')
          ax.set_xticks(ind)
          for i in plt.gca().get_xticklabels():
             i.set_color("#4f300b")
          for i in plt.gca().get_yticklabels():
             i.set_color("#4f300b")
          plt.figtext(.91,.31,"PERCENTAGE(%)",family='sans-serif',color="#4f300b",rotation='vertical')
          ax.set_xticklabels( ('A+', 'A', 'A-', 'B+', 'B','B-','C+','C','C-','D+','D','D-','F') )
          fig.set_size_inches(5,5)
          plt.savefig(imagepath+s.statement+'.png',facecolor=fig.get_facecolor(),edgecolor='none',dpi=100,format='png')

def median_index(median):
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


def participant_slider1_hist():
    """produce histogram for all participant above level 8"""
    
    
    os = get_os(1)
    disc_stmt = get_disc_stmt(os, 1)
    
    bins=[0,0.01,0.19,0.32,0.38,0.44,0.56,0.63,0.69,0.81,0.86,0.92,0.99,1]  
        # F    D-   D    D+   C-   C    C+   B-   B   B+    A-   A    A+
    N=len(bins)-1
    ind=numpy.arange(N)
    width=0.5
    alluser=User.objects.all()
   
    for cur_user in alluser:
           cur_user_comment=DiscussionComment.objects.filter(user=cur_user,discussion_statement= disc_stmt,is_current = True)
           if len(cur_user_comment)>0:
              slider1=CommentAgreement.objects.filter(comment=cur_user_comment[0])
              slider1_rating=[]
               
              for i in range(0, len(slider1)):
              	 if slider1[i].rater.is_active:
                    slider1_rating.append(1-slider1[i].agreement)
              #produce png only if len(slider) >0
              if len(slider1_rating)>0:
                 slider1_hist,bin_edges_1 = numpy.histogram(slider1_rating,bins,normed=False)
                 slider1_hist_in_percent=(100*slider1_hist/float(sum(slider1_hist)))[::-1]
                 #overcome xscale issue in pyplot 
                 if slider1_hist_in_percent[0]==0:
                    slider1_hist_in_percent[0]=0.001
                 if slider1_hist_in_percent[len(slider1_hist_in_percent)-1]==0:
                    slider1_hist_in_percent[len(slider1_hist_in_percent)-1]=0.001
                 fig1, ax1=plt.subplots()


                 rects1 = ax1.bar(ind, slider1_hist_in_percent, width, facecolor='#74b9b7', 
                 align='center',edgecolor = "none")
                 fig1.patch.set_facecolor('#74b9b7')
                 ax1.patch.set_facecolor('#f5ebde')
                 
                 median1=numpy.median(slider1_rating)
                 median_bar1=median_index(median1)
                 rects1[median_bar1].set_color('#4f300b')
                 ax1.set_xticks(ind)
                 for i in plt.gca().get_xticklabels():
                    i.set_color("#4f300b")
                 for i in plt.gca().get_yticklabels():
                    i.set_color("#4f300b")
                 plt.figtext(.91,.31,"PERCENTAGE(%)",family='sans-serif',color="#4f300b",rotation='vertical')
                 ax1.set_xticklabels( ('A+', 'A', 'A-', 'B+', 'B','B-','C+','C','C-','D+','D','D-','F') )
                 fig1.set_size_inches(5,5)
                 plt.savefig(imagepath+str(cur_user.id)+'_1.png',facecolor=fig1.get_facecolor(),edgecolor='none',dpi=100,format='png')
              
          

def participant_slider2_hist():
    os = get_os(1)
    disc_stmt = get_disc_stmt(os, 1)
    
    bins=[0,0.01,0.19,0.32,0.38,0.44,0.56,0.63,0.69,0.81,0.86,0.92,0.99,1]  
        # F    D-   D    D+   C-   C    C+   B-   B   B+    A-   A    A+
    N=len(bins)-1
    ind=range(N)
	
    alluser=User.objects.filter(is_active = True)
   
    for cur_user in alluser:
           cur_user_comment=DiscussionComment.objects.filter(user=cur_user,discussion_statement= disc_stmt,is_current = True)
           if len(cur_user_comment)>0:           
              slider2=CommentRating.objects.filter(comment=cur_user_comment[0])
              slider2_rating=[]
               
              for i in range(0, len(slider2)):
              	 if slider2[i].rater.is_active:
                    slider2_rating.append(1-slider2[i].rating)
              #produce png only if len(slider) >0
              
              if len(slider2_rating)>0:
                 slider2_hist,bin_edges_2 = numpy.histogram(slider2_rating,bins,normed=False)              
                 slider2_hist_in_percent=(100*slider2_hist/float(sum(slider2_hist)))[::-1]
                 #overcome xscale issue in pyplot 
                 if slider2_hist_in_percent[0]==0:
                    slider2_hist_in_percent[0]=0.001
                 if slider2_hist_in_percent[len(slider2_hist_in_percent)-1]==0:
                    slider2_hist_in_percent[len(slider2_hist_in_percent)-1]=0.001
                 plt.figure()
                 fig2, ax2=plt.subplots()
                 rects2 = ax2.bar(ind, slider2_hist_in_percent, width=0.5, facecolor='#74b9b7', 
                 align='center',edgecolor = "none")
                 fig2.patch.set_facecolor('#74b9b7')
                 ax2.patch.set_facecolor('#f5ebde')
                 median2=numpy.median(slider2_rating)
                 median_bar2=median_index(median2)
                 rects2[median_bar2].set_color('#4f300b')
                 for i in plt.gca().get_xticklabels():
                    i.set_color("#4f300b")
                 for i in plt.gca().get_yticklabels():
                    i.set_color("#4f300b")
                 plt.figtext(.91,.31,"PERCENTAGE(%)",family='sans-serif',color="#4f300b",rotation='vertical')
                 ax2.set_xticks(ind)
                 ax2.set_xticklabels( ('A+', 'A', 'A-', 'B+', 'B','B-','C+','C','C-','D+','D','D-','F') )
                 fig2.set_size_inches(5,5)
                 plt.savefig(imagepath+str(cur_user.id)+'_2.png',facecolor=fig2.get_facecolor(),edgecolor='none',dpi=100,format='png')

geostats()
participant_slider1_hist()
participant_slider2_hist()
issues_hist()
