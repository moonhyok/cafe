#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
import numpy as np
import random
import os

data =  int(os.popen("./total_users_apache_logs.sh").readlines()[0].rstrip())
print data
su = User.objects.filter(id=1)[0]
udo  = UserData.objects.filter(user=su,key='total_count').delete()
udo =  UserData(user=su,key='total_count',value=data)
udo.save()

