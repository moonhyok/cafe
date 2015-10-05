#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
from opinion.includes.queryutils import *
import json

import csv
with open('spanish_comments.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	count = 1
	for row in spamreader:
		if count != 1:
			comment = DiscussionComment.objects.filter(id=count)
			if len(comment) != 0:
				comment = comment[0]
				comment.comment = row[2]
				#comment.spanish_comment = row[4]
				#a = AdminCommentTag(tag = row[1], comment = comment) 
				#a.save()
				comment.save()
				print count,row[1],row[2],comment.spanish_comment
		count = count + 1


