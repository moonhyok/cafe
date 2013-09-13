from django.http import Http404, HttpResponseRedirect
from cafe.includes.jsonutils import *
from cafe.cafe_core.models import *
from cafe.settings_local import URL_ROOT, ALLOW_UNAUTH_ACCESS_METHODS


def auth_required(view_func):
	"""
	Decorator checking whether a user is logged in and whether they have the proper entry code if
	USE_ENTRY_CODES = True
	"""
	def login_check(request, *args, **kwargs):
		ERROR_MSG = 'You must be authenticated to do that.'
		
		# Check basic authentication
		if request.user.is_authenticated():

			# Check for entry code
			if Settings.objects.boolean('USE_ENTRY_CODES'):

				# check for a valid entry code
				if request.method == "POST":				
					entrycode = request.POST.get("entrycode","")
					codeobject = EntryCode.objects.filter(code = entrycode)

					if entrycode == "" or len(codeobject) == 0:
						return json_result({'error': ERROR_MSG, 'auth_required': True})

					users = User.objects.filter(username=codeobject[0].username)
					if len(users) == 0:
						return json_result({'error': ERROR_MSG, 'auth_required': True})

					# check if authenticated user matches the entry code user
					if request.user != users[0]:
						return json_result({'error': ERROR_MSG, 'auth_required': True})
					else:
						return view_func(request, *args, **kwargs)
						
				else:
					# If the client doesn't post
					return json_result({'error': ERROR_MSG, 'auth_required': True})
										
			else:
				# If the user is authenticated and there are no entry codes
			    return view_func(request, *args, **kwargs)
	
		else:
			# If the user isn't authenticated
			if view_func.__name__ not in ALLOW_UNAUTH_ACCESS_METHODS:
				return json_result({'error': ERROR_MSG, 'auth_required': True})
			else:
				return view_func(request, *args, **kwargs)

	return login_check

# Decorator for checking if user has admin rights. If not then returning json error
def admin_required(view_func):
    def login_check(request, *args, **kwargs):
        if request.user.is_authenticated():
			adminuser = AdminPanelUser.objects.filter(user = request.user.id)
			if len(adminuser) == 0 and not request.user.id == 1:
				return HttpResponseRedirect(URL_ROOT+'/adminpanel/loginerror/')				
			else:
				return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(URL_ROOT+'/adminpanel/')

    return login_check
