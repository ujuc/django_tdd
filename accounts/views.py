from django.contrib.auth import authenticate
from django.http import httpResponse

def persona_login():
	authenticate(assertion=request.POST['assertion'])
	return httpResponse()