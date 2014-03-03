#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
from opinion.includes.queryutils import *

uids =[785, 488, 769, 764, 779, 1335, 1561, 1245]
for u in User.objects.filter(id__in = uids):
    ratings = CommentAgreement.objects.filter(rater = u).count()
    print ratings*100


