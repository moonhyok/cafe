#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

u = User.objects.filter(id = 1)[0]
print u.username
u.set_password('admin')
u.save()


