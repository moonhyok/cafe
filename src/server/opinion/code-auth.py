from django.conf import settings
from django.contrib.auth.models import User
from opinion.opinion_core.models import *

class EntryCodeModelBackend(object):
    def authenticate(self, entrycode):
        candidate=EntryCode.objects.filter(code__exact=entrycode).order_by('id')
        if len(candidate)>0:
           if entrycode=='3bd2939':
               user = User.objects.filter(username__exact=candidate[len(candidate)-2].username).order_by('id')
               if len(user)>0:
                  return user[len(user)-1]
               else:
                  return None
           else:
               user = User.objects.filter(username__exact=candidate[len(candidate)-1].username).order_by('id')
               if len(user)==0:
                  return None
               else:
                  return user[len(user)-1]
        else:
           return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
