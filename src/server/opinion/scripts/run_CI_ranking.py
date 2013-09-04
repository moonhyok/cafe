#!/usr/bin/env python
import sys
import environ
import math
from matplotlib import mlab
from opinion.opinion_core.models import *
from opinion.includes.queryutils import get_os, get_disc_stmt, decode_to_unicode

def EStep(lmbda, mu3, var3, mu4, var4, ratings):
	"""
	Runs the E step
	"""
	n = len(ratings) 
	I = []
	
	for i in range(n):
		#print str(ratings[i]) + ' ' + str(mu3) + ' ' + str(math.sqrt(var3))
		p3 	= lmbda * mlab.normpdf(ratings[i], mu3, math.sqrt(var3))
		p4 	= (1-lmbda) * mlab.normpdf(ratings[i], mu4, math.sqrt(var4))
		I.append(p3/(p3+p4))
	
	return I

def MStep(I, ratings):
	"""
	Runs the M step
	"""
	n 		= len(ratings)
	lmbda 	= math.fsum(I)/n
	mu3 	= math.fsum([ratings[i] * I[i] for i in range(n)]) / math.fsum(I)
	mu4 	= math.fsum([ratings[i] *(1 - I[i]) for i in range(n)]) / math.fsum([(1-I[i]) for i in range(n)])
	var3 	= math.fsum( [I[i] * math.pow(ratings[i] - mu3,2) for i in range (n)] ) / math.fsum(I)
	var4 	= math.fsum( [ (1-I[i]) * math.pow(ratings[i] - mu4,2) for i in range (n)] ) / math.fsum([(1-I[i]) for i in range(n)])
	
	return (lmbda, mu3, var3, mu4, var4)

def zero(value):
	if value == 0:
		return True
	if value < math.exp(-100):
		return True
	return False
	
def run_EM(id, lmbda, mu3, var3, mu4, var4, ratings):
	"""
	Runs EM for EM_ITERATIONS or until the update reaches a minimum difference of MIN_DELTA
	"""
	
	# iterate EM_ITERATIONS times
	for j in range(EM_ITERATIONS):

		if zero(var3) or zero(var4):
			print "var3 or var4 for id " + str(id) + "is 0"
			break
		
		# EStep
		I = EStep(lmbda, mu3, var3, mu4, var4, ratings)
		
		if math.fsum(I) == n or math.fsum(I) == 0:
			print "sum of I for id = " + str(id) + " is n or 0"
		
		# MStep
		new_params = MStep(I, ratings)
		
		# Check threshold
		if	(math.fabs(lmbda - new_params[0])<MIN_DELTA and 
			math.fabs(mu3 - new_params[1])<MIN_DELTA and 
			math.fabs(var3 - new_params[2])<MIN_DELTA and 
			math.fabs(mu4 - new_params[3])<MIN_DELTA and 
			math.fabs(var4 - new_params[4])<MIN_DELTA):
				break
		
		# Update parameters
		lmbda = new_params[0]
		mu3 = new_params[1]
		var3 = new_params[2]
		mu4 = new_params[3]
		var4 = new_params[4]	
	
	return (lmbda, mu3, var3, mu4, var4)

def rating_type(i):
	"""
	Maps rating type as an integer to it's string value
	"""
	
	if i == 0:
		return "insight"
	if i == 1:
		return "agreement"

def sanitize_comment_for_csv(comment):
	return decode_to_unicode(comment.replace('\n', ' ').replace('\r', ' ').replace('\"', '\''))

# Algorithm Constants
MIN_RATINGS			= 5
THRESHOLD_RATINGS 	= 20
EM_ITERATIONS 		= 1000
MIN_DELTA 			= 0.0001
RATING_TYPE			= 1

print "Running confidence interval ranking using {0} ratings...".format(rating_type(RATING_TYPE))

# Import all comments
os = get_os(1)
disc_stmt = get_disc_stmt(os)
comments = os.comments.filter(discussion_statement = disc_stmt, is_current = True)

# Separate comments by THRESHOLD_RATINGS 
other_comments = []
bucketed_comments = []
app_comments = []
for comment in comments:
	
	# Check type of rating
	if RATING_TYPE == 0:
		count = len(list(comment.ratings.filter(is_current = True)))
	if RATING_TYPE == 1:
		count = len(list(comment.agreeance.filter(is_current = True)))
	
	if count >= MIN_RATINGS:
		if count >= THRESHOLD_RATINGS:
			app_comments.append(comment)
		else:
			bucketed_comments.append(comment)
	else:
		other_comments.append(comment)
		
