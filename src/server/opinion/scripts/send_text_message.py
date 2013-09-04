from django.http import HttpResponse
from opinion.includes.smsutils import *
import urllib
#python script
#does checks
#
mobilenumber = raw_input('Enter phone number of person to text: ')
message = raw_input('Enter message to be sent: ') 
if send_sms(mobilenumber,message) == -1:
    print('Failed to send message')
else:
    print('Message sent successfully')
        
    
