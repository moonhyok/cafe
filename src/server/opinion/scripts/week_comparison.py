import environ
from opinion.opinion_core.models import *
import numpy as np
import datetime
from django.db.models import Avg
import matplotlib.pyplot as plt
import prettyplotlib as ppl


# Note: pandas 0.15.2 or earlier needed!!!!!

def compare_weeks():
	users = User.objects.filter(is_active=True)
	today = datetime.date.today()
	start_of_week = today - datetime.timedelta(days=today.weekday())
	start_of_week = datetime.datetime.combine(start_of_week, datetime.time())
	last_week = start_of_week - datetime.timedelta(days=7)

	# Calculate this week's average rating for each Opinion Space
	# Statement
	avg_this_week = []
	for i in range(5):
		filtered = UserRating.objects.filter(user__in=users, created__gte=start_of_week,
										created__lt=start_of_week + datetime.timedelta(days=7),
										opinion_space_statement__statement_number=i)
                print(filtered)
                avg = filtered.aggregate(avg=Avg('rating'))['avg']
		if not avg:
			avg = 0.0
		avg_this_week.append(avg)

	# Calculate last week's average rating for each Opinion Space
	# Statement
	avg_last_week = []
	for i in range(5):
		filtered = UserRating.objects.filter(user__in=users, created__gte=last_week,
										created__lt=start_of_week,
										opinion_space_statement__statement_number=i)
		avg = filtered.aggregate(avg=Avg('rating'))['avg']
		if not avg:
			avg = 0.0
		avg_last_week.append(avg)

	labels = ['1', '2', '3', '4', '5']
	fig, ax = plt.subplots()
	ind = np.arange(5)
	ppl.bar(ax, ind, avg_last_week, width=0.3, annotate=True, xticklabels=labels, color='r', label='Last week')
	ppl.bar(ax, ind+0.4, avg_this_week, width=0.3, annotate=True, xticklabels=labels, color='b', label='This week')
	plt.ylim(0.0, 1.1)
	ax.set_xlabel('QAT Number')
	ax.set_ylabel('Mean Rating')
	ppl.legend(ax, loc="upper right")
	fig.savefig('../../client/media/images/qat.png')