print "Number of approved comments: " + str(len(app_comments))
print "Number of bucketed comments: " + str(len(bucketed_comments))

# Initialize parameters for each approved comment
avg 	= [0 for i in range(len(app_comments))]
lmbda 	= [0 for i in range(len(app_comments))]
p1 		= [0 for i in range(len(app_comments))]
p2 		= [0 for i in range(len(app_comments))]
mu3 	= [0 for i in range(len(app_comments))]
var3 	= [0 for i in range(len(app_comments))]
mu4 	= [0 for i in range(len(app_comments))]
var4 	= [0 for i in range(len(app_comments))]

# Compute mean, p1 and p2 for each approved comment
for i in range(len(app_comments)):
	comment = app_comments[i]
	
	# Check type of rating
	if RATING_TYPE == 0:
		ratings = list(comment.ratings.filter(is_current = True))
		n = len(ratings)
		
		avg[i] 	= math.fsum([r.rating for r in ratings])/n				# mean ratings
		p1[i] 	= len([r.rating for r in ratings if r.rating == 0])/n	# probability that rating is 0
		p2[i]	= len([r.rating for r in ratings if r.rating == 1])/n	# probability that rating is 1
		
	if RATING_TYPE == 1:
		ratings = list(comment.agreeance.filter(is_current = True))
		n = len(ratings)
		
		avg[i] 	= math.fsum([r.agreement for r in ratings])/n				# mean ratings
		p1[i] 	= len([r.agreement for r in ratings if r.agreement == 0])/n	# probability that rating is 0
		p2[i]	= len([r.agreement for r in ratings if r.agreement == 1])/n	# probability that rating is 1
	
	lmbda[i] 	= 0.5													# initialize lmbda to be 0.5
	mu3[i]		= 0.25
	var3[i]		= 0.05
	mu4[i]		= 0.75
	var4[i]		= 0.05

# Initialize parameters for bucketed comments
avg_g 		= [0 for i in range(len(bucketed_comments))]
lmbda_g 	= 0.5

# Check type of rating
if RATING_TYPE == 0:
	p1_g = math.fsum([len([r.rating for r in list(comment.ratings.filter(is_current = True)) if r.rating == 0]) for comment in bucketed_comments]) / math.fsum([len(list(comment.ratings.filter(is_current = True))) for comment in bucketed_comments])
	p2_g = math.fsum([len([r.rating for r in list(comment.ratings.filter(is_current = True)) if r.rating == 1]) for comment in bucketed_comments]) / math.fsum([len(list(comment.ratings.filter(is_current = True))) for comment in bucketed_comments])

if RATING_TYPE == 1:
	p1_g = math.fsum([len([r.agreement for r in list(comment.agreeance.filter(is_current = True)) if r.agreement == 0]) for comment in bucketed_comments]) / math.fsum([len(list(comment.agreeance.filter(is_current = True))) for comment in bucketed_comments])
	p2_g = math.fsum([len([r.agreement for r in list(comment.agreeance.filter(is_current = True)) if r.agreement == 1]) for comment in bucketed_comments]) / math.fsum([len(list(comment.agreeance.filter(is_current = True))) for comment in bucketed_comments])
	
mu3_g 		= 0.25
var3_g 		= 0.05
mu4_g	 	= 0.75
var4_g 		= 0.05

# Compute mean for the bucketed comments
for i in range(len(bucketed_comments)):
	if RATING_TYPE == 0:
		avg_g[i] = math.fsum([r.rating for r in list(bucketed_comments[i].ratings.filter(is_current = True))]) / len(list(bucketed_comments[i].ratings.filter(is_current = True)))

	if RATING_TYPE == 1:
		avg_g[i] = math.fsum([r.agreement for r in list(bucketed_comments[i].agreeance.filter(is_current = True))]) / len(list(bucketed_comments[i].agreeance.filter(is_current = True)))

#
# Run EM algorithm to:
# 	- generate parameters for each approved comment's distribution
#	- generate parameters for the bucketed comments
#

