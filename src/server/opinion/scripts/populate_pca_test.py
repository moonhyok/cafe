#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from django.contrib.auth.models import User
from random import *
from opinion.includes.mathutils import *
import csv


# Get the first OS
first_os = OpinionSpace.objects.get(pk = 1)

# Get the OS statements for the first OS
os_stmts = OpinionSpaceStatement.objects.filter(opinion_space = first_os)

# Get the discussion statement for the first OS
disc_stmt = first_os.discussion_statements.filter(is_current = True)[0]


# Read from csvfile, hardcoded for now to read from my local directory. This file will be changed when shit gets done.
with open('../../../../../L1Embedding/statements_5711_processed.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        user = User.objects.create_user('user_%d' % i, 'user_%d@gmail.com' % i, 'test')
        user.save()
        rating = UserRating(user = user,
                            opinion_space = first_os,
                            opinion_space_statement = stmt,
                            rating = row,
                            is_current = True)
        rating.save()

        print row

'''
# Create random users
for i in range(0, 30):
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

# Create random ratings
for user in User.objects.all():
        
        # rate all comments randomly
        i = 1
        for comment in DiscussionComment.objects.order_by('?')[:20]:
                print "User: " + str(user.id) + " rating for comment " + str(i)
                
                rating = random()
                score = calculate_reputation_score(1, user, comment.user, rating)
                cr = CommentRating(comment = comment, rater = user, rating = rating, score = score, reviewer_score = 1, is_current = True, early_bird = 1)
                cr.save()
                
                agreement = random()
                ca = CommentAgreement(comment = comment, rater = user, agreement = agreement, is_current = True)
                ca.save()
                
                i+=1
'''
print "ratings created"