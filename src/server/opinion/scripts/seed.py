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
names = ['rob', 'john', 'mary', 'elaine','james']
for i in range(0, 5):
    print "Creating user %s/5..." % (i + 1)
    
    if i == 0:
        user = User.objects.filter(id=1)[0]
    else:
        user = User.objects.create_user(names[i], '%s@example.com' % names[i], 'admin')
        user.save()
    
    # Create random ratings
    for stmt in os_stmts:
        rating = random()
        test = random()
        if test < .1:
            rating = .1
        elif test > .9:
            rating = .9
			
        rating = UserRating(user = user,
                            opinion_space = first_os,
                            opinion_space_statement = stmt,
                            rating = rating,
                            is_current = True)
        rating.save()

    # Create random comments
    comment = DiscussionComment(user = user,
                                opinion_space = first_os,
                                discussion_statement = disc_stmt,
                                comment = 'This is user %s\'s comment. This is a test comment' % user,
								query_weight = 1,
                                is_current = True)
    comment.save()
    
print 'Database populated with random users and ratings.'

# Create random ratings
for user in User.objects.all():
	
	# rate all comments randomly
	i = 1
	for comment in DiscussionComment.objects.order_by('?')[:4]:
		print "User: " + str(user.id) + " rating and suggestion for comment " + str(i)
		
		rating = random()
		score = calculate_reputation_score(1, user, comment.user, rating)
		cr = CommentRating(comment = comment, rater = user, rating = rating, score = score, reviewer_score = 1, is_current = True, early_bird = 1)
		cr.save()
		
		agreement = random()
		ca = CommentAgreement(comment = comment, rater = user, agreement = agreement, is_current = True)
		ca.save()
	
		suggestion = Suggestion(suggester = user, comment = comment, q = random(),suggestion = "This is a suggestion")
		suggestion.save()
		i+=1
		
print "ratings created"
