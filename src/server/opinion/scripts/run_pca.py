#!/usr/bin/env python
import sys
import environ
from opinion.includes.pca_module import *
from numpy import *
from opinion.opinion_core.models import *
from django.contrib.auth.models import User

"""
We are plotting users, so:
- Objects: users
- Variables: different ratings for each OS statement

Thus, the data matrix will be of the form:

User 1: [rating_1 rating_2 rating_3 rating_4 rating_5]
User 2: [rating_1 rating_2 rating_3 rating_4 rating_5]
...
User n: [rating_1 rating_2 rating_3 rating_4 rating_5]
"""
	
def eig_sort(explained_vars, eigenvectors):
    evar_to_evec = dict(map(None, explained_vars, eigenvectors))
    sorted_evars = evar_to_evec.keys()
    sorted_evecs = []
    for evar in sorted_evars:
        sorted_evecs.append(evar_to_evec.get(evar))
        print evar
    return sorted_evecs
    
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

standardized = False
try:
    scores, eigenvectors, explained_vars = PCA_nipals2(data, standardize=True, PCs=2, E_matrices=False)
    standardized = True
except ZeroDivisionError:
    scores, eigenvectors, explained_vars = PCA_nipals2(data, standardize=False, PCs=2, E_matrices=False)
    standardized = False
sorted_eigenvectors = eig_sort(explained_vars, eigenvectors)

# Set old eigenvectors as not current
OpinionSpaceEigenvector.objects.filter(opinion_space = os,
                                       is_current = True).update(is_current = False)

# Store all new eigenvectors in the database
for i, eigenvector in enumerate(sorted_eigenvectors):
    for j, value in enumerate(eigenvector):
        os_eigenvector = OpinionSpaceEigenvector(opinion_space = os,
                                                 eigenvector_number = i,
                                                 coordinate_number = j,
                                                 value = value,
                                                 is_current = True)
        os_eigenvector.save()
        
print 'PCA script complete (standardized = %s).' % standardized
