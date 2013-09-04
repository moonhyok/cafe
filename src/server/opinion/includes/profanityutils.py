# Checks if there is any profanity in the provided text
from profanity_list import *

def check_bad_words(value):
	value_lowered = value.lower()
	value_split = value_lowered.split(' ')
	words_seen = [w for w in PROFANITY_LIST if w in value_lowered]
	
	profanity = ""
	original_words = ""
	for word in words_seen:
		# Remove false positives by making sure the entire word is used
		# Add words to this list that can be any sub-string of a non profane word (i.e. poon in spoon)
		if word in FULL_WORDS_LIST:
			if word in value_split:
				profanity += word + ' '
				original_words += word + ' '
		else:
			for w in value_split:
				if word in w:
					profanity += word + ' '
					original_words += w + ' '
	
	if profanity:
		return [True, profanity, original_words]
	else:
		return [False, [], []]