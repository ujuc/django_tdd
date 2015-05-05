from django.contrib.auth import authenticate
from django.http import HttpResponse

def persona_login():
    authenticate(assertion=request.POST['assertion'])
    if user:
        login(request, user)
    return HttpResponse('OK')