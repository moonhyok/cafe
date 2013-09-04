#!/usr/bin/python
import sys
import environ
import pickle
import fileinput
import md5
from opinion.opinion_core.models import *
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

#creates a table of users, emails, passwords, entry codes, dumps to console
#entry 0 username
#entry 1 email
#entry 2 password
#entry 3 entrycode


if len(sys.argv) < 4:
	print "Usage: python create_entry_code_users.py username_base file_to_read inital_base"
	sys.exit()

username_base = sys.argv[1] #base username to use
email_base = "" #not sure what we want here
file_to_read = sys.argv[2] 
n = int(sys.argv[3])  #initial numeric base

for line in fileinput.input(file_to_read):
    password = User.objects.make_random_password(8) #generates a random password
    user = User.objects.create_user(username_base + str(n), "", password)
    user.save()

    #generates an entry code and creates the associated object
    m = md5.md5()
    m.update(password + line)
    numericalcode = m.hexdigest() 
    entrycode = EntryCode(username = username_base + str(n), code = str(numericalcode), first_login = True)
    entrycode.save()

    username = username_base + str(n);
    email = ""

    pid = UserData(user = user,key = "pid",value = line.strip())
    pid.save()

    print  line.strip() + "\t" + username + "\t" + password + "\t " + str(numericalcode)
    n = n + 1
