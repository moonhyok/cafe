import environ
from opinion_core.models import *
from opinion.scripts.user_stats import stats
from opinion.includes.queryutils import *
from opinion.includes.wilson_scores import *
from opinion.includes.calculate_score import get_score
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime

num_weeks = calculate_week(User.objects.filter(is_active=True))[0]

title = 'M-CAFEWeek{0}Update.pdf'.format(str(num_weeks))
doc = SimpleDocTemplate(title)
story = []

styles = getSampleStyleSheet()

heading1 = '<font size=20>' + 'M-CAFE Week {0} Update'.format(str(num_weeks)) \
			+ '</font>'
style1 = styles['Title']
p1 = Paragraph(heading1, style1)
story.append(p1)
story.append(Spacer(1, 12))

heading2 = '<font size=16>' + 'M-CAFE Team' + '</font>'
style2 = ParagraphStyle(name='Centered Title', alignment=1)
p2 = Paragraph(heading2, style2)
story.append(p2)
story.append(Spacer(1, 12))

heading3 = '<font size=16>' + str(datetime.date.today()) + '</font>'
p3 = Paragraph(heading3, style2)
story.append(p3)
story.append(Spacer(1, 24))

part_summary = '<strong>Participation Summary:</strong>'
style_norm = styles['Normal']
story.append(Paragraph(part_summary, style_norm))
story.append(Spacer(1, 10))


today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=7)
today = datetime.datetime.combine(today, datetime.time())
start_of_week = datetime.datetime.combine(start_of_week, datetime.time())

qat = UserRating.objects.filter(created__gte=start_of_week,
				created__lt=today).count()
qat = '{0} students responded to the QATs this week.'.format(qat)
story.append(Paragraph(qat, style_norm))
story.append(Spacer(1, 10))

ideas = DiscussionComment.objects.filter(created__gte=start_of_week,
							created__lt=today)
num_ideas = ideas.count()
rated = 0
for comment in ideas:
	if comment.ratings.count() > 0:
		rated += 1

text = '{0} new ideas with {1} rated.'.format(num_ideas, rated)
story.append(Paragraph(text, style_norm))
story.append(Spacer(1, 10))

total_ideas = DiscussionComment.objects.all().count()
total_comm_ratings = CommentRating.objects.all().count()
text = '{0} total ideas with {1} total peer-to-peer ratings.'.format(
	total_ideas, total_comm_ratings)
story.append(Paragraph(text, style_norm))
story.append(Spacer(1, 10))

bold_text = '<strong>Mean values of QATs up to this week:</strong>'
story.append(Paragraph(bold_text, style_norm))
story.append(Spacer(1, 10))

note = '*Plots are based on the mean ratings each week for the entire class'
story.append(Paragraph(note, style_norm))
story.append(Spacer(1, 10))

user_set = User.objects.filter(is_active=True)
for i in range(1, 6):
	stats(user_set, i)
	path = '../../client/media/images/graph{0}.png'.format(i)
	img = Image(path, 5*inch, 4*inch)
	story.append(img)
	story.append(Spacer(1, 10))

text = '<strong>New Ideas</strong>'
story.append(Paragraph(text, style_norm))
story.append(Spacer(1, 10))

text = '*Ideas are ranked by their Wilson scores. ' + \
	'Ideas with no ratings so far are displayed at the end.'
story.append(Paragraph(text, style_norm))
story.append(Spacer(1, 10))

data = [['Time', 'Score', '# Ratings', 'Idea']]

body_text_style = styles["BodyText"]
wilson = wilson_scores(ideas)
for com in wilson:
	row = []
	row.append(str(com.created))
	score = "{0:.3f}".format(get_score(com)[0])
	row.append(score)
	ratings = CommentRating.objects.filter(comment = com.id).count()
	row.append(ratings)
	row.append(Paragraph(str(com.comment), body_text_style))
	data.append(row)

num_rows = len(data)
tbl = Table(data, colWidths=[1.5*inch, 1*inch, 1*inch, 3*inch])
tbl_style = TableStyle([('ALIGN', (1,1), (-2,-2),'RIGHT'),
                       ('TEXTCOLOR', (1,1), (-2,-2), colors.black),
                       ('VALIGN', (0,0), (0,-1),'TOP'),
                       ('TEXTCOLOR', (0,0), (0,-1), colors.black),
                       ('ALIGN', (0,-1), (-1,-1), 'RIGHT'),
                       ('VALIGN', (0, 0), (-1,-1), 'TOP'),
                       ('TEXTCOLOR', (0,-1), (-1,-1), colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.5, colors.black)
                       ])
tbl.setStyle(tbl_style)
story.append(tbl)



doc.build(story)





