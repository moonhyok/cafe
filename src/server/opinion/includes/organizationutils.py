from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
import numpy as np


def filter_by_org(id):
	events = LogUserEvents.objects.filter(log_type=10, details=id)
	visitor_set = Visitor.objects.filter(id__in = events.values_list('logger_id',flat= True))
	user_set = visitor_set.exclude(user = None).values_list('user', flat=True)
	return (visitor_set, user_set)

def response_set(user_set):
	return DiscussionComment.objects.filter(user__in = user_set,is_current=True)

def rating_set(visitor_set):
	ratings = {'var1': [], 'var2': [], 'var3':[], 'var4':[], 'var5':[], 'var6':[]}
	skip_count = {1: 0, 2: 0, 3:0, 4:0, 5:0, 6:0}
	for v in visitor_set:
        	skip_logs = LogUserEvents.objects.filter(logger_id = v.id, log_type=11, details__contains='skip')
        	for i in range(1,7):
                	if skip_logs.filter(details__contains = str(i)).count() >= 1:
                        	skip_count[i] = skip_count[i] + 1
                	else:
                        	final_set = LogUserEvents.objects.filter(logger_id = v.id, log_type=11).exclude(details__contains='skip').exclude(details__contains='grade')
                        	final_set = final_set.filter(details__contains = str(i)).order_by('-created')
                        	if final_set.count() >= 1:
                                	rating =final_set[0].details[12:].lstrip()
                                	ratings['var' + str(i)].append(float(rating))
	return (ratings, skip_count)

def rating_dict_to_grades(ratings):
	medians = []
	for i in range(1,7):
		median = np.median(ratings['var' + str(i)])
		s = OpinionSpaceStatement.objects.filter(id = i)
		s = s[0]
		medians.append((s.short_version,score_to_grade((1-median)*100)))
	return medians

def get_organization_data(orgid):
	orgusers = filter_by_org(orgid)
	responses = response_set(orgusers[1])
	ratings = rating_set(orgusers[0])
	grades = rating_dict_to_grades(ratings[0])
	return {'responses': responses, 'grades': grades, 'vistorlist': orgusers[0]}