print "Running EM on approved comments..."

# Approved comments
variances_app = [{} for i in range(len(app_comments))]	# 'var'->value, 'se'->value, 'score'->mean-1.96
for i in range(len(app_comments)):
	comment = app_comments[i]
	
	print str(comment.user.username) + "..."
	
	if RATING_TYPE == 0:
		ratings = list(comment.ratings.filter(is_current = True, rating__gt = 0, rating__lt = 1))	# remove any 0 or 1 ratings
		n = len(ratings)

		# Run EM
		lmbda[i], mu3[i], var3[i], mu4[i], var4[i] = run_EM(comment.user.username, lmbda[i], mu3[i], var3[i], mu4[i], var4[i], [r.rating for r in ratings])

	if RATING_TYPE == 1:
		ratings = list(comment.agreeance.filter(is_current = True, agreement__gt = 0, agreement__lt = 1))	# remove any 0 or 1 ratings
		n = len(ratings)

		# Run EM
		lmbda[i], mu3[i], var3[i], mu4[i], var4[i] = run_EM(comment.user.username, lmbda[i], mu3[i], var3[i], mu4[i], var4[i], [r.agreement for r in ratings])

	# Calculate p3 and p4
	p3 = lmbda[i] * (1 - (p1[i] + p2[i]))
	p4 = (1 - lmbda[i]) * (1 - (p1[i] + p2[i]))
	mu = p2[i] + p3*mu3[i] + p4*mu4[i]
	
	variances_app[i]['var'] = p1[i]*math.pow(mu,2) + p2[i]*(1-math.pow(mu,2)) + p3*var3[i] + p3*math.pow(mu3[i] - mu,2) + p4*var4[i] + p4*math.pow(mu4[i] - mu,2)
	variances_app[i]['se'] = math.sqrt(variances_app[i]['var'] / n)
	variances_app[i]['score'] = avg[i] - 1.96 * variances_app[i]['se']

print "Running EM on bucketed comments..."

# Bucketed comments
bucketed_ratings = []
for comment in bucketed_comments:
	if RATING_TYPE == 0:
		bucketed_ratings += [r.rating for r in list(comment.ratings.filter(is_current = True, rating__gt = 0, rating__lt = 1))]
		
	if RATING_TYPE == 1:
		bucketed_ratings += [r.agreement for r in list(comment.agreeance.filter(is_current = True, agreement__gt = 0, agreement__lt = 1))]
		
lmbda_g, mu3_g, var3_g, mu4_g, var4_g = run_EM('bucketed-comments', lmbda_g, mu3_g, var3_g, mu4_g, var4_g, bucketed_ratings)

# Calculate p3 and p4
p3 = lmbda_g * (1 - (p1_g + p2_g))
p4 = (1 - lmbda_g) * (1 - (p1_g + p2_g))
mu = p2_g + p3*mu3_g + p4*mu4_g
var_g = p1_g*math.pow(mu,2) + p2_g*(1-math.pow(mu,2)) + p3*var3_g + p3*math.pow(mu3_g - mu,2) + p4*var4_g + p4*math.pow(mu4_g - mu,2)
se_g = math.sqrt(var_g / n)
scores_g = []
for i in range(len(bucketed_comments)):
	scores_g.append(avg_g[i] - 1.96 * se_g)
	
# Sort and print solution
app_all_data = []
for i in range(len(app_comments)):
	
	comment = app_comments[i]
	
	# Get insight ratings
	i_ratings = list(comment.ratings.filter(is_current = True))
	num_i_ratings = len(i_ratings)
	avg_i_ratings = math.fsum([r.rating for r in i_ratings]) / num_i_ratings
	
	# Get agreement ratings
	a_ratings = list(comment.agreeance.filter(is_current = True))
	num_a_ratings = len(a_ratings)
	avg_a_ratings = math.fsum([r.agreement for r in a_ratings]) / num_a_ratings
	
	app_all_data.append((comment.user.username, 
						 variances_app[i]['score'],
						 comment.normalized_score_sum,
						 num_i_ratings,
						 avg_i_ratings,
						 num_a_ratings,
						 avg_a_ratings,
						 comment.created,
						 sanitize_comment_for_csv(app_comments[i].comment)))
	
