from django.utils.simplejson.encoder import JSONEncoder
from django.http import Http404, HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
from tracking.models import VisitorTracked, u_clean as uc
from datetime import datetime

def update_active_users(request):
    """
    Returns a list of all active users
    """
    if request.is_ajax():
        active = VisitorTracked.objects.active()
        user = getattr(request, 'user', None)

        info = {
            'active': active,
            'registered': active.filter(user__isnull=False),
            'guests': active.filter(user__isnull=True),
            'user': user
        }

        # render the list of active users
        t = loader.get_template('tracking/_active_users.html')
        c = Context(info)
        users = {'users': t.render(c)}

        return HttpResponse(content=JSONEncoder().encode(users))

    # if the request was not made via AJAX, raise a 404
    raise Http404

def get_active_users(request):
    """
    Retrieves a list of active users which is returned as plain JSON for
    easier manipulation with JavaScript.
    """
    if request.is_ajax():
        active = VisitorTracked.objects.active().reverse()
        now = datetime.now()

        # we don't put the session key or IP address here for security reasons
        data = {'users': [{
                'id': v.id,
                #'user': uc(v.user),
                'user_agent': uc(v.user_agent),
                'referrer': uc(v.referrer),
                'url': uc(v.url),
                'page_views': v.page_views,
                'geoip': v.geoip_data_json,
                'last_update': (now - v.last_update).seconds,
                'friendly_time': ', '.join(friendly_time((now - v.last_update).seconds)),
            } for v in active]}
        #print data

        response = HttpResponse(content=JSONEncoder().encode(data),
                                mimetype='text/javascript')
        response['Content-Length'] = len(response.content)

        return response

    # if the request was not made via AJAX, raise a 404
    raise Http404

def friendly_time(last_update):
    minutes = last_update / 60
    seconds = last_update % 60

    friendly_time = []
    if minutes > 0:
        msuff = ('s' if minutes != 1 else '')
        friendly_time.append('%i minute%s' % (minutes, msuff))
    if seconds > 0:
        ssuff = ('s' if seconds != 1 else '')
        friendly_time.append('%i second%s' % (seconds, ssuff))

    return friendly_time

def display_map(request):
    """
    Displays a map of recently active users.  Requires a Google Maps API key
    and GeoIP in order to be most effective.
    """
    GOOGLE_MAPS_KEY = getattr(settings, 'GOOGLE_MAPS_KEY', None)

    return render_to_response('tracking/visitor_map.html',
                              {'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY},
                              context_instance=RequestContext(request))
