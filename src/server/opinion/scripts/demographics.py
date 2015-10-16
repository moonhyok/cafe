import environ
from opinion.opinion_core.models import *
import matplotlib.pyplot as plt
from collections import Counter
from textwrap import wrap

def count_occurences(lst):
	"""
	Counts the number of occurences of the
	values in lst and returns a list of the values
	and their respective counts.
	"""
	c = Counter(lst)
	labels = []
	counts = []
	for key, num in c.items():
		if key == "-1" or key == "":
			key = "Not Specified"
		labels.append(key)
		counts.append(num)
	return labels, counts

def format_text(lst):
	"""
	Formats the words in lst so that they fit into the
	demographics graphs.
	"""
	ret = []
	for word in lst:
		if len(word) > 25:
			low = 0
			ind = word.find(" ", low, -1)
			while (ind != -1):
				if (ind - low) >= 10:
					temp = list(word)
					temp[ind] = "\n"
					word = "".join(temp)
				low = ind + 1
				ind = word.find(" ", low, -1)
		ret.append(word)
	return ret


def demographics():
	majors = []
	for data in UserData.objects.filter(key="major"):
		majors.append(data.value)

	years = []
	for data in UserData.objects.filter(key="year"):
		years.append(data.value)

	courses_taken = []
	for data in UserData.objects.filter(key="regdesign"):
		courses_taken.append(data.value)

	interest = []
	for data in UserData.objects.filter(key="interests"):
		interest.append(data.value)


	colors = ['r', 'g', 'b', 'blueviolet', 'coral', 'darkblue',
		'deeppink', 'orangered', 'purple', 'limegreen', 'mediumturquoise',
		'greenyellow']

	labels, counts = count_occurences(majors)
	labels = format_text(labels)
	fig, ax = plt.subplots()
	patches, texts, autotexts = plt.pie(counts, labels=labels,
		autopct="%1.1f%%", colors=colors, pctdistance=0.9)
	ax.set_title("Majors")
	for t in texts:
		t.set_size("small")
		t.set_rotation_mode("anchor")
		t.set_rotation(-15)
	for t in autotexts:
		t.set_size("small")
		t.set_color("white")
	ax.set_aspect('equal')
	fig.savefig('/var/www/opinion/opinion.berkeley.edu/landing/m-cafe/ieor115-fa15/src/client/media/images/majors.png')


	labels, counts = count_occurences(years)
	fig, ax = plt.subplots()
	patches, texts, autotexts = plt.pie(counts, labels=labels,
		autopct="%1.1f%%", colors=colors, pctdistance=0.9)
	ax.set_title("Year")
	for t in texts:
		t.set_size("small")
	for t in autotexts:
		t.set_size("small")
		t.set_color("white")
	ax.set_aspect('equal')
	fig.savefig('/var/www/opinion/opinion.berkeley.edu/landing/m-cafe/ieor115-fa15/src/client/media/images/years.png')


	labels, counts = count_occurences(courses_taken)
	fig, ax = plt.subplots()
	patches, texts, autotexts = plt.pie(counts, labels=labels,
		autopct="%1.1f%%", colors=colors, pctdistance=0.9)
	ax.set_title("Number of Design Courses Taken")
	for t in texts:
		t.set_size("small")
	for t in autotexts:
		t.set_size("small")
		t.set_color("white")
	ax.set_aspect('equal')
	fig.savefig('/var/www/opinion/opinion.berkeley.edu/landing/m-cafe/ieor115-fa15/src/client/media/images/courses.png')


	labels, counts = count_occurences(interest)
	fig, ax = plt.subplots()
	patches, texts, autotexts = plt.pie(counts, labels=labels,
		autopct="%1.1f%%", colors=colors, pctdistance=0.9)
	ax.set_title("Interests")
	for t in texts:
		t.set_size("small")
	for t in autotexts:
		t.set_size("small")
		t.set_color("white")
	ax.set_aspect('equal')
	fig.savefig('/var/www/opinion/opinion.berkeley.edu/landing/m-cafe/ieor115-fa15/src/client/media/images/interests.png')

demographics()

