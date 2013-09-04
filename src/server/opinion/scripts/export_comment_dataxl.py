#!/usr/bin/env python
import environ
from xlwt.Workbook import *
from numpy import mean
from opinion.opinion_core.models import *

# variables
headers = ["ID","Email","Username","Productivity","Involvement","Implementation","Leadership","Technology","Comment","Spatial Score (between 0 -1)","Number of agreement ratings","Mean agreement rating (between 0 -1)","Number of insightfulness ratings","Mean insighfulness rating (0 - 1)"]
stmt_ids = [1,2,3,4,5]
default_stmt_rating = 0.5
disc_stmt_id = 1

# xl file
wb = Workbook()
ws0 = wb.add_sheet('0')

# intialize headers
for i in range(len(headers)):
	ws0.write(0, i, headers[i])

# write data for users
row_num = 1
users = User.objects.all()
for user in users:
		
	# Id, email, username
	ws0.write(row_num, 0, user.id)
	ws0.write(row_num, 1, user.email)
	ws0.write(row_num, 2, user.username)
	
	# stmts
	for i in range(len(stmt_ids)):
		stmt_rating = UserRating.objects.filter(user = user, opinion_space_statement = stmt_ids[i], is_current = True)
		if len(stmt_rating) > 0:
			ws0.write(row_num, 3 + i, stmt_rating[0].rating)
		else:
			ws0.write(row_num, 3 + i, default_stmt_rating)
	
	# comment
	comment = DiscussionComment.objects.filter(user = user, discussion_statement = disc_stmt_id, is_current = True)
	
	if len(comment) == 0: # no comment, so move on to next user
		row_num += 1
		continue
	
	# comment data
	comment = comment[0]
	ws0.write(row_num, 8, comment.comment)
	ws0.write(row_num, 9, comment.normalized_score_sum)
	
	# rating data
	a_ratings = comment.agreeance.filter(is_current = True)
	ws0.write(row_num, 10, a_ratings.count())
	ws0.write(row_num, 11, mean([a.agreement for a in a_ratings]))
	
	i_ratings = comment.ratings.filter(is_current = True)
	ws0.write(row_num, 12, i_ratings.count())
	ws0.write(row_num, 13, mean([i.rating for i in i_ratings]))
	
	# increment row
	row_num += 1
	
# save
wb.save('exported_user_data.xls')