#!/usr/bin/python
import environ
import numpy
import sys
import pickle

from opinion.settings_local import SUBGROUPS, USER_DATA_KEYS, ASSETS_LOCAL
from opinion.opinion_core.models import *
from django.contrib.auth.models import User

if len(sys.argv) != 2:
    print "Usage: python end_report.py [os_id]"
    exit()

os_id = sys.argv[1]
os = OpinionSpace.objects.filter(id = os_id)[0]

def makeHistogram(user_data):
    histogram = dict()
    for entry in user_data:
        if entry.value in histogram:
            histogram[entry.value]+=1
        else:
            histogram[entry.value]=1
    return histogram
    
#TYPES:
TYPE_QUANTITATIVE = 'quantitative'
TYPE_ORDINAL = 'ordinal'
TYPE_NOMINAL = 'nominal'

# return the sum of all the entries in the dict
# requires counts to be not None
def histogramSum(counts):
    s = 0
    for entry in counts:
        s+=counts[entry]
    return s

# subgroup name mapped to a list of users
subgroups_user_list = {}
subgroups_user_list["All"] = [] # Keep track of all users for aggregate analysis

#iterate through the defined subgroups
for groupname in SUBGROUPS:
    users = User.objects.all()
    definition = SUBGROUPS[groupname]
    for user in users:
        meets_criteria = True
        for key in definition:
            search_result = len(UserData.objects.filter(user = user,key = key, value__in = definition[key]))
            if search_result == 0:
                meets_criteria = False
        if meets_criteria:
            if subgroups_user_list.has_key(groupname):
                subgroups_user_list[groupname].append(user)
            else:
                subgroups_user_list[groupname] = []
                subgroups_user_list[groupname].append(user)
        # Keep track of all users for aggregate analysis			

#iterate through users to for aggregate analysis [cant be placed in subgroups loop in event there are no subgroups defined]
users = User.objects.all()
for user in users:
    subgroups_user_list["All"].append(user) 

author_list = []
dlist = DiscussionComment.objects.filter(is_current = True).exclude(confidence = None).order_by('normalized_score_sum')
for comment in dlist:
    author_list.append(comment.user)
max_size = min(50, len(author_list))
subgroups_user_list["Top 50 Authors: Overall"] = author_list[:max_size]

discussions = DiscussionStatement.objects.all()
for discussion in discussions:
    dlist = DiscussionComment.objects.filter(is_current = True, discussion_statement = discussion).exclude(confidence = None).order_by('normalized_score_sum')
    author_list = []
    for comment in dlist:
        author_list.append(comment.user)
        subgroups_user_list["Top 50 Authors: "+discussion.short_version] = author_list[:min(50, author_list)]

reviewer_list = User.objects.all().order_by('reviewerscore')
max_size = min(50, len(reviewer_list))
subgroups_user_list["Top 50 Reviewers"] = reviewer_list[len(reviewer_list)-max_size:len(reviewer_list)]
subgroups_user_list["Bottom 50 Reviewers"] = reviewer_list[0:max_size]

#maps subgroup names to a dictionary of stats for the subgroup
analytics = {}
for subgroup in subgroups_user_list:
    group = subgroups_user_list[subgroup]
    keygroup = {}
    for key in USER_DATA_KEYS:
        if USER_DATA_KEYS[key]['subgroup_analysis']:
            analytic = {}
            type = USER_DATA_KEYS[key]['type']
            user_data = UserData.objects.filter(user__in = group, key = key)
            analytic['type']=type
            analytic['counts']=makeHistogram(user_data)
            analytic['counts_labels'] = []
            analytic['counts_data'] = []
            for value in USER_DATA_KEYS[key]['possible_values']:
                analytic['counts_labels'].append(value)
                if analytic['counts'].has_key(value):
                    analytic['counts_data'].append(analytic['counts'][value])
                else:
                    analytic['counts_data'].append(0)
            if type == TYPE_QUANTITATIVE:
                values = numpy.array([float(user.value) for user in user_data])
                analytic['median'] = numpy.median(values)
                analytic['std'] = numpy.std(values)
                analytic['mean'] = values.mean()
            elif type == TYPE_ORDINAL:
                counts = analytic['counts']
                target = histogramSum(counts)/2
                total = 0
                for i in USER_DATA_KEYS[key]['possible_values']:
                    curValue = i
                    if curValue in counts:
                        total += counts[curValue]
                    if total > target:
                        analytic['median'] = curValue
                        break
            keygroup[key] = analytic
    #statements 
    statements = OpinionSpaceStatement.objects.distinct().filter(opinion_space = os)
    for statement in statements:
        ratings_objects = UserRating.objects.filter(is_current = True, opinion_space = os, user__in = group, opinion_space_statement = statement)
        
        if len(ratings_objects) == 0:
            continue
        #adding histogram for statement ratings
        data = {}
        counts = []
        for i in ratings_objects:
            counts.append(i.rating)
        data['counts'] = counts
        data['mean'] = numpy.mean(counts)
        data['std'] = numpy.std(counts)
        keygroup[statement.short_version] = data
        
    analytics[subgroup] = keygroup

path=ASSETS_LOCAL+'statistics/subgroup.pkl'
pickle.dump(analytics, open(path, "w"))
#print analytics
