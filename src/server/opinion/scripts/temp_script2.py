#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import random

for s in Settings.objects.all():
	print s.key,s.value

