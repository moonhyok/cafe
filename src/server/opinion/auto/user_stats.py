import os
import environ
from opinion.includes.queryutils import *
from opinion.opinion_core.models import *
import numpy as np
from ggplot import *
from pandas import DataFrame
import datetime


def stats(user_set, question):
	"""
	Plots the average rating per week for Opinion Space
	statement question over the range of num_weeks

	users: list of users whose stats we want to plot
	question: the number of the Opinon Space statement
	to plot
	"""
	# determine start date of cafe
	num_weeks, start_date = calculate_week(user_set)
	os_statements = OpinionSpaceStatement.objects.count()

	#Stats page plots
	weekly_data = [UserRating.objects.filter(user__in=user_set, created__lt=(start_date+datetime.timedelta(days=7))).exclude(rating=0.4)]
	lower_bound = 7
	upper_bound = 14
	for i in range(num_weeks):
		weekly_data.append(UserRating.objects.filter(user__in=user_set, \
			created__gte=(start_date+datetime.timedelta(days=lower_bound)), \
			created__lt=(start_date+datetime.timedelta(days=upper_bound)))) \
			.exclude(rating=0.4)
		lower_bound += 7
		upper_bound += 7


	names = ['user', 'opinion_space', 'opinion_space_statement',
			'rating', 'is_current', 'created']

	weekly_array = []
	for i in range(num_weeks):
		weekly_array.append(models_to_array(weekly_data[i], names))


	
	temps = []
	for i in range(num_weeks):
		to_append = [0.5] * os_statements if weekly_array[i].size == 0 \
					else tapply(weekly_array[i][:,3], weekly_array[i][:,2], np.mean)[0]
		temps.append(to_append)

	sd = []
	for i in range(num_weeks):
		to_append = [0] * os_statements if weekly_array[i].size == 0 \
					else tapply(weekly_array[i][:,3], weekly_array[i][:,2], np.std)[0]
		sd.append(to_append)
	

	
	lens = []
	for i in range(num_weeks):
		to_append = [1] * os_statements if weekly_array[i].size == 0 \
					else tapply(weekly_array[i][:,3], weekly_array[i][:,2], len)[0]
		lens.append(to_append)


	se = []
	for i in range(num_weeks):
		to_append = [sd[i][j]/sqrt(lens[i][j]) for j in range(len(lens[i]))]
		se.append(to_append)


	title = title = OpinionSpaceStatement.objects.filter(
		statement_number=(question-1))[0].short_version
	if question == 1:
		diff = []
		for i in range(num_weeks):
			to_append = temps[i][0] * 10
			diff.append(to_append)

		sd_diff = []
		for i in range(num_weeks):
			to_append = se[i][0] * 20
			sd_diff.append(to_append)

		data = np.array([range(1, num_weeks+1), diff])
		p = ggplot(DataFrame(data), aes(x=range(1,num_weeks+1), y=diff)) + \
	  	geom_line() + \
	  	geom_point() + \
	  	ylim(0, 10) + \
	  	xlab('Week') + \
	  	ylab('Mean Rating') + \
	  	ggtitle(title)
	  	ggsave(p, "../../client/media/images/graph1.png", scale=0.75)
	elif question == 2:
		useful = []
		for i in range(num_weeks):
			to_append = temps[i][1] * 10
			useful.append(to_append)

		sd_useful = []
		for i in range(num_weeks):
			to_append = se[i][1] * 20
			sd_useful.append(to_append)

		data = np.array([range(1, num_weeks+1), useful])
	  	p = ggplot(DataFrame(data), aes(x=range(1,num_weeks+1), y=useful)) + \
	  	geom_line() + \
	  	geom_point() + \
	  	ylim(0,10) + \
	  	xlab('Week') + \
	  	ylab('Mean Rating') + \
	  	ggtitle(title)
	  	ggsave(p, "../../client/media/images/graph2.png", scale=0.75)
	elif question == 3:
		enthus = []
		for i in range(num_weeks):
			to_append = temps[i][2] * 10
			enthus.append(to_append)

		sd_enthus = []
		for i in range(num_weeks):
			to_append = se[i][2] * 20
			sd_enthus.append(to_append)

		data = np.array([range(1, num_weeks+1), enthus])
	  	p = ggplot(DataFrame(data), aes(x=range(1,num_weeks+1), y=enthus)) + \
	  	geom_line() + \
	  	geom_point() + \
	  	ylim(0,10) + \
	  	xlab('Week') + \
	  	ylab('Mean Rating') + \
	  	ggtitle(title)
	  	ggsave(p, "../../client/media/images/graph3.png", scale=0.75)
	elif question == 4:
		perf = []
		for i in range(num_weeks):
			to_append = temps[i][3] * 10
			perf.append(to_append)

		sd_perf = []
		for i in range(num_weeks):
			to_append = se[i][3] * 20
			sd_perf.append(to_append)

		data = np.array([range(1, num_weeks+1), perf])
		p = ggplot(DataFrame(data), aes(x=range(1,num_weeks+1), y=perf)) + \
	  	geom_line() + \
	  	geom_point() + \
	  	ylim(0,10) + \
	  	xlab('Week') + \
	  	ylab('Mean Rating') + \
	  	ggtitle(title)
	  	ggsave(p, "../../client/media/images/graph4.png", scale=0.75)
	else:
		hw = []
		for i in range(num_weeks):
			to_append = temps[i][4] * 10
			hw.append(to_append)

		sd_hw = []
		for i in range(num_weeks):
			to_append = se[i][4] * 20
			sd_hw.append(to_append)

	  	data = np.array([range(1, num_weeks+1), hw])
		p = ggplot(DataFrame(data), aes(x=range(1,num_weeks+1), y=hw)) + \
	  	geom_line() + \
	  	geom_point() + \
	  	ylim(0,10) + \
	  	xlab('Week') + \
	  	ylab('Mean Rating') + \
	  	ggtitle(title)
	  	ggsave(p, "../../client/media/images/graph5.png", scale=0.75)

user_set = User.objects.filter(is_active=True)
stats(user_set, 1)
stats(user_set, 2)
stats(user_set, 3)
stats(user_set, 4)
stats(user_set, 5)


