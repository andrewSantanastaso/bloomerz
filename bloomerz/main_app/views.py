from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
# Create your views here.


def homepage(request):
    return render(request, 'main_app/homepage.html')

class Home(LoginView):
    template_name = 'homepage.html'
    
