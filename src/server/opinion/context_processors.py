from opinion.settings_local import URL_ROOT
from opinion.settings_local import ASSETS_URL
from opinion.opinion_core.models import Settings

def url_root(request):
	context_extras = {}
	if URL_ROOT:
		context_extras['url_root'] = URL_ROOT
	return context_extras
	
def entry_codes(request):
	context_extras = {}
	if Settings.objects.boolean('USE_ENTRY_CODES'):
		context_extras['entry_codes'] = True
	return context_extras
	
def assets_url(request):
	context_extras = {}
	if ASSETS_URL:
		context_extras['assets_url'] = ASSETS_URL
	return context_extras
