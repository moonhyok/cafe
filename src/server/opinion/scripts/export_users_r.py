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

statement_count = os.statements.count()
user_count = User.objects.count()

default_rating = (settings.MAX_RATING - settings.MIN_RATING) / 2.0
data = mat(default_rating * ones((user_count, statement_count)))

# Create a dictionary mapping the user's actual ID to his number in the user count
uid_to_unum = {}
for i, user in enumerate(User.objects.all()):
    uid_to_unum[user.id] = i

for rating in os.ratings.filter(is_current = True):
    try:
        row = uid_to_unum.get(rating.user.id)
        col = rating.opinion_space_statement.statement_number
        data[row, col] = rating.rating
    except IndexError:
        print 'Error in creating the data matrix.'
        sys.exit()

print data