#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *

all_users = User.objects.all()
count_active = 0
for u in all_users:
	if u.id <= 310:
		u.is_active = False
		u.save()
		c = DiscussionComment.objects.filter(user = u, is_current= True)
		if len(c) > 0:
			c[0].blacklisted = True
			c[0].save()
		print "Removing user:", str(u.id)

for c in DiscussionComment.objects.all():
	if 'test' in c.comment.lower():
		c.blacklisted = True
		c.save() 
		c.user.is_active = False
		c.user.save()
		print "Removing user:", str(c.user.id)
	elif len(c.comment.split()) < 5:
		c.blacklisted = True
                c.save()
                c.user.is_active = False
                c.user.save()
                print "Removing user:", str(c.user.id)
	else:
		count_active = count_active + 1

print "Active comments:", str(count_active)
print "Active Users:", str(User.objects.filter(is_active=True).count())
		
		
