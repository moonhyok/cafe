#!/usr/bin/env python
import environ
import string
import array
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.dateformat import DateFormat
from opinion.includes.queryutils import *
import numpy
import random
import matplotlib.pyplot as plt

"""
users = User.objects.all()
buckets = []

for u in users:
    ratings = CommentRating.objects.filter(rater = u, is_current= True).order_by('created')
    prev = None
    flag = False
    
    for r in ratings:
        if not prev == None:
            diff = r.created - prev.created
            if diff < datetime.timedelta(seconds = 20) and not r.comment.user == prev.comment.user:
                flag = True
                print diff
                break
        prev = r
        
    if not flag:
        good_ratings = CommentAgreement.objects.filter(rater = u, is_current = True)
        for g in good_ratings:
            buckets.append(g.agreement) 
            print g.agreement
plt.hist(buckets,10)
plt.show()

comments = DiscussionComment.objects.all()
for c in comments:
    ratings_array = []
    ratings = CommentRating.objects.filter(comment = c, is_current = True)
    for r in ratings:
        ratings_array.append(r.rating)
    if len(ratings) > 10:
        print numpy.std(ratings_array)/sqrt(len(ratings_array))

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
    se = numpy.std(time_sum_array)/sqrt(len(time_sum_array))
    if valid_ratings > 20:
        x.append((time_sum/valid_ratings).seconds + (time_sum/valid_ratings).microseconds/1E6)
        y.append(len(comment.comment))
        print comment.id, valid_ratings,(time_sum/valid_ratings), se
plt.xlabel('Rating Time (s)')
plt.ylabel('Length of Comment (in chars)')
plt.title('Avg. Rater Time vs. Comment Length\n(>20 ratings)')
plt.xlim(0,60)
plt.ylim(0,1000)
plt.scatter(x,y)
plt.show()

x = []
y = []
for i in range(1,20):
    userid = random.randint(3,2106)
    print userid
    comments = DiscussionComment.objects.all()
    user = User.objects.filter(id = userid)[0]
    for comment in comments:
        time_sum = datetime.timedelta(seconds = 0)
        valid_ratings = 0
        ratings = CommentRating.objects.filter(comment = comment, rater = user, is_current = True)
        time_sum_array = []
        for rating in ratings:
            comment_views = LogCommentView.objects.filter(comment = comment, logger_id = rating.rater.id).order_by('created')
            if len(comment_views) > 0:
                first_view = comment_views[0]
                diff = rating.created - first_view.created
                if diff < datetime.timedelta(seconds = 60):
                    x.append(diff.seconds + diff.microseconds / 1E6)
                    y.append(len(comment.comment))

plt.xlabel('Rating Time (s)')
plt.ylabel('Length of Comment (in chars)')
plt.title('Rating Time vs. Comment Length\nFor 20 Random Users')
plt.xlim(0,60)
plt.ylim(0,1000)
plt.scatter(x,y)
plt.show()"""


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
    if valid_ratings > 20:
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
    
plt.bar(x,user_tally)
plt.xlabel('Database User Id')
plt.ylabel('# of Ratings quicker by 1.5 std-devs')
plt.title('Number of fast ratings for each OS-GM user')
plt.show()

