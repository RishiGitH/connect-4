import urllib.parse

def calculate_cache_key(view_instance, view_method, request, args, kwargs):
	#:1:apicaching.get./api/1/global-request-track
	#":1:apicaching.get./api/1/global-request-track?request_id=%5B%27test-1%27%5D&fields=%5B%27request_id%27%5D"
	#/api/1/global-request-track?request_id=test-1&fields=request_id
	url = str(request.path) 
	request_get_items = dict(request.query_params)
	request_get_items.pop('magicflag', None)
	url += '?' + urllib.parse.urlencode(request_get_items).encode('ascii', 'ignore').decode('ascii')
	return '.'.join(['apicaching', str(view_method.__name__).lower(), str(url)])