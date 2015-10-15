from functools import wraps
frmo flask import request, Response

def check_auth(username, password):
 // Check if a username /password combination is valid
 
	return username == 'admin' and password == 'secret'
	
def authenticate():
	return Response('Could not verify your access.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated