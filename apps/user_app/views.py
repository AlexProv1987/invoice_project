from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def LoginView(request):
    if request.user.is_authenticated:
        return redirect('invoice-gen')
    else:
        return HttpResponseRedirect(reverse('login'))

def LandingPage(request):
    return render (request, 'landingpage.html')