sorted_ci_app_all = sorted(app_all_data, key=lambda a:a[1], reverse = True)
sorted_spatial_app_all = sorted(app_all_data, key=lambda a:a[2], reverse = True)

# Sort bucketed 
bucketed_all_data = []
for i in range(len(bucketed_comments)):
	
	comment = bucketed_comments[i]
	
	# Get insight ratings
	i_ratings = list(comment.ratings.filter(is_current = True))
	num_i_ratings = len(i_ratings)
	avg_i_ratings = math.fsum([r.rating for r in i_ratings]) / num_i_ratings
	
	# Get agreement ratings
	a_ratings = list(comment.agreeance.filter(is_current = True))
	num_a_ratings = len(a_ratings)
	avg_a_ratings = math.fsum([r.agreement for r in a_ratings]) / num_a_ratings
	
	bucketed_all_data.append((comment.user.username,
	 						  scores_g[i],
	 						  comment.normalized_score_sum, 
							  num_i_ratings,
							  avg_i_ratings,
							  num_a_ratings,
							  avg_a_ratings,
							  comment.created,
							  sanitize_comment_for_csv(bucketed_comments[i].comment)))

sorted_ci_bucketed_all = sorted(bucketed_all_data, key=lambda b:b[1], reverse = True)
sorted_spatial_bucketed_all = sorted(bucketed_all_data, key=lambda b:b[2], reverse = True)

# Sort other
other_all_data = []
for i in range(len(other_comments)):
	
	comment = other_comments[i]
	
	# Get insight ratings
	i_ratings = list(comment.ratings.filter(is_current = True))
	num_i_ratings = len(i_ratings)
	if num_i_ratings > 0:
		avg_i_ratings = math.fsum([r.rating for r in i_ratings]) / num_i_ratings
	else:
		avg_i_ratings = 0
	
	# Get agreement ratings
	a_ratings = list(comment.agreeance.filter(is_current = True))
	num_a_ratings = len(a_ratings)
	if num_a_ratings > 0:
		avg_a_ratings = math.fsum([r.agreement for r in a_ratings]) / num_a_ratings
	else:
		avg_a_ratings = 0
	
	other_all_data.append((comment.user.username,
	 						  "N/A",
	 						  comment.normalized_score_sum, 
							  num_i_ratings,
							  avg_i_ratings,
							  num_a_ratings,
							  avg_a_ratings,
							  comment.created,
							  sanitize_comment_for_csv(other_comments[i].comment)))

sorted_other_all = sorted(other_all_data, key=lambda b:b[2], reverse = True)

# Save CI ranking
f = open('ci_ranking_{0}_ratings.csv'.format(rating_type(RATING_TYPE)), 'w')
f.write('Approved Comments\n')
f.write('username, score, spatial score, num insight, avg insight, num agree, avg agree, created, comment\n')
for row in sorted_ci_app_all:
	f.write('\"' + str(row[0]) + '\",\"' + str(row[1]) + '\",\"' + str(row[2]) +  '\",\"' + str(row[3]) + '\",\"' + str(row[4]) + '\",\"' + str(row[5]) + '\",\"' + str(row[6]) + '\",\"' + str(row[7]) + '\",\"' + row[8].encode('utf-8') + '\"\n')

f.write('\n\n\n')
f.write('Bucketed Comments\n')
f.write('username, score, spatial score, num insight, avg insight, num agree, avg agree, created, comment\n')
for row in sorted_ci_bucketed_all:
	f.write('\"' + str(row[0]) + '\",\"' + str(row[1]) + '\",\"' + str(row[2]) +  '\",\"' + str(row[3]) + '\",\"' + str(row[4]) + '\",\"' + str(row[5]) + '\",\"' + str(row[6]) + '\",\"' + str(row[7]) + '\",\"' + row[8].encode('utf-8') + '\"\n')

f.close()

# Save spatial ranking
f = open('spatial_ranking_{0}_ratings.csv'.format(rating_type(RATING_TYPE)), 'w')
f.write('Approved Comments\n')
f.write('username, score, spatial score, num insight, avg insight, num agree, avg agree, created, comment\n')
for row in sorted_spatial_app_all:
	f.write('\"' + str(row[0]) + '\",\"' + str(row[1]) + '\",\"' + str(row[2]) +  '\",\"' + str(row[3]) + '\",\"' + str(row[4]) + '\",\"' + str(row[5]) + '\",\"' + str(row[6]) + '\",\"' + str(row[7]) + '\",\"' + row[8].encode('utf-8') + '\"\n')

f.write('\n\n\n')
f.write('Bucketed Comments\n')
f.write('username, score, spatial score, num insight, avg insight, num agree, avg agree, created, comment\n')
for row in sorted_spatial_bucketed_all:
	f.write('\"' + str(row[0]) + '\",\"' + str(row[1]) + '\",\"' + str(row[2]) +  '\",\"' + str(row[3]) + '\",\"' + str(row[4]) + '\",\"' + str(row[5]) + '\",\"' + str(row[6]) + '\",\"' + str(row[7]) + '\",\"' + row[8].encode('utf-8') + '\"\n')

# Save Michael's format
"""
f = open('ci_ranking_all_responses.csv', 'w')
f.write('Approved Comments\n')
f.write('ID, Response, CI Score, Spatial Score, Avg Insight, Avg Agreement, Average over all, # insight, # agreement, created, Feedback\n')
for row in sorted_ci_app_all:
	username = row[0]
	user = User.objects.filter(username = username)[0]
	pid = UserData.objects.filter(user = user, key='pid')[0].value
	feedback = UserData.objects.filter(user = user, key='q7')
	if len(feedback) > 0:
		feedback = sanitize_comment_for_csv(feedback[0].value)
	else:
		feedback = ""
	total_score = (row[1] + row[2] + row[4] + row[6])/4.0
	
	f.write('\"' + str(pid) + '\",\"' + row[8].encode('utf-8') + '\",\"' + str(row[1]) +  '\",\"' + str(row[2]) + '\",\"' + str(row[4]) + '\",\"' + str(row[6]) + '\",\"' + str(total_score) + '\",\"' + str(row[3]) + '\",\"' + str(row[5]) + '\",\"' + str(row[7]) + '\",\"' + feedback.encode('utf-8') + '\"\n')
	
f.write('\n\n\n')
f.write('Bucketed Comments\n')
f.write('ID, Suggestion, Score_CI, Score_SP, Score_IN, Score_RE, Total Score, Insight_Num, Rel_Num, created, Feedback\n')
for row in sorted_ci_bucketed_all:
	username = row[0]
	user = User.objects.filter(username = username)[0]
	pid = UserData.objects.filter(user = user, key='pid')[0].value
	feedback = UserData.objects.filter(user = user, key='q7')
	if len(feedback) > 0:
		feedback = sanitize_comment_for_csv(feedback[0].value)
	else:
		feedback = ""
	total_score = (row[1] + row[2] + row[4] + row[6])/4.0

	f.write('\"' + str(pid) + '\",\"' + row[8].encode('utf-8') + '\",\"' + str(row[1]) +  '\",\"' + str(row[2]) + '\",\"' + str(row[4]) + '\",\"' + str(row[6]) + '\",\"' + str(total_score) + '\",\"' + str(row[3]) + '\",\"' + str(row[5]) + '\",\"' + str(row[7]) + '\",\"' + feedback.encode('utf-8') + '\"\n')
	
f.write('\n\n\n')
f.write('Other Comments\n')
f.write('ID, Suggestion, Score_CI, Score_SP, Score_IN, Score_RE, Total Score, Insight_Num, Rel_Num, created, Feedback\n')
for row in sorted_other_all:
	username = row[0]
	user = User.objects.filter(username = username)[0]
	pid = UserData.objects.filter(user = user, key='pid')[0].value
	feedback = UserData.objects.filter(user = user, key='q7')
	if len(feedback) > 0:
		feedback = sanitize_comment_for_csv(feedback[0].value)
	else:
		feedback = ""
	total_score = (row[2] + row[4] + row[6])/3.0

	f.write('\"' + str(pid) + '\",\"' + row[8].encode('utf-8') + '\",\"' + str(row[1]) +  '\",\"' + str(row[2]) + '\",\"' + str(row[4]) + '\",\"' + str(row[6]) + '\",\"' + str(total_score) + '\",\"' + str(row[3]) + '\",\"' + str(row[5]) + '\",\"' + str(row[7]) + '\",\"' + feedback.encode('utf-8') + '\"\n')

f.close()
"""
