#!/usr/bin/env python
import environ
from opinion.opinion_core.models import *
from opinion.includes.queryutils import *
from django.core.mail import EmailMessage
from django.utils.http import int_to_base36
import hashlib
import datetime

subject = 'Opinion Space: Notification'
from_email = Settings.objects.string('DEFAULT_FROM_EMAIL')
    
body = """Hello {USERNAME},

There have been several updates to the system since your last visit.
{NOTIFICATIONS}

- the Hybrid Wisdom Team



To unsubscribe: {UNSUBSCRIBE_LINK}
"""


def send_notifications(os_id = 1):
    # Get OS
    os = get_os(os_id)
    
    # Get handle of current discussion statement
    discussion_statements = DiscussionStatement.objects.filter(opinion_space = os, is_current = True)
    if len(discussion_statements) == 0:
        return json_error('No Discussion Statements')    
    current_disc_stmt = discussion_statements[0]
    
    users = User.objects.exclude(email = "").exclude(userdata__key = 'unsubscribe_notification_updates')
    for user in users:
        send_user_notifications(user, os, current_disc_stmt)

def createUnsubscribeLink(user):
    uid = int_to_base36(user.id)
    url_root = settings.URL_ROOT
    hasher = hashlib.md5()
    hasher.update(user.email)
    token = hasher.hexdigest()
    return url_root + '/accountsjson/unsubscribe/notifications/' + uid + '-' + token + '/'

def createNotificationBody(user, os, disc_stmt):
    num_updated_comments = 0
    num_new_ratings = 0
    num_new_suggestions = 0
    num_new_suggestion_ratings = 0
    notifications = get_n_recent_notification_events(-1,user,os,disc_stmt)
    notificationViewSessions = UserData.objects.filter(user = user, key = 'last_notification_query')
    lastViewTime = datetime.datetime.fromtimestamp(float(notificationViewSessions[0].value)) 
    if (len(notificationViewSessions)==0):
        lastViewTime = datetime.datetime(datetime.MINYEAR, 1, 1, tzinfo=None) 
    
    # notifications is sorted in descending time, so once we find one that is old, the rest are also old
    for i in xrange(len(notifications)):
        if (notifications[i]['time'] < lastViewTime):
            break
        if (notifications[i]['type']=='suggestion_update'):
            num_updated_comments += 1
        elif (notifications[i]['type']=='rating'):
            num_new_ratings += 1
        elif (notifications[i]['type']=='suggestion'):
            num_new_suggestions += 1
        elif (notifications[i]['type']=='suggestion_rating'):
            num_new_suggestion_ratings += 1
    
    notification_body = ""
    if(num_new_ratings!=0):
        notification_body += "\n You have received "+str(num_new_ratings)+" new rating(s)"
    if(num_new_suggestions!=0):
        notification_body += "\n You have received "+str(num_new_suggestions)+" new suggestion(s)"
    if(num_new_suggestion_ratings!=0):
        notification_body += "\n "+str(num_new_suggestion_ratings)+" of your suggestion(s) have been rated"
    if(num_updated_comments!=0):
        notification_body += "\n "+str(num_updated_comments)+" comment(s) have been updated"
    return notification_body

def send_user_notifications(user, os, disc_stmt):
    userbody = body.replace('{USERNAME}', user.username).replace('{UNSUBSCRIBE_LINK}', createUnsubscribeLink(user))
    
    notification_body = createNotificationBody(user, os, disc_stmt)
    if(notification_body != ""):
        userbody = userbody.replace('{NOTIFICATIONS}', notification_body)
        email = EmailMessage(subject = subject,
                         body = userbody,
                         from_email = from_email,
                         to = [user.email],
                         headers = {'Reply-To': Settings.objects.string('DEFAULT_FROM_EMAIL')})
        email.send()

if __name__ == '__main__':
    send_notifications()
    
