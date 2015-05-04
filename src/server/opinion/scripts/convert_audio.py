#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import settings

from sh import say

for comment in DiscussionComment.objects.all():
	path = str(comment.id) + ".ogg"
	say("-r 200", "-o" + path, _in=comment.comment)
