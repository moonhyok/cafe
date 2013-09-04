#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from django.contrib.auth.models import User

os_id = 1 # Using OS #1 for now

try:
    os = OpinionSpace.objects.get(pk = os_id)
except OpinionSpace.DoesNotExist:
    print 'That Opinion Space does not exist.'
    sys.exit()

# Set old eigenvectors as not current
eigenvectors = OpinionSpaceEigenvector.objects.filter(opinion_space = os,
                                                      is_current = True)
eigenvector_list = []
for eigenvector in eigenvectors:
    eigenvector_list.append(eigenvector)
eigenvectors.update(is_current = False)

flipped_eigenvector_numbers = {}
for eigenvector in eigenvector_list:
    if eigenvector.eigenvector_number == 0:
        flipped_eigenvector_numbers[eigenvector.id] = 1
    else:
        flipped_eigenvector_numbers[eigenvector.id] = 0

# Store the rotated eigenvectors
for eigenvector in eigenvector_list:
    new_eigenvector = OpinionSpaceEigenvector(opinion_space = eigenvector.opinion_space,
                                              eigenvector_number = flipped_eigenvector_numbers.get(eigenvector.id),
                                              coordinate_number = eigenvector.coordinate_number,
                                              value = eigenvector.value,
                                              is_current = True)
    new_eigenvector.save()

print 'Eigenvectors rotated.'
