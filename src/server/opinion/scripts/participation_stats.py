import environ
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
import numpy as np
import datetime
import matplotlib.pyplot as plt
from pylab import *

def participation():
	user_set = User.objects.filter(is_active=True)

	num_weeks, start_date = calculate_week(user_set)

	# Weekly comment data
	comment_data = [DiscussionComment.objects.filter(user__in=user_set, \
                created__gte=start_date, created__lt=(start_date+datetime.timedelta(days=7))).count()]
	lower_bound = 7
	upper_bound = 14
	for i in range(num_weeks - 1):
		comment_count = DiscussionComment.objects.filter(user__in=user_set, \
			created__gte=(start_date+datetime.timedelta(days=lower_bound)), \
			created__lt=(start_date+datetime.timedelta(days=upper_bound))).count()
		comment_data.append(comment_count)
		lower_bound += 7
		upper_bound += 7


	# Weekly user data
	user_data = [UserRating.objects.filter(user__in=user_set, \
            created__gte=start_date, created__lt=(start_date+datetime.timedelta(days=7))).count()]
	user_data = [user_data[0]/5]
	lower_bound = 7
	upper_bound = 14
	for i in range(num_weeks - 1):
		user_count = UserRating.objects.filter(user__in=user_set, \
			created__gte=(start_date+datetime.timedelta(days=lower_bound)), \
			created__lt=(start_date+datetime.timedelta(days=upper_bound))).count()
		user_data.append(user_count/5)
		lower_bound += 7
		upper_bound += 7

	# Weekly CF rating data
	cf_data = [CommentAgreement.objects.filter(created__gte=start_date,\
			created__lt=(start_date+datetime.timedelta(days=7))).count()]
	lower_bound = 7
	upper_bound = 14
	for i in range(num_weeks - 1):
		cf_count = (CommentAgreement.objects.filter(created__gte=(start_date+datetime.timedelta(days=lower_bound)), \
			created__lt=(start_date+datetime.timedelta(days=upper_bound))).count())/5
		cf_data.append(cf_count)
		lower_bound += 7
		upper_bound += 7

	fig, ax = plt.subplots()
	ax.set_xlabel('Week')
	ax.set_ylabel('Weekly Participation')
	ax.set_title('Weekly User Participation')
	x = range(1, num_weeks+1)
	ax.plot(x, user_data)
	ax.plot(x, cf_data)
	ax.plot(x, comment_data)
	ax.legend(["# Weekly Users", "# CF Ratings", "# Comments"], loc='upper right')
	plt.show()
	fig.savefig('../../client/media/images/participation.png')

