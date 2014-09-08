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
os_election = OpinionSpace(name = 'CRC V2',
						   created_by = super_user)
os_election.save()

# Create the OS statements
os_election_stmts = {}
os_election_stmt_strings = {}
os_election_stmt_strings[0] = 'Implementation of the Affordable Care Act ("Obamacare")'
os_election_stmt_strings[1] = 'Quality of K-12 public education'
os_election_stmt_strings[2] = 'Affordability of state colleges and universities'
os_election_stmt_strings[3] = 'Access to state services for undocumented immigrants'
os_election_stmt_strings[4] = 'Laws and regulations regarding recreational marijuana'
os_election_stmt_strings[5] = 'Marriage rights for same-sex partners'
os_election_stmt_strings[6] = 'Facebook causes distraction for primary and secondary students.'
os_election_stmt_strings[7] = 'Video lectures are better than traditional lectures as they free up class time for group discussions.'

os_election_stmt_sstrings = {}
os_election_stmt_sstrings[0] = 'Aplicación de la Ley de Cuidado de Salud Asequible ("Obamacare")'
os_election_stmt_sstrings[1] = 'Calidad de la educación pública K-12'
os_election_stmt_sstrings[2] = 'Asequibilidad de los colleges y universidades estatales'
os_election_stmt_sstrings[3] = 'Acceso de inmigrantes indocumentados a servicios estatales'
os_election_stmt_sstrings[4] = 'Leyes y regulaciones con respecto al uso recreativo de la mariguana'
os_election_stmt_sstrings[5] = 'Derecho al matrimonio para parejas del mismo sexo'
os_election_stmt_sstrings[6] = 'Facebook causes distraction for primary and secondary students.'
os_election_stmt_sstrings[7] = 'Video lectures are better than traditional lectures as they free up class time for group discussions.'

#if numStatements > 5:
#	for i in range(5,numStatements):
#		os_election_stmt_strings[i]=('Statement ' + str(i) + ' is a dummy statement created for the purposes of testing')

os_election_stmt_shorts = {}
os_election_stmt_shorts[0] = 'Obamacare'
os_election_stmt_shorts[1] = 'K12'
os_election_stmt_shorts[2] = 'College'
os_election_stmt_shorts[3] = 'Immigration'
os_election_stmt_shorts[4] = 'Marijuana'
os_election_stmt_shorts[5] = 'Marriage Rights'
os_election_stmt_shorts[6] = 'Facebook Distraction'
os_election_stmt_shorts[7] = 'Video Lectures'

os_election_stmt_sshorts = {}
os_election_stmt_sshorts[0] = 'Obamacare'
os_election_stmt_sshorts[1] = 'K12'
os_election_stmt_sshorts[2] = 'Los Colleges'
os_election_stmt_sshorts[3] = 'Inmigración'
os_election_stmt_sshorts[4] = 'Mariguana'
os_election_stmt_sshorts[5] = 'Derecho al matrimonio'
os_election_stmt_sshorts[6] = 'Facebook Distraction'
os_election_stmt_sshorts[7] = 'Video Lectures'

#if numStatements > 5:
#	for i in range(5,numStatements):
#		os_election_stmt_shorts[i] = ('Statement ' + str(i))
#

for i in range(0, numStatements):
    os_election_stmts[i] = OpinionSpaceStatement(opinion_space = os_election,
                                                 statement_number = i,
                                                 statement = os_election_stmt_strings.get(i),
                                                 spanish_statement = os_election_stmt_sstrings.get(i)
						                         type = 1,
                                                 spanish_short_version = os_election_stmt_sshorts.get(i)
                                                 short_version = os_election_stmt_shorts.get(i))
    os_election_stmts[i].save()

disc = DiscussionStatement(opinion_space = os_election, statement = 'What issue should be included in the next report card and why is it important to Californians?', spanish_statement = '¿Cuál problema piensa debe ser incluído en la próxima Report Card, y por qué cree es importante para los Californianos?', short_version='How can social media be used to benefit primary and secondary learning?', is_current = True)
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
