from django.http import HttpResponse
import urllib
def receive_sms(request):
    if request.method == 'GET':
        gt = request.GET
        if (gt.__contains__("mobilenumber") and gt.__contains__("message") and gt.__contains__("SHORTCODE") and gt.__contains__("Rcvd")):
            return gt
        else:
            return False
    else:
        return False

#returns -1 on failure
def send_sms(mobilenumber,message):
    url = "https://smsapi.txtimpact.com/smsadmin/submitsm.aspx"
    params = urllib.urlencode({'ID': 2.0,'USERID':'hwl_sms','PASSWORD':'hwlsms','VASID':1322,'PROFILEID':2,'FROM':27126,'TO':mobilenumber,'TEXT':message})
    f = urllib.urlopen(url,params)
    return f.read().find("JOBID")
