#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
from opinion.includes.queryutils import *
import json
from django.db.models import Q

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1
print json.dumps(counties)
"""
"""
geo_json=open('../geo-ca.json')
geo_data=json.load(geo_json)
counties = {}
for i in range(0,len(geo_data['features'])):
    county=geo_data['features'][i]['properties']['NAME']
    zipcode_in_county=ZipCode.objects.filter(state='CA').filter(county__startswith=county)
    if len(zipcode_in_county) > 0:
        counties[county] = ZipCodeLog.objects.filter(location__in=zipcode_in_county).count()/(geo_data['features'][i]['properties']['Population']/10000.0)
print json.dumps(counties)
"""

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1

counties2 = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0 and CommentAgreement.objects.filter(is_current=True,rater=u).count() > 5:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties2:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
        else:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
print json.dumps(counties2)
"""

"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0 and UserRating.objects.filter(is_current=True, user = u).count() > 3:
        m = np.mean(UserRating.objects.filter(is_current=True, user = u).values_list('rating'))
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]].append(m)
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = [m]

counties2 = {}
for c in counties:
    counties2[c] = 1-np.median(counties[c])
print json.dumps(counties2)

"""
"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    if len(zc_log_object) > 0:
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1

counties2 = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    comment = ""
    if DiscussionComment.objects.filter(user = u,is_current=True).count() > 0:
        c = DiscussionComment.objects.filter(user = u,is_current=True)[0]
        tag_object = AdminCommentTag.objects.filter(comment = c)
        if tag_object.count() > 0:
            comment = tag_object[0].tag.lower()

    if len(zc_log_object) > 0 and (('disaster' in comment)):
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties2:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] + 1/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
        else:
                counties2[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = 1.0/counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]]
print json.dumps(counties2)
"""


"""
counties = {}
for u in User.objects.all():
    zc_log_object = ZipCodeLog.objects.filter(user = u)
    comments = AdminCommentTag.objects.filter(Q(tag__icontains="disaster")).values("comment")
    if len(zc_log_object) > 0 and CommentAgreement.objects.filter(is_current=True, rater = u, comment__in = comments).count() > 0:
        m = np.mean(CommentRating.objects.filter(is_current=True, rater = u, comment__in = comments).values_list('rating'))
        if zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7] in counties:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]].append(m)
        else:
                counties[zc_log_object[0].location.county[0:len(zc_log_object[0].location.county)-7]] = [m]

counties2 = {}
for c in counties:
    counties2[c] = 1-np.median(counties[c])
print json.dumps(counties2)
"""
"""
for r in CommentAgreement.objects.filter(comment__in = DiscussionComment.objects.filter(Q(is_current=True, comment__icontains='water', user__in=User.objects.filter(is_active=True))), is_current=True).order_by('created'):
    if r.agreement != .5:
        print 1-r.agreement
"""
