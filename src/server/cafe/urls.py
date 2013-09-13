from django.conf.urls.defaults import *
from django.conf import settings
from cafe.cafe_core.views import index
from cafe.settings import DEBUG

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^', include('cafe.cafe_core.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^accountsjson/', include('registration_json.urls')),
)

# Enable admin  
#from django.contrib import admin
#admin.autodiscover()
#urlpatterns += patterns('', (r'^admin/(.*)', admin.site.root))

urlpatterns += settings.STATIC_MEDIA_PATTERN
