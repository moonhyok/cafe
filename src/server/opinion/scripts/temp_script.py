#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np

c = User.objects.filter(is_active = False).count()
print c
