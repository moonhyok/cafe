#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from numpy import *

from random import *

# Gets the super user, and errors if there isn't one
try:
    super_user = User.objects.get(pk = 1)
except User.DoesNotExist:
    print 'Error: you must have a super user account in order to set up the database properly!'
    sys.exit()
    
# Create the OS
os_new = OpinionSpace(name = 'US Foreign Policy',
						   created_by = super_user)
os_new.save()

# Create the OS statements
os_new_stmts = {}
os_new_stmt_strings = {}
os_new_stmt_strings[0] = 'Preventing the spread and use of nuclear weapons is an enormous security challenge, and there is no more urgent threat to the United States than a terrorist armed with a nuclear weapon.'
os_new_stmt_strings[1] = 'Anything short of relentless diplomatic efforts will fail to produce a lasting, sustainable peace in Afghanistan and Pakistan.'
os_new_stmt_strings[2] = 'Climate change poses a threat to political stability around the world.'
os_new_stmt_strings[3] = 'Investing in other countries to increase the amount of food grown will ultimately help benefit me and my family in the future.'
os_new_stmt_strings[4] = 'The best way to advance a country\'s economic development is to empower its women.'
os_new_stmt_shorts = {}
os_new_stmt_shorts[0] = 'Nuclear Weapons'
os_new_stmt_shorts[1] = 'Proactive Diplomacy'
os_new_stmt_shorts[2] = 'Climate Change'
os_new_stmt_shorts[3] = 'Invest in Food'
os_new_stmt_shorts[4] = 'Empower Women'
for i in range(0, 5):
    os_new_stmts[i] = OpinionSpaceStatement(opinion_space = os_new,
                                                 statement_number = i,
                                                 statement = os_new_stmt_strings.get(i),
                                                 short_version = os_new_stmt_shorts.get(i))
    os_new_stmts[i].save()

disc = DiscussionStatement(opinion_space = os_new, statement = 'In your view, what innovations in approach and method were most successful in the Department of State\'s first year, and what new ideas do you feel would be most effective in making the world safer and more just going forward?', short_version='The Department of State\'s First Year', is_current = True)
disc.save()

# These are the initial eigenvectors
sorted_eigenvectors = [array([1, 0, 1, 0, 1]), array([0, 1, 0, 1, 0])]

# Store initial eigenvectors in the database
for i, eigenvector in enumerate(sorted_eigenvectors):
    for j, value in enumerate(eigenvector):
        os_eigenvector = OpinionSpaceEigenvector(opinion_space = os_new,
                                                 eigenvector_number = i,
                                                 coordinate_number = j,
                                                 value = value,
                                                 is_current = True)
        os_eigenvector.save()

# Create landmarks
# Note: the landmarks must provide a rating for each of the discussion statements!
"""
landmark = Landmark(opinion_space = os_new, name = 'Ralph Nader', description = 'Ralph Nader was an independent candidate for President of the United States in 2004 and 2008, and a Green Party candidate in 1996 and 2000.', guess_text = 'His position on the map is an extrapolation based on his public statements and campaign platforms.', image_path = 'images/nader.jpg', ratings_json = '[0.0,1.0,0.9,1.0,0.0]', is_current = True)
landmark.save()

landmark = Landmark(opinion_space = os_new, name = 'Rush Limbaugh', description = 'Rush Limbaugh is an American radio host and conservative political commentator.', guess_text = 'His position on the map is an extrapolation based on his public statements and broadcasts.', image_path = 'images/limbaugh.jpg', ratings_json = '[1.0,0.0,0.0,0.0,1.0]', is_current = True)
landmark.save()

landmark = Landmark(opinion_space = os_new, name = 'Arnold Schwarzenegger', description = 'Arnold Schwarzenegger is the current Governor of the U.S. state of California. He is a Republican.', guess_text = 'His position on the map is an extrapolation based on his public statements and policies.', image_path = 'images/schwarzenegger.jpg', ratings_json = '[0.4,0.3,0.5,0.9,0.2]', is_current = True)
landmark.save()

landmark = Landmark(opinion_space = os_new, name = 'Nancy Pelosi', description = 'Nancy Pelosi is the current Speaker of the United States House of Representatives. She is a Democrat.', guess_text = 'Her position on the map is an extrapolation based on her public statements and voting record.', image_path = 'images/pelosi.jpg', ratings_json = '[0.4,1.0,0.9,0.9,0.0]', is_current = True)
landmark.save()
"""

print 'New opinion space created.'
