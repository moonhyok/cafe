#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

f = open('comments.txt','r')
line = f.readline()
text = []
while line != "":
	text.append(line.strip())
	line = f.readline()

for u in DiscussionComment.objects.all():
	u.comment = text[u.id % len(text)]
	print u.id,u.comment
	u.save()

