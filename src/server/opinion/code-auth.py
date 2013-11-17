from django.conf import settings
from django.contrib.auth.models import User
from opinion.opinion_core.models import *

class EntryCodeModelBackend(object):
    def authenticate(self, entrycode):
        candidate=EntryCode.objects.filter(code__exact=entrycode)
        if len(candidate)>0:
           user = User.objects.filter(email__exact=candidate[0].username)
           return user[0]
        else:
           return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
