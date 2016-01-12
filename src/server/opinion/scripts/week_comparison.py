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
										opinion_space_statement__statement_number=i) \
										.exclude(rating=0.4)
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
										opinion_space_statement__statement_number=i) \
										.exclude(rating=0.4)
		avg = filtered.aggregate(avg=Avg('rating'))['avg']
		if not avg:
			avg = 0.5
		avg_last_week.append(avg)

	labels = ['1', '2', '3', '4', '5']
	fig, ax = plt.subplots()
	ind = np.array([0.1, 1.1, 2.1, 3.1, 4.1])
	bar1 = ax.bar(ind, avg_last_week, width=0.3, color='r', label='Last week')
	bar2 = ax.bar(ind+0.35, avg_this_week, width=0.3, color='b', label='This week')
	label_mean(ax, bar1)
	label_mean(ax, bar2)
	ax.set_xticks(ind+0.3)
	ax.set_xticklabels(labels)
	plt.ylim(0.0, 1.1)
	ax.set_xlabel('QAT Number')
	ax.set_ylabel('Mean Rating')
	ppl.legend(ax, loc="upper right")
	fig.savefig('/var/www/opinion/opinion.berkeley.edu/landing/m-cafe/ieor170-sp16/src/client/media/images/qat.png')


def label_mean(ax, bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2., 1.05*height, '%0.3f'%height, \
                ha='center', va='bottom')
