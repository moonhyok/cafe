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
os_stmts = OpinionSpaceStatement.objects.filter(opinion_space = first_os).order_by('id')

# Get the discussion statement for the first OS
disc_stmt = first_os.discussion_statements.filter(is_current = True)[0]


# Read from csvfile, hardcoded for now to read from my local directory. This filepath will be changed when shit gets done.
with open('state_dept.csv', 'rb') as csvfile: #../../../../../L1Embedding/
    reader = csv.reader(csvfile)
    i = 1
    stmt = list(os_stmts[:1])[0]
    for row in reader:
        user = User.objects.create_user('user_%d' % i, 'user_%d@gmail.com' % i, 'test')
        user.save()

        #for stmt in os_stmts:
        if i > 1: # skip first row because it's just labels
            for j in range(0,len(row)):
                if j >= 6 and j <= 10:
                    number = row[j]
                    rating = UserRating(user = user,
                                        opinion_space = first_os,
                                        opinion_space_statement = stmt,
                                        rating = float(number),
                                        is_current = True)
                    rating.save()
            print number

        i += 1

        #print row

print "ratings created"