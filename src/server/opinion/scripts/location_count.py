#!/usr/bin/env python
import sys
import environ
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
from operator import itemgetter

print "Aggregating user locations"

locations = {}
users = User.objects.all()
for user in users:
	location = get_location(user)
	if location in locations.keys():
		locations[location] += 1
	else:
		locations[location] = 1

loc = locations.items()
loc.sort(key = itemgetter(1), reverse=True)

for l in loc:
	print l[0] + ': ' + str(l[1])
	
print "Done."