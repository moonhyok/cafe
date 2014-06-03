"""
URLConf for Django user registration and authentication.

If the default behavior of the registration views is acceptable to
you, simply use a line like this in your root URLConf to set up the
default URLs for registration::

    (r'^accounts/', include('registration.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

But if you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead. If you do, it's a
good idea to use the names ``registration_activate``,
``registration_complete`` and ``registration_register`` for the
various steps of the user-signup process.

"""


from django.conf.urls.defaults import *

from registration_json import views


urlpatterns = patterns('',
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           views.activate,
                           name='registration_activate'),
                       url(r'^login/$',
                           views.login,
                           name='auth_login'),
                       url(r'^logout/$',
                           views.logout,
                           name='auth_logout'),
                       url(r'^password/change/$',
                           views.password_change,
                           name='auth_password_change'),
                       url(r'^password/reset/$',
                           views.password_reset2,
                           name='auth_password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           views.password_reset_confirm,
                           name='auth_password_reset_confirm'),
                       url(r'^password/create/$',
                           views.password_create,
                           name='auth_password_create'),
                       url(r'^register/$',
                           views.register,
                           name='registration_register'),
                       url(r'^suggest/$',
                           views.username_suggest,
                           name='auth_suggest'),
                       url(r'^update/$',
                           views.update_user_data_field,
                           name='auth_update'),
                       url(r'^entrycode/get/$',
                           views.get_entry_code,
                           name='auth_entry_get'),
                       url(r'^entrycode/firstlogin/$',
                           views.get_entry_code_first_login,
                           name='auth_entry_get_login_status'),
                       url(r'^upload/picture/$',
                       	   views.upload_file,
			               name='auth_entry_upload_picture'),
						url(r'^authstate/$',
                           views.get_auth_state,
						   name='auth_state'),
						url(r'^clearautherr/$',
						   views.clear_auth_err,
						   name='auth_err'),
                        url(r'^unsubscribe/notifications/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                            views.unsubscribe_notifications,
                            name='unsubscribe_notifications'),
                       )
