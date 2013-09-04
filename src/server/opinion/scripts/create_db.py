#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from numpy import *

from random import *

if len(sys.argv) != 2:
	print 'Usage: python create_db.py [num statements]'
	exit()
	
numStatements = int(sys.argv[1])
	
# Clear the relevant DB tables
Site.objects.all().delete()
OpinionSpace.objects.all().delete()
OpinionSpaceStatement.objects.all().delete()
OpinionSpaceEigenvector.objects.all().delete()
UserRating.objects.all().delete()
DiscussionComment.objects.all().delete()

# Gets the super user, and errors if there isn't one
try:
    super_user = User.objects.get(pk = 1)
except User.DoesNotExist:
    print 'Error: you must have a super user account in order to set up the database properly!'
    sys.exit()
    
# Add the site domain/name to the database
site = Site(id = 1,
            domain = 'opinion.berkeley.edu',
            name = 'Opinion Space')
site.save()

# Create the OS
os_election = OpinionSpace(name = 'Fujitsu Learning',
						   created_by = super_user)
os_election.save()

# Create the OS statements
os_election_stmts = {}
os_election_stmt_strings = {}
os_election_stmt_strings[0] = 'Google Docs can help students learn math by enabling them to work together to solve problems.'
os_election_stmt_strings[1] = 'Social Media games like "Words with Friends" can teach students about collective problem solving.'
os_election_stmt_strings[2] = 'Twitter can expose students to new perspectives on topics they are studying.'
os_election_stmt_strings[3] = 'Facebook can improve student\'s social skills.'
os_election_stmt_strings[4] = 'A degree from an on-line school like Khan Academy is equivalent to a high-school diploma.'
os_election_stmt_strings[5] = 'Nothing can replace a pencil and paper for learning.'
os_election_stmt_strings[6] = 'Facebook causes distraction for primary and secondary students.'
os_election_stmt_strings[7] = 'Video lectures are better than traditional lectures as they free up class time for group discussions.'

#if numStatements > 5:
#	for i in range(5,numStatements):
#		os_election_stmt_strings[i]=('Statement ' + str(i) + ' is a dummy statement created for the purposes of testing')

os_election_stmt_shorts = {}
os_election_stmt_shorts[0] = 'Google Docs'
os_election_stmt_shorts[1] = 'Collective Problem Solving'
os_election_stmt_shorts[2] = 'Twitter'
os_election_stmt_shorts[3] = 'Facebook Social Skills'
os_election_stmt_shorts[4] = 'Online Degree'
os_election_stmt_shorts[5] = 'Pencil/Paper'
os_election_stmt_shorts[6] = 'Facebook Distraction'
os_election_stmt_shorts[7] = 'Video Lectures'

#if numStatements > 5:
#	for i in range(5,numStatements):
#		os_election_stmt_shorts[i] = ('Statement ' + str(i))
#

for i in range(0, numStatements):
    os_election_stmts[i] = OpinionSpaceStatement(opinion_space = os_election,
                                                 statement_number = i,
                                                 statement = os_election_stmt_strings.get(i),
                                                 short_version = os_election_stmt_shorts.get(i))
    os_election_stmts[i].save()

disc = DiscussionStatement(opinion_space = os_election, statement = 'How can social media be used to benefit primary and secondary learning?', short_version='How can social media be used to benefit primary and secondary learning?', is_current = True)
disc.save()

# These are the initial eigenvectors
sorted_eigenvectors = [[], []]
for i in range(0,numStatements):
	sorted_eigenvectors[0].append(i%2)
	sorted_eigenvectors[1].append(1 - i%2)

# Store initial eigenvectors in the database
for i, eigenvector in enumerate(sorted_eigenvectors):
    for j, value in enumerate(eigenvector):
        os_eigenvector = OpinionSpaceEigenvector(opinion_space = os_election,
                                                 eigenvector_number = i,
                                                 coordinate_number = j,
                                                 value = value,
                                                 is_current = True)
        print os_eigenvector.value
        os_eigenvector.save()

print 'Opinion Space database created.'
