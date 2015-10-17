import sys, os
import opinion.scripts.environ
from opinion.opinion_core.models import *
from django.contrib.auth.models import User

import numpy as np
#from matplotlib import pyplot as plt
import itertools, datetime
import pickle
import datetime

import string
import array
from django.core.mail import send_mail
from django.utils.dateformat import DateFormat
from opinion.includes.queryutils import *



def find_seconds(td):
	return float(td.days*24*3600 + td.seconds)

class Plotter:
    FIGSIZE = (7,7)
    
    def __init__(self, path):
        self.path = path
        try:
            f = open(self.path + "dirs.pkl")
            self.dirpaths = pickle.load(f)
        except IOError:
            self.dirpaths = {}

        try:
            f = open(self.path + "stats.pkl")
            self.stats = pickle.load(f)
        except IOError:
            self.stats = {}

    def start_plot(self, startDate, path_segment, name, endDate = datetime.datetime.now(), custom=False):
        
        self.startDate = startDate
        self.endDate = endDate

        self.custom = custom

        if not custom:
                self.dirpaths[name] = path_segment
        self.current_plot = path_segment
        self.stats[self.current_plot]={}
        try:
            os.mkdir(self.path+path_segment)
        except:
            for file in os.listdir(self.path+path_segment):
                os.remove(self.path+path_segment+"/"+file)

    def save_plot(self, fig, name):
        fig.savefig(self.path+self.current_plot+"/"+name+".png")

    def add_stats(self, name, data):
        self.stats[self.current_plot][name] = data
        
    def pickle_data(self):
        if not self.custom:
                self.stats['date_created'] = str(datetime.datetime.today())
        pickle.dump(self.dirpaths, open(self.path+"dirs.pkl", "w"))
        pickle.dump(self.stats, open(self.path+"stats.pkl", "w"))

    def comments_histogram(self):

        rate_count = []
        view_count = []

        for u in User.objects.all():
            for dis in DiscussionComment.objects.filter(created__gte=self.startDate, created__lte=self.endDate).filter(user=u):
                k = CommentRating.objects.filter(comment=dis).count()
                if (k < 150):
                    rate_count.append(k)
                i = LogCommentView.objects.filter(comment=dis).count()
                if (i < 150):
                    view_count.append(i)

        fig1 = plt.figure(figsize=self.FIGSIZE)
        view = fig1.add_subplot(211)
        view.hist(view_count, 50)
        view.set_xlabel('# of Times Viewed')
        view.set_ylabel('Count')
        rate = fig1.add_subplot(212)
        rate.hist(rate_count, 50)
        rate.set_xlabel('# of Times Rated')
        rate.set_ylabel('Count')
        self.save_plot(fig1, "comment_histograms")

        ratecount={'Mean # of ratings':np.round(np.mean(rate_count),2),
                   'StdDev for # of ratings ':np.round(np.std(rate_count),2),
                   'Median for# of Ratinds':np.median(rate_count),
                   'Mean # of views':np.round(np.mean(view_count),2),
                   'StdDev for # of views':np.round(np.std(view_count),2),
                   'Median for # of views':np.median(view_count)}


        self.add_stats("commenthistograms", ratecount)


    def session_plots(self):
        idle_duration = datetime.timedelta(minutes=15)
        visit_gap = datetime.timedelta(hours=1)
        minimum_session_length = 1 #datetime.timedelta(minutes=1
        maximum_no_visit_length = 15
        events = [5, 6, 7] #session-worthy events

        avg_session_length = []
        avg_session_gap = []
        user_visit_counts = []
        session_count=[]

        for u in User.objects.all():
                id_lst = [u.id]
                for v in Visitor.objects.filter(user=u):
                        id_lst.append(v.id)
                log = list(LogUserEvents.objects.filter(created__gte=self.startDate, created__lte=self.endDate)\
                .filter(logger_id__in=id_lst, log_type__in=events).order_by('created') )
                if len(log) < 2:
                        continue

                session_last_log_date= log[0].created
                session_end_at_end_of_log = False
                session_duration = []
                session_gap = []

                visit_count = 0

                for i in range(0, len(log)-1):
                        diff = log[i+1].created - log[i].created
                        if (diff > idle_duration):
                                if(i == len(log)-2):
                                        session_at_end_of_log = True
                                mins = find_seconds((log[i].created - session_last_log_date)) / 60
                                if mins > minimum_session_length and mins < 60*5:
                                        session_duration.append(mins)
                                        next_session_start = log[i+1].created
                                        session_last_log_date = next_session_start
                                        days = find_seconds(diff)/(24*3600)
                                        session_gap.append(days)
                                        if(diff > visit_gap):
                                                visit_count = visit_count + 1

                if not session_end_at_end_of_log:
                                mins = find_seconds((log[-1].created - session_last_log_date)) / 60
                                if mins > minimum_session_length and mins < 60*5:
                                        session_duration.append(mins)

                if session_duration:
                        session_count.append(len(session_duration))
                        m = np.mean(session_duration)
                        avg_session_length.append(m)

                if session_gap:
                        avg_session_gap.append(np.mean(session_gap))

                if visit_count:
                        user_visit_counts.append(visit_count)


        fig2 = plt.figure(figsize=self.FIGSIZE)
        whole = fig2.add_subplot(211)
        whole.hist(avg_session_length, 30)
        whole.set_xlabel('Average Session Duration (minutes) 0 < min < 300')
        whole.set_ylabel('Count')
        part = fig2.add_subplot(212)
        part.hist(filter(lambda x: x < 60, avg_session_length), 30)
        part.set_xlabel('Average Session Duration (minutes) 0 < min < 60')
        part.set_ylabel('Count')
        self.save_plot(fig2, "session_duration")

        sessionlength={'Mean session duration':np.round(np.mean(filter(lambda x: x < 60, avg_session_length)),2),
                       'StvDev of session duration':np.round(np.std(filter(lambda x: x < 60, avg_session_length)),2),
                       'Median of session duration':np.median(filter(lambda x: x < 60, avg_session_length))}

        self.add_stats("sessionlength", sessionlength)


        fig3 = plt.figure(figsize=self.FIGSIZE)
        p = fig3.add_subplot(211)
        p.hist(avg_session_gap, 50)
        p.set_xlabel('Average Gap Between Sessions (days)')
        p.set_ylabel('Count')
        p2 = fig3.add_subplot(212)
        p2.hist(filter(lambda x: x < 7, avg_session_gap), 50)
        p2.set_xlabel('Average Gap Between Sessions for Frequent Users (days) 0 < days < 7')
        p2.set_ylabel('Count')
        self.save_plot(fig3, "session_gap")

        sessiongap={'Mean session gap':np.round(np.mean(avg_session_gap),2),
                    'StdDev of session gap':np.round(np.std(avg_session_gap),2),
                    'Median of session gap':np.round(np.median(avg_session_gap),2)}

        self.add_stats("sessiongap", sessiongap)


        fig4 = plt.figure(figsize=self.FIGSIZE)
        p = fig4.add_subplot(211)
        p.hist(session_count, 50)
        p.set_xlabel('# of Sessions')
        p.set_ylabel('Count')
        p2 = fig4.add_subplot(212)
        p2.hist(filter(lambda x: x < 20, session_count), 20)
        p2.set_xlabel('# of Sessions 0 < sessions < 20')
        p2.set_ylabel('Count')
        self.save_plot(fig4, "session_count")

        sessioncount={'Mean of # of sessions':np.round(np.mean(session_count),2),
                    'StdDev of # of sessions':np.round(np.std(session_count),2),
                    'Median of # of sessions':np.median(session_count)}

        self.add_stats("sessioncount", sessioncount)


    def comments_returned(self):
        disp = {}

        for l in LogCommentsReturned.objects.filter(created__gte=self.startDate, created__lte=self.endDate, query_type=LogCommentsReturned.unrated):
                comments = l.comments_list.split()
                for c in comments:
                        if c in disp:
                                disp[c] += 1
                        else:
                                disp[c] = 1

        x = []
        y = []

        for k in disp.keys():
                x.append(int(k))
                y.append(int(disp[k]))


        fig5 = plt.figure(figsize=self.FIGSIZE)
        p = fig5.add_subplot(211)
        p.plot(x, y, 'ro')
        p.set_xlabel('Comment ID')
        p.set_ylabel('# of Times Returned')
        p2 = fig5.add_subplot(212)
        p2.plot(x, y, 'ro')
        p2.axis([0, max(x)*0.8, 0, max(y)*0.8])
        p2.set_xlabel('Comment ID')
        p2.set_ylabel('# of Times Returned, zoomed in')
        self.save_plot(fig5, "comments_returned")


    def sessions_per_day(self):
        x = []
        y = []
        y2 = []

        oneDay = datetime.timedelta(days=1)

        start = self.startDate.date()
        end = start + oneDay

        idle_duration = datetime.timedelta(minutes=15)
        session_at_end_of_log = False

        loop = True
        xcoord = 0

        while loop:
                log = list(LogUserEvents.objects.filter(created__gte=start, created__lte=end).order_by('created'))
                session_count = 0
                for i in range(0, len(log)-1):
                        diff = log[i+1].created - log[i].created
                        if (diff > idle_duration):
                                if(i == len(log)-2):
                                        session_at_end_of_log = True
                                session_count += 1
                y.append(session_count)
                x.append(xcoord)
                y2.append(CommentRating.objects.filter(created__gte=start, created__lte=end).count())
                xcoord += 1
                start += oneDay
                end += oneDay
                if start > self.endDate.date():
                        loop = False


        fig6 = plt.figure(figsize=self.FIGSIZE)
        p = fig6.add_subplot(211)
        p.bar(x, y)
        p.set_xlabel('Days Since Start Date')
        p.set_ylabel('# of Sessions')
        p2 = fig6.add_subplot(212)
        p2.bar(x, y2)
        p2.set_xlabel('Days Since Start Date')
        p2.set_ylabel('# of Ratings')
        self.save_plot(fig6, "sessions_per_day")

        y = filter(lambda x: x>0, y)
        y2 = filter(lambda x: x>0, y2)

        sessionsPerDay={'Mean # of sessions per day':np.round(np.mean(y), 2),
                    'StdDev for # of sessions per day':np.round(np.std(y), 2),
                    'Median for # of sessions per day':np.median(y),
                        'Mean of # of ratings per day': np.mean(y2),
                        'StdDev for # of ratings per day': np.std(y2),
                        'Median for # of ratings per day': np.median(y2)}


        self.add_stats("sessionsPerDay", sessionsPerDay)

    def create_plots(self):
        self.comments_returned()
        self.comments_histogram()
        self.session_plots()
        self.sessions_per_day()
        self.pickle_data()
