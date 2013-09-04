#!/usr/bin/env python
import sys, os
import environ
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from opinion.settings_local import ASSETS_LOCAL

import numpy as np
from matplotlib import pyplot as plt
import itertools, datetime
import pickle

import string
import array
from django.core.mail import send_mail
from django.utils.dateformat import DateFormat
from opinion.includes.queryutils import *

from opinion.includes.plotutils import *

FIGSIZE=(7,7)
s=ASSETS_LOCAL+'statistics/'

comments = DiscussionComment.objects.all()
x = []
y = []
user_tally = [0]*2107
for comment in comments:
    time_sum = datetime.timedelta(seconds = 0)
    valid_ratings = 0
    ratings = CommentRating.objects.filter(comment = comment, is_current = True)
    time_sum_array = array.array('f')
    rater_array = []
    for rating in ratings:
        comment_views = LogCommentView.objects.filter(comment = comment, logger_id = rating.rater.id).order_by('created')
        if len(comment_views) > 0:
            first_view = comment_views[0]
            diff = rating.created - first_view.created
            if diff < datetime.timedelta(seconds = 60):
                time_sum = time_sum + diff
                valid_ratings = valid_ratings + 1
                time_sum_array.append(diff.seconds)
                rater_array.append(rating.rater)
    se = numpy.std(time_sum_array)/sqrt(len(time_sum_array))
    thresh_std = numpy.std(time_sum_array)*1.5
    if valid_ratings > 0:
        thresh = numpy.mean(time_sum_array)-thresh_std
        i = 0
        for t in time_sum_array:
            if t < thresh:
                user_tally[rater_array[i].id] = user_tally[rater_array[i].id] + 1
                print comment.id, rater_array[i].id, t, thresh
            i = i + 1
        #y.append(len(comment.comment)+0.0)
j = 0
for u in user_tally:
    x.append(j)
    if u > 10:
        print "participant" + str(j-2) + " is suspected of malicious behavior since " + str(u) + " of their ratings were 1.5 standard deviations quicker than the mean rating time" 
    j = j + 1

fig7 = plt.figure(figsize=FIGSIZE)
p = fig7.add_subplot(111)
p.bar(x,user_tally)
p.set_xlabel('Database User Id')
p.set_ylabel('# of Ratings quicker by 1.5 std-devs')
p.set_title('Number of fast ratings for each OS-Beta2.1.0 user')
fig7.savefig(s+"/fastratings.png")

comments = DiscussionComment.objects.all()
x = array.array('f')
y = array.array('f')
for comment in comments:
    time_sum = datetime.timedelta(seconds = 0)
    valid_ratings = 0
    ratings = CommentRating.objects.filter(comment = comment, is_current = True)
    time_sum_array = []
    for rating in ratings:
        comment_views = LogCommentView.objects.filter(comment = comment, logger_id = rating.rater.id).order_by('created')
        if len(comment_views) > 0:
            first_view = comment_views[0]
            diff = rating.created - first_view.created
            if diff < datetime.timedelta(seconds = 60):
                time_sum = time_sum + diff
                valid_ratings = valid_ratings + 1
                time_sum_array.append(diff.seconds + diff.microseconds / 1E6)

    if valid_ratings > 0:
        se = numpy.std(time_sum_array)/sqrt(len(time_sum_array))
        x.append((time_sum/valid_ratings).seconds + (time_sum/valid_ratings).microseconds/1E6)
        y.append(len(comment.comment))
        print comment.id, valid_ratings,(time_sum/valid_ratings), se

fig8 = plt.figure(figsize=FIGSIZE)
p = fig8.add_subplot(111)
p.set_xlabel('Rating Time (s)')
p.set_ylabel('Length of Comment (in chars)')
p.set_title('Rating Time vs. Comment Length')
p.axis([0,60,0,1000])
p.scatter(x,y)
fig8.savefig(s+"/ratingtime_commentlength.png")

