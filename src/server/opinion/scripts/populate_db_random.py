#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from random import *
from opinion.includes.mathutils import *

# Get the first OS
first_os = OpinionSpace.objects.get(pk = 1)

# Get the OS statements for the first OS
os_stmts = OpinionSpaceStatement.objects.filter(opinion_space = first_os)

# Get the discussion statement for the first OS
disc_stmt = first_os.discussion_statements.filter(is_current = True)[0]

# Create random users
for i in range(30, 75):
    print "Creating user %s/30..." % (i + 1)
    
    user = User.objects.create_user('user_%d' % i, 'user_%d@gmail.com' % i, 'test')
    user.save()
    
    # Create random ratings
    for stmt in os_stmts:
        rating = UserRating(user = user,
                            opinion_space = first_os,
                            opinion_space_statement = stmt,
                            rating = random(),
                            is_current = True)
        rating.save()

    # Create random comments
    comment = DiscussionComment(user = user,
                                opinion_space = first_os,
                                discussion_statement = disc_stmt,
                                comment = 'This is user %s\'s comment.' % user,
								query_weight = 1,
                                is_current = True)
    comment.save()
    
print 'Database populated with random users and ratings.'
