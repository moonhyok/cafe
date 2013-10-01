#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

"""
f = open('output.csv', 'a')
age_to_value={'na':-1,'01-18':0,'18-25':1,'26-33':2,'33-50':3,'50+':4}
bre = True
for c in DiscussionComment.objects.filter(is_current=True).order_by('-normalized_score_sum'):
		try:
			print c.user.id, c.comment
					
			if bre:
				if c.user.id == 129:
					bre = False
				continue
			
			d = raw_input('cat:')
			if UserData.objects.filter(key='age',user=c.user).count() > 0:
				nom = UserData.objects.filter(key='age',user=c.user)[0].value
				f.write(d+','+str(age_to_value[nom]))
			print '-----------------'
		except UnicodeEncodeError:
			print 'err'

f = open('output.csv', 'a')
"""
sorted_comments = []
for c in DiscussionComment.objects.filter(is_current=True).order_by('-normalized_score_sum').exclude(normalized_score_sum=None):
        val = 0
        if CommentAgreement.objects.filter(comment=c,is_current=True).count() > 2:
            val = .5*np.mean(CommentAgreement.objects.filter(comment=c,is_current=True).values_list('agreement')) + .5*c.normalized_score_sum
            sorted_comments.append((val,c.comment,c.user))

sorted_comments.sort(reverse=True)
for c in sorted_comments[:20]:
		try:
			print c[2].email,c[2].id,c[0],c[1]
		except UnicodeEncodeError:
			print ""

"""
f = open('output.csv', 'a')
sorted_comments = []
for c in DiscussionComment.objects.filter(is_current=True).order_by('-normalized_score_sum').exclude(normalized_score_sum=None):
        val = 0
        if CommentAgreement.objects.filter(comment=c,is_current=True).count() > 2:
            val = np.std(CommentRating.objects.filter(comment=c,is_current=True).values_list('rating'))
            sorted_comments.append((val,c.comment))

sorted_comments.sort(reverse=True)
for c in sorted_comments:
        print c[0]
"""
		

