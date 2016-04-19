import os
import environ
from opinion.opinion_core.models import *
import numpy as np
from django.db.models import Avg
import matplotlib.pyplot as plt
from collections import Counter

def comment_corr(comments):
	tags = []
	# populate list of all possible tags
	#for c in DiscussionComment.objects.all():
	for c in comments:
		tag = AdminCommentTag.objects.get(comment=c).tag
		if tag not in tags:
			if tag == "":
			 	if "Other" not in tags:
					tags.append("Other")
			else:
				tags.append(tag)

	ratings = []
	comment_topics = []
	for c in DiscussionComment.objects.all():
		row = []
		tag = AdminCommentTag.objects.get(comment=c).tag
		if tag == "":
			comment_topics.append("Other")
		else:
			comment_topics.append(tag)
		user_ratings = []
		for i in range(5):
			rating = UserRating.objects.filter(user=c.user, \
				opinion_space_statement__statement_number=i).aggregate(Avg('rating'))
			if i == 0:
				rating['rating__avg'] = -rating['rating__avg']
			user_ratings.append(rating['rating__avg'])
		row.extend(user_ratings)
		topic_array = []
		for j in range(len(tags)):
			if tag == tags[j]:
				topic_array.append(1)
			elif tag == "" and tags[j] == "Other":
				topic_array.append(1)
			else:
				topic_array.append(0)
		row.extend(topic_array)		
		ratings.append(row)		# Add this user's ratings to ratings[]

	corr = np.corrcoef(np.transpose(ratings))
	c = corr[:len(tags), 5:]
	final = {}
	for i in range(len(tags)):
		final[tags[i]] = sum(c[:,i])

	# print Topic <correlation>
	# for topic, c in final.items():
	# 	print(topic + " " + str(c))

	return final


def plot_comment_corr(final, tags):
	count = Counter(comment_topics)
	num_comments = []
	vals = []
	for k, v in sorted(count.items()):
		num_comments.append(v*50)
	for k, v, in sorted(final.items()):
		vals.append(v)
	# scatterplot with positive/negative; size of circle being how many people talk about it
	plt.scatter(vals, np.arange(len(tags)), s=num_comments)
	plt.xlabel("Correlation")
	y = 0
	for topic, x in sorted(final.items()):
		plt.annotate(topic, (x + 0.01, y + 0.01))
		y += 1
	plt.vlines([0], 0, len(tags), color='r', linestyles='dashed')
	plt.show()
	