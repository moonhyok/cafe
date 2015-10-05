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
    super_user.set_password('admin')
    super_user.save()
except User.DoesNotExist:
    print 'Error: you must have a super user account in order to set up the database properly!'
    sys.exit()
    
# Add the site domain/name to the database
site = Site(id = 1,
            domain = 'opinion.berkeley.edu',
            name = 'Opinion Space')
site.save()

# Create the OS
os_election = OpinionSpace(name = 'Opinion Space',
						   created_by = super_user)
os_election.save()

# Create the OS statements
os_election_stmts = {}
os_election_stmt_strings = {}
for i in range(0,numStatements):
	os_election_stmt_strings[i] = 'Statement ' + str(i)

#if numStatements > 5:
#	for i in range(5,numStatements):
#		os_election_stmt_strings[i]=('Statement ' + str(i) + ' is a dummy statement created for the purposes of testing')

os_election_stmt_shorts = {}
for i in range(0,numStatements):
	os_election_stmt_shorts[i] = 'Statement ' + str(i)

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

disc = DiscussionStatement(opinion_space = os_election, statement = 'Question?', short_version='Question?', is_current = True)
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
