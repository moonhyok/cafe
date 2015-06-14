#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import settings
import time

from sh import say as _say
from sh import mkdir

BASE_DIR = "./../../client/media/audio.{}/".format(time.time())
mkdir("-p", BASE_DIR)

def say(txt, path):
        _say("-r 200", "-vSamantha", "-o" + BASE_DIR + path, _in=txt)

for comment in DiscussionComment.objects.all():
	path = str(comment.id) + ".ogg"
        say(comment.comment, path)

for statement in OpinionSpaceStatement.objects.all():
	path = "statement-{}.ogg".format(statement.id)
        say(statement.statement, path)

say("Each leaf represents a participant. Tap any leaf to begin. The question is... in what specific way can the nutrition centers be improved and why?", "leaves-instructions.ogg")
say("Please rate the importance of that suggestion from a participant. A red face means the suggestion is not very important and a green face means the suggestion is very important.", "listen-comment-instructions.ogg")
say("Please rate whether you agree with the statement. A red face means you strongly disagree with the statement, and a green face means you strongly agree.", "listen-statement-instructions.ogg")
say("This is how your responses compare to others who have completed this survey.", "compare-instructions.ogg")

# Converts ogg files to wav files
# ls *.ogg | cut -d. -f1 | xargs -I{} ffmpeg -i {}.ogg {}.wav
