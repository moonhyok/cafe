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
import csv

def geostats():
    """produce geojson file for leaflet"""
    f=open(imagepath+'geotest.txt','w')
    geo_json=open('/var/www/latest-version/src/server/opinion/geo.json')
    #geo_json=open('geo.json')
    geo_data=json.load(geo_json)
    skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)
    statements = OpinionSpaceStatement.objects.all().order_by('id')
    ofile  = open(settings.MEDIA_ROOT + "/mobile/js/"+"ca_capita_carto.csv", "wb")
    writer=csv.writer(ofile,delimiter=',')
    writer.writerow(['COUNTY','POPULATION','COLOR'])
    for s in statements:
       issue_ofile=open(settings.MEDIA_ROOT + "/mobile/js/"+"ca_issue"+str(s.id)+"_carto.csv", "wb")
       writer_issue=csv.writer(issue_ofile,delimiter=',')
       writer_issue.writerow(['COUNTY','POPULATION','COLOR'])
       skip_ca=0
       for i in range(0,len(geo_data['features'])-1):
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
          if(s.id==1):
             ratio=10000*float(len(s_grade)+s_skip)/geo_data['features'][i]['properties']['Population']
             writer.writerow([geo_data['features'][i]['properties']['NAME']+" County",geo_data['features'][i]['properties']['Population'],capita_color(ratio)])
       
          if len(s_grade)==0:
             writer_issue.writerow([geo_data['features'][i]['properties']['NAME']+" County",geo_data['features'][i]['properties']['Population'],'13'])
          else:
             writer_issue.writerow([geo_data['features'][i]['properties']['NAME']+" County",geo_data['features'][i]['properties']['Population'],issue_color(1-numpy.median(s_grade))])
          if len(s_grade)+s_skip==0:
             geo_data['features'][i]['properties']["s"+str(s.id)]=10  #for leaflet to show NA color
             geo_data['features'][i]['properties']['PARTICIPANTS']=0
          if len(s_grade)+s_skip>0:
             geo_data['features'][i]['properties']['PARTICIPANTS']=len(s_grade)+s_skip
             if len(s_grade)>0:
                geo_data['features'][i]['properties']["s"+str(s.id)]=numpy.median(s_grade)
             else:
                geo_data['features'][i]['properties']["s"+str(s.id)]=10
				 
       f.write("skip ca user:"+str(skip_ca)+'\n')

    #find median for non ca zipcode
    '''zipcode_nonca=ZipCode.objects.exclude(state='CA')
    for s in statements:
        s_grade=[]
        s_skip=0
        for j in range(0, len(zipcode_nonca)):
            log=ZipCodeLog.objects.filter(location__exact=zipcode_nonca[j])
            for k in range(0, len(log)):
            	if log[k].user.is_active:
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
        
        f.write("skip non ca user:"+str(s_skip)+'\n')
        if len(s_grade)+s_skip==0:
            geo_data['features'][len(geo_data['features'])-1]['properties']["s"+str(s.id)]=10
            geo_data['features'][len(geo_data['features'])-1]['properties']['PARTICIPANTS']=0
        if len(s_grade)+s_skip>0:
            geo_data['features'][len(geo_data['features'])-1]['properties']['PARTICIPANTS']=len(s_grade)+s_skip
            if len(s_grade)>0:
                geo_data['features'][len(geo_data['features'])-1]['properties']["s"+str(s.id)]=numpy.median(s_grade)
            else:
                geo_data['features'][len(geo_data['features'])-1]['properties']["s"+str(s.id)]=10

    with open(jspath+'geostat.js', 'w') as outfile:
         outfile.write('var geostat=')
         json.dump(geo_data, outfile)
         outfile.write(';')'''
         
def issues_hist():
   """produce histogram for each issue"""
   statements = OpinionSpaceStatement.objects.all().order_by('id')
   #bins=[0,0.01,0.19,0.32,0.38,0.44,0.56,0.63,0.69,0.81,0.86,0.92,0.99,1]
   bins=[0,0.001,0.08,0.14,0.19,0.31,0.37,0.44,0.56,0.62,0.68,0.81,0.999,1]  
        #A+   A   A-   B+   B    B-   C+   C    C-   D+   D    D-    F
   N=len(bins)# include "skip"
   ind=numpy.arange(N)
   width=0.5
   
   f=open(imagepath+'skiptest.txt','w')
   
   active_users = list(User.objects.filter(is_active=True)) 
   skip_begin_date=datetime.datetime(2014,1,9,0,0,0,0)
   for s in statements:
       activeuser=0
       user_no_visitor=0
       s_rating=UserRating.objects.filter(opinion_space_statement=s,is_current=True,user__in = active_users)
       s_rating_list=[]
       s_skip=0
       slogskip_0=0
       for rating in s_rating:
          if rating.created>=skip_begin_date:
       	        activeuser=activeuser+1
                visitor=Visitor.objects.filter(user=rating.user)  #get the visitor of the user
                if len(visitor)>0:
                   s_log_skip=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11,details__contains='skip').filter(details__contains=str(s.id)).order_by('-created') #get issue skip log
                   s_log_rating=LogUserEvents.objects.filter(is_visitor=True, logger_id=visitor[0].id,log_type=11).exclude(details__contains='skip').filter(details__startswith='slider_set '+str(s.id)).order_by('-created')
                   if len(s_log_skip)==0: #no skip
                      slogskip_0=slogskip_0+1
                      if len(s_log_rating)>0:
                         s_rating_list.append(rating.rating)
                      else: #not click on skip, not move slider s, => skip
                         s_skip=s_skip+1
                   else:
                      if len(s_log_rating)==0:  #click skip, not move slider s => skip
                         s_skip=s_skip+1
                      else:
                         if s_log_skip[0].created>s_log_rating[0].created: #final decision is skip
                            s_skip=s_skip+1
                         else:
                            s_rating_list.append(rating.rating)
                else: 
                   s_rating_list.append(rating.rating)
          else:
                activeuser=activeuser+1
                s_rating_list.append(rating.rating)
       f.write("active_user:"+str(activeuser)+'\n')
       f.write("active rating user:"+str(len(s_rating_list))+'\n')
       f.write("skip user:"+str(s_skip)+'\n')
       
       ratings = UserRating.objects.filter(is_current=True,opinion_space_statement = s, user__in = active_users)
       skip_logs = LogUserEvents.objects.filter(is_visitor=True, log_type=11,details__contains='slider_set',created__gte = skip_begin_date)
       users_with_grades = []
       for skip_log in skip_logs:
         slider_set_args = skip_log.details[10:].lstrip()
         visitor = Visitor.objects.filter(id = skip_log.logger_id)
         if len(visitor) > 0:
           visitor = visitor[0]
           if visitor.user != None and visitor.user.is_active and int(slider_set_args[0]) == s.id:
             users_with_grades.append(visitor.user)
       
       
       if len(s_rating_list)>0:
          hist,bin_edges = numpy.histogram(s_rating_list,bins,normed=False)
          skip=numpy.array([s_skip])
          hist=numpy.concatenate((hist,skip), axis=1)
          hist_in_percent=(100*hist/float(sum(hist)))
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
          f.write(str(s.id))
          f.write(str(median)+'\n')
          median_bar=median_index(1-median)
          rects1[median_bar].set_color('#4f300b')
          rects1[13].set_color('#0b294f')
          ax.set_xticks(ind)
          for i in plt.gca().get_xticklabels():
             i.set_color("#4f300b")
          for i in plt.gca().get_yticklabels():
             i.set_color("#4f300b")
          plt.figtext(.91,.31,"PERCENTAGE(%)",family='sans-serif',color="#4f300b",rotation='vertical')
          ax.set_xticklabels( ('A+', 'A', 'A-', 'B+', 'B','B-','C+','C','C-','D+','D','D-','F','Skip') )
          plt.setp(ax.get_xticklabels(), fontsize=10)
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

def issue_color(median):
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
    if median<=0.01 and median>=0:
        return 12




def capita_color(ratio):
    #["0", "0.01-0.02", "0.021-0.05", "0.51-0.1", "0.11-0.2","0.21-0.5","0.51-1","1.01-2","2.01-3",">3"];
    if ratio==0:
        return 1;
    elif ratio>0 and ratio<=0.02:
        return 2;
    elif ratio>0.02 and ratio<=0.05:
        return 3;
    elif ratio>0.05 and ratio<=0.1:
        return 4;
    elif ratio>0.1 and ratio<=0.2:
        return 5;
    elif ratio>0.2 and ratio<=0.5:
        return 6;
    elif ratio>0.5 and ratio<=1:
        return 7;
    elif ratio>1 and ratio<=2:
        return 8;
    elif ratio>2 and ratio<=3:
        return 9;
    else:
        return 10;

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
                 if slider1_hist_in_percent[median_bar1]<0.001:
                    if 	slider1_hist_in_percent[median_bar1-1]>0.001: 
                        rects1[median_bar1-1].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1+1]>0.001:
                        rects1[median_bar1+1].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1-2]>0.001: 
                        rects1[median_bar1-2].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1+2]>0.001: 
                        rects1[median_bar1+2].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1-3]>0.001: 
                        rects1[median_bar1-3].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1+3]>0.001: 
                        rects1[median_bar1+3].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1-4]>0.001: 
                        rects1[median_bar1-4].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1+4]>0.001: 
                        rects1[median_bar1+4].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1-5]>0.001: 
                        rects1[median_bar1-5].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1+5]>0.001: 
                        rects1[median_bar1+5].set_color('#4f300b')
                    elif slider1_hist_in_percent[median_bar1-6]>0.001: 
                        rects1[median_bar1-6].set_color('#4f300b')
                    else:
                        rects1[median_bar1+6].set_color('#4f300b')
                 else:    
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
                 if slider2_hist_in_percent[median_bar2]<0.001:
                    if 	slider2_hist_in_percent[median_bar2-1]>0.001: 
                        rects2[median_bar2-1].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2+1]>0.001:
                        rects2[median_bar2+1].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2-2]>0.001: 
                        rects2[median_bar2-2].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2+2]>0.001: 
                        rects2[median_bar2+2].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2-3]>0.001: 
                        rects2[median_bar2-3].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2+3]>0.001: 
                        rects2[median_bar2+3].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2-4]>0.001: 
                        rects2[median_bar2-4].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2+4]>0.001: 
                        rects2[median_bar2+4].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2-5]>0.001: 
                        rects2[median_bar2-5].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2+5]>0.001: 
                        rects2[median_bar2+5].set_color('#4f300b')
                    elif slider2_hist_in_percent[median_bar2-6]>0.001: 
                        rects2[median_bar2-6].set_color('#4f300b')
                    else:
                        rects2[median_bar2+6].set_color('#4f300b')
                 else:    
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

#geostats()
participant_slider1_hist()
participant_slider2_hist()
#issues_hist()
