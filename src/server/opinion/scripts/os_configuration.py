#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from django.contrib.auth.models import User

"""

This script will only handle the creation and updating of 
Opinion Space, statements, discussion statements, and landmarks

It will initialize an Opinion Space with new eigenvectors if none exist

"""

# Input OS name, statements, and discussion question as strings
os_name = 'Unilever'
statements = {}
statements[0] = 'I regularly attend religious services'
statements[1] = 'Not many of my friends are Jewish.'
statements[2] = 'I consider myself culturally Jewish.'
statements[3] = 'I don\'t closely follow Middle East politics.'
statements[4] = 'The Holocaust could happen again.'
statements_short = {}
statements_short[0] = 'Attendance of Religious Services'
statements_short[1] = 'Jewish Friends'
statements_short[2] = 'Culturally Jewish'
statements_short[3] = 'Middle East Politics'
statements_short[4] = 'The Holocaust'
discussion_statement = 'The \"Are We There Yet?\" exhibit (opening in March 2011) will feature a changing series of questions from Jewish texts and history to pop culture. What are some questions that resonate with you that we might consider including?'
discussion_statement_short = 'Questions for the \"Are We There Yet?\" Exhibit'

# Input landmarks as a list of dictionaries formatted as 
# {'name':name, 'description':description, 'guess': guess_text, 'image_path':image_path, 'ratings_json': '[1.0,0.5,0.75,1.0,1.0]'}
landmarks = {}

# Gets the super user, and errors if there isn't one
try:
    super_user = User.objects.get(pk = 1)
except User.DoesNotExist:
    print 'Error: you must have a super user account in order to set up the database properly!'
    sys.exit()

# Looks for the OS and create it if it can't find it
try:
	os = OpinionSpace.objects.get(name = os_name)
except OpinionSpace.DoesNotExist:
	os = OpinionSpace(name = os_name,
					  created_by = super_user)
	os.save()
	
# Initialize eigenvectors if needed
eigenvector_filter = OpinionSpaceEigenvector.objects.filter(opinion_space = os)
if len(eigenvector_filter) == 0:
	sorted_eigenvectors = [[1, 0, 1, 0, 1], [0, 1, 0, 1, 0]]
	for i, eigenvector in enumerate(sorted_eigenvectors):
	    for j, value in enumerate(eigenvector):
	        os_eigenvector = OpinionSpaceEigenvector(opinion_space = os,
	                                                 eigenvector_number = i,
	                                                 coordinate_number = j,
	                                                 value = value,
	                                                 is_current = True)
	        os_eigenvector.save()	
	
# Go through the statements. If the statement exists, update the text. Otherwise, create a new one
for i in range(0, len(statements)):
	try:
		stmt = OpinionSpaceStatement.objects.get(opinion_space = os, statement_number = i)
		OpinionSpaceStatement.objects.filter(opinion_space = os, statement_number = i).update(statement = statements[i], short_version = statements_short[i])
	except OpinionSpaceStatement.DoesNotExist:
		stmt = OpinionSpaceStatement(opinion_space = os,
	                                statement_number = i,
									statement = statements[i],
									short_version = statements_short[i])
		stmt.save()

# Add the discussion statment if it doesn't exist
try:
	disc = DiscussionStatement.objects.get(opinion_space = os,
										  statement = discussion_statement)
except DiscussionStatement.DoesNotExist:
	disc = DiscussionStatement(opinion_space = os, 
						   	  statement = discussion_statement, 
					   		  short_version  = discussion_statement_short,
						   	  is_current = True)
	disc.save()

# Add landmarks or update their info if they exist
for i in range(0, len(landmarks)):
	try:
		landmark = Landmark.objects.get(opinion_space = os, 
										name = landmarks[i]['name'],
										is_current = True)
										
		Landmark.objects.filter(opinion_space = os, 
								name = landmarks[i]['name'],
								is_current = True).update(description = landmarks[i]['description'], 
														 guess_text = landmarks[i]['guess'], 
														 image_path = landmarks[i]['image_path'], 
														 ratings_json = landmarks[i]['ratings_json'])
	except Landmark.DoesNotExist:
		landmark = Landmark(opinion_space = os, 
							name = landmarks[i]['name'],
							description = landmarks[i]['description'], 
							guess_text = landmarks[i]['guess'], 
							image_path = landmarks[i]['image_path'], 
							ratings_json = landmarks[i]['ratings_json'],
							is_current = True)
		landmark.save()

print "Done."

