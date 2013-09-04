#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from numpy import *

os_id = 1 # Using OS #1 for now

try:
    os = OpinionSpace.objects.get(pk = os_id)
except OpinionSpace.DoesNotExist:
    print 'That Opinion Space does not exist.'
    sys.exit()

discussion_statement = DiscussionStatement.objects.filter(opinion_space = os, is_current = True)[0]
# Only look at comments for the most recent discussion statement
current_comments = DiscussionComment.objects.filter(opinion_space = os, discussion_statement = discussion_statement, is_current = True)
for current_comment in current_comments:
    if current_comment.average_score is not None:
        print str(current_comment.average_score)
    else:
        print 'Null'